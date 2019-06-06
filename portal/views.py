import MySQLdb

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from portal.models import *

# Create your views here.

def home(request):
    return redirect('portal:profile')
    report_types = [
        'Acquisition',
        'Catalog',
        'Patrons',
        'Circulation',
        'Serials'
    ]

    # Get all the models of the app
    from django.apps import apps
    app_models=apps.all_models['portal']

    model_names = [] # List for names of models

    for model_name, model in app_models.items():
        model_names.append(model_name)


    # Context dictionary being passed to the HTML template to display the choices.
    context = {
        'report_types':report_types,
        'tables': model_names
    }

    return render(request, 'portal/reports_home.html', context=context)

class CirculationReport(View):
    # User must be logged in to access this view

    @method_decorator(login_required)
    def get(self, request):

        return render(request, 'portal/circulation.html')

    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        print(data)
        print(data)


        db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="igcarlibrary",
            db="library"
        )
        cur = db.cursor()

        from_timestamp = '{} 00:00:01'.format(data['from_date'])
        to_timestamp = '{} 23:59:59'.format(data['to_date'])


        sql_query='''
        (SELECT bib.title AS book_title, bib.author AS book_author, it.barcode,
            TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) )as patron_name,
            b.cardnumber, b.email, b.phone, issues.issuedate AS issuedate, issues.date_due AS duedate, issues.returndate
            FROM issues
            LEFT JOIN borrowers b ON (b.borrowernumber=issues.borrowernumber)
            LEFT JOIN items it ON (it.itemnumber=issues.itemnumber)
            LEFT JOIN biblio bib ON (bib.biblionumber=it.biblionumber)
            WHERE issues.issuedate BETWEEN \'{0}\' AND \'{1}\'
        )
        UNION ALL
        (
        SELECT bib.title, bib.author, it.barcode,
            TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) )as name,
            b.cardnumber, b.email, b.phone, old_issues.issuedate, old_issues.date_due, old_issues.returndate
            FROM old_issues
            LEFT JOIN borrowers b ON (b.borrowernumber=old_issues.borrowernumber)
            LEFT JOIN items it ON (it.itemnumber=old_issues.itemnumber)
            LEFT JOIN biblio bib ON (bib.biblionumber=it.biblionumber)
            WHERE old_issues.issuedate BETWEEN \'{2}\' AND \'{3}\'
        )
        '''.format(data['from_date'],data['to_date'],data['from_date'],data['to_date'])


        from_date = data['from_date']
        to_date = data['to_date']

        # sql_query = '''SELECT biblio.title, biblio.author, items.barcode, issues.issuedate,
        #         TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) )as name, borrowers.cardnumber,
        #         borrowers.email,borrowers.phone,issues.date_due
        #     FROM issues, borrowers, items, biblio
        #     WHERE issues.issuedate BETWEEN \'{0}\' AND \'{1}\'
        #     AND borrowers.borrowernumber=issues.borrowernumber
        #     AND items.itemnumber=issues.itemnumber
        #     AND biblio.biblionumber=items.biblionumber'''.format(data['from_date'],data['to_date'])


        try:
            order_by = data.getlist('order_by')
            if order_by:
                sql_query += ' ORDER BY '
                for order in order_by:
                    filter = str(order)+'_filter'
                    sql_query += 'LOWER({})'.format( str(order) ) + ' ' + data[filter] + ','

            # Remove the last extra comma
            sql_query = sql_query[:-1]
        except:
            # No order_by filter provided
            pass


        headings = [
            'Title of the book',
            'Author',
            'Barcode',
            'Patron Name',
            'Membership Number',
            'Email ID',
            'Phone number',
            'Issue Date',
            'Due date',
            'Return Date'
        ]

        print(sql_query)

        try:
            cur.execute(sql_query)

            count=0 #To count the total number of entries

            values = []
            for row in cur.fetchall():
                count+=1
                row = list(row)
                if not row[-1]:
                    row[-1]='Not returned'
                values.append(row)

            context = {
                'count':count,
                'values':values,
                'headings':headings,
                'report_type':'Circulation Report',
                'from_date':from_date,
                'to_date':to_date
            }

            # Save the data in request session
            request.session['saved'] = data
            return render(request, 'portal/circulation_reoprt.html', context)

        except MySQLdb.Error as e:
            print(e)
            return JsonResponse({"message":"Unable to fetch data"})

class GenerateReport(APIView):

    def post(self, request):
        data = dict(request.data)
        print(data)

        # Get all the models of the app
        from django.apps import apps
        app_models=apps.all_models['portal']

        table = data['Table'][0]
        print(table)

        # Get the model selected
        model = app_models[table]
        print(model)

        # Get all columns of the table
        columns = model._meta.get_fields() # All the column classes
        column_names=[]
        for column in columns:
            try:
                column_names.append(column.attname)
            except:
                continue

        attr = []

        for row in model.objects.all():
            row_values = []
            for column_name in column_names:
                row_values.append(getattr(row, column_name))
            attr.append(row_values)

        context = {
            'column_values': column_names,
            'values': attr
        }

        return render(request, 'portal/generate_report.html', context)

class Login(View):
    '''Login the patron based on his userid and Bcrypt hashed password ? '''

    def get(self, request):

        # If the user is already logged in , redirect him to his profile page, else, the login page

        if request.user.is_authenticated:

            # If the user specified a next parameter, redirect him to that url else to his profile page
            valuenext = request.GET.get('next')
            if valuenext:
                return HttpResponseRedirect(valuenext)
            else:
                return redirect('portal:profile')
        else:
            return render(request, 'portal/login.html')

    def post(self, request):

        data = request.POST
        username = data['username']
        password = data['password']

        valuenext = request.POST.get('next')

        # Authenticate the credentials
        #This will change
        user = authenticate(username = username, password = password) # Will return Null if the credentials are wrong

        if user is not None:
            login(request, user)
            if valuenext:
                return HttpResponseRedirect(valuenext)
            else:
                return redirect('portal:profile')
        else:
            return JsonResponse({'message':'The credentials are wrong'})

def logout_view(request):
    logout(request)
    return redirect('portal:login')

@login_required
def profile(request):
    try:
        user = request.user
        return render(request, 'portal/profile.html')
    except Exception as unknown_exception:
        return JsonResponse({'message':unknown_exception})

def demo(request):
    return JsonResponse(request.session['saved'])

def checked_out(request):
    # To return all the books that are currently checked out

    sql_query = '''
        SELECT biblio.title AS book_title, biblio.author AS book_author, items.barcode,
        TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) )AS patron_name,
        borrowers.cardnumber, borrowers.email, issues.issuedate AS issuedate, issues.date_due AS duedate
        FROM issues
        LEFT JOIN borrowers ON borrowers.borrowernumber = issues.borrowernumber
        LEFT JOIN items ON items.itemnumber = issues.itemnumber
        LEFT JOIN biblio ON biblio.biblionumber = items.biblionumber
        '''

    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="igcarlibrary",
        db="library"
    )
    cur = db.cursor()


    print(sql_query)

    try:
        cur.execute(sql_query)

        count=0 #To count the total number of entries

        values = []
        for row in cur.fetchall():
            count+=1
            values.append(row)

        headings = [
            'Title of the book',
            'Author',
            'Barcode',
            'Patron Name',
            'Membership Number',
            'Email ID',
            'Issue Date',
            'Due date',
        ]

        context = {
            'count':count,
            'values':values,
            'headings':headings,
            'report_type':'Circulation Report - Books currently checked out'
        }

        return render(request, 'portal/checked_out.html', context)

    except MySQLdb.Error as e:
        print(e)
        return JsonResponse({"message":"Unable to fetch data"})

def report_types(request):
    return render(request, 'portal/types.html')

def inactive_patrons(request):
    sql_query='''
        SELECT TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) ),
        borrowers.cardnumber, borrowers.categorycode, borrowers.email
        FROM borrowers
        WHERE NOT EXISTS (
            SELECT borrowernumber FROM statistics
            WHERE borrowers.borrowernumber = borrowernumber)
        '''

    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="igcarlibrary",
        db="library"
    )
    cur = db.cursor()

    try:
        cur.execute(sql_query)

        count=0 #To count the total number of entries

        values = []
        for row in cur.fetchall():
            count+=1
            print(row)
            values.append(row)

        headings = [
            'Patron Name',
            'Membership Number',
            'Category Code',
            'Email ID'
        ]

        context = {
            'count':count,
            'values':values,
            'headings':headings,
            'report_type':'Circulation Report - Inactive Patrons'
        }

    except MySQLdb.Error as e:
        print(e)
        return JsonResponse({'message':"Unable to fetch data"})

    return render(request, 'portal/inactive_patrons.html', context=context)

def inactive_books(request):
    sql_query='''
            SELECT biblio.title, biblio.author, items.barcode
            FROM biblio, items
            WHERE NOT EXISTS (
                SELECT itemnumber FROM statistics
                WHERE items.itemnumber = itemnumber)
            AND biblio.biblionumber=items.biblionumber;
            '''
