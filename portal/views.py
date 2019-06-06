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

        import MySQLdb

        db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="igcarlibrary",
            db="library"
        )
        cur = db.cursor()

        from_timestamp = '{} 00:00:01'.format(data['from_date'])
        to_timestamp = '{} 23:59:59'.format(data['to_date'])

        sql_query = '''SELECT biblio.title, biblio.author, items.barcode, issues.issuedate,
                TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) )as name, borrowers.cardnumber,
                borrowers.email,borrowers.phone,issues.date_due
            FROM issues, borrowers, items, biblio
            WHERE issues.issuedate BETWEEN \'{0}\' AND \'{1}\'
            AND borrowers.borrowernumber=issues.borrowernumber
            AND items.itemnumber=issues.itemnumber
            AND biblio.biblionumber=items.biblionumber'''.format(data['from_date'],data['to_date'])

        try:
            order_by = data.getlist('order_by')
            if order_by:
                sql_query += ' ORDER BY '
                for order in order_by:
                    filter = str(order)+'_filter'
                    sql_query += 'LOWER({})'.format( str(order) ) + ' ' + data[filter] + ','
        except:
            # No order_by filter provided
            pass

        # Remove the last extra comma
        sql_query = sql_query[:-1]


        headings = [
            'Title of the book',
            'Author',
            'Barcode',
            'Date and time of Issue',
            'Patron Name',
            'Membership Number',
            'Email ID',
            'Phone number',
            'Due date'
        ]

        print(sql_query)

        try:
            cur.execute(sql_query)

            values = []
            for row in cur.fetchall():
                print(row)
                values.append(row)

            context = {
                'values':values,
                'headings':headings,
                'report_type':'Circulation Report'
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
