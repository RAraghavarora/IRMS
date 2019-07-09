import base64
import os
import json
import MySQLdb
import datetime
import re
import cryptography

from dal import autocomplete
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Value, Sum, Max
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View

#Using django-mysql library to Extract surname from Marctag
from django_mysql.models.functions import XMLExtractValue

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from portal.models import *
from portal.forms import ReservesForm, AqBasketForm
from portal.apps import *

from IRMS import keyconfig

text = "hello world"
text = text.encode()
salted = b'salt_'


# **************************************** IMPORTANT ************************************************************

# Extracting subtitle from Marctag -

# SELECT concat( b.title, ' ', ExtractValue((
#     SELECT metadata
#     FROM biblio_metadata b2
#     WHERE b.biblionumber = b2.biblionumber),
#       '//datafield[@tag="245"]/subfield[@code="b"]') ) AS title,
#     b.author, i.itemcallnumber FROM biblio b LEFT JOIN items i ON (i.biblionumber=b.biblionumber)

# **************************************** IMPORTANT ************************************************************


def execute_query(sql_query):
    '''
    Helper Function that takes a SQL query and returns the executed output
    '''
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd=keyconfig.password,
        db="library"
    )
    cur = db.cursor()

    try:
        cur.execute(sql_query)
        return cur.fetchall()
    except MySQLdb.Error as e:
        print(e)
        return 'Error'

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
            messages.warning(request, 'Invalid Credentials')
            print(request.META.get('HTTP_REFERER'))
            return redirect(request.META.get('HTTP_REFERER'))
            return JsonResponse({'message':'The credentials are wrong'})

def logout_view(request):
    logout(request)
    return redirect('portal:login')

@login_required
def profile(request):
    try:
        user = request.user
        return render(request, 'portal/profile.html', {'name':user.username.capitalize()})
    except Exception as unknown_exception:
        return JsonResponse({'message':unknown_exception})

@login_required
def report_types(request):
    '''
    Display the different types of reports, and a live search bar to search for books.
    Django-autocomplete-light has been used for the search bar
    '''
    form = ReservesForm()
    return render(request, 'portal/types.html', {'form':form})

class CirculationReport(View):
    '''
    Generate Date-wise circulation report
    '''
    # User must be logged in to access this view

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'portal/circulation.html')

    @method_decorator(login_required)
    def post(self, request):
        data = request.POST

        from_timestamp = '{} 00:00:01'.format(data['from_date'])
        to_timestamp = '{} 23:59:59'.format(data['to_date'])


        sql_query='''
        (SELECT concat( bib.title, ' ', ExtractValue((
                SELECT metadata
                FROM biblio_metadata b2
                WHERE bib.biblionumber = b2.biblionumber),
                  '//datafield[@tag="245"]/subfield[@code="b"]') ) AS book_title,
            bib.author AS book_author, it.barcode,
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
        SELECT concat( bib.title, ' ', ExtractValue((
                SELECT metadata
                FROM biblio_metadata b2
                WHERE bib.biblionumber = b2.biblionumber),
                  '//datafield[@tag="245"]/subfield[@code="b"]') ),
            bib.author, it.barcode,
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
            'Full Title of the book',
            'Author',
            'Barcode (Accession Number)',
            'Patron Name',
            'Membership Number',
            'Email ID',
            'Phone number',
            'Issue Date',
            'Due date',
            'Return Date'
        ]

        count=0 #To count the total number of entries

        values = []
        for row in execute_query(sql_query):
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

        return render(request, 'portal/circulation_reoprt.html', context)

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

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salted,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(text))
f = fsociety(key)


@login_required
def checked_out(request):
    # To return all the books that are currently checked out

    sql_query = '''
        SELECT concat( biblio.title, ' ', ExtractValue((
                SELECT metadata
                FROM biblio_metadata b2
                WHERE biblio.biblionumber = b2.biblionumber),
                  '//datafield[@tag="245"]/subfield[@code="b"]') ) AS book_title,
            biblio.author AS book_author,
            items.barcode,
            TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) )AS patron_name,
            borrowers.cardnumber,
            borrowers.email,
            issues.issuedate AS issuedate,
            issues.date_due AS duedate
        FROM issues
        LEFT JOIN borrowers ON borrowers.borrowernumber = issues.borrowernumber
        LEFT JOIN items ON items.itemnumber = issues.itemnumber
        LEFT JOIN biblio ON biblio.biblionumber = items.biblionumber
        WHERE EXISTS (
            SELECT * FROM statistics
            WHERE statistics.type='return'
            AND statistics.datetime > issues.issuedate)
        ORDER BY duedate
        '''

    total_books = Items.objects.filter(itype='C').count # itype 'C' means the items that are 'Circulated' and ignores the journals, etc.

    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):

        # Issues are present only for the books currently checked out.
        # If an issue exists, for an item that has been checked in or out anytime after the issue date, ignore that issue
        # Because that issue exists due to inconsistent data.
        # Because of shifting to Koha in february 2019

        issuedate = row[6].date() # Convert datetime to date, because datelastseen is date and not datetime
        barcode = row[2]
        duedate = row[7]

        item = Items.objects.get(barcode = barcode)
        date_last_seen = item.datelastseen

        if date_last_seen > issuedate:
            pass
        else:
            issuedate = row[6]
            row = list(row)
            if duedate > issuedate:
                diff = (duedate - issuedate)
                remark = "Time Left for Due date: {time}".format(time=str(diff))
            else:
                diff = ( issuedate - duedate)

                remark = "{days} Overdue".format(days=str(diff))
            row.append(remark)
            values.append(row)
            count+=1

    headings = [
        'Title of the book',
        'Author',
        'Barcode (Accession Number)',
        'Patron Name',
        'Membership Number',
        'Email ID',
        'Issue Date',
        'Due date',
        'Remarks'
    ]

    context = {
        'count':count,
        'total':total_books,
        'values':values,
        'headings':headings,
        'report_type':'Circulation Report - Books currently checked out'
    }

    return render(request, 'portal/circulation_reoprt.html', context)

@login_required
def inactive_patrons(request):
    sql_query='''
        SELECT TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) ),
        borrowers.cardnumber, borrowers.categorycode, borrowers.email,
        DATEDIFF(NOW(), borrowers.dateenrolled) inactive_days
        FROM borrowers
        WHERE NOT EXISTS (
            SELECT borrowernumber FROM statistics
            WHERE borrowers.borrowernumber = borrowernumber)
        ORDER BY inactive_days DESC
        '''

    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):
        count+=1
        row = list(row)
        inactive_days = row[4]
        row[4] = "Inactive since {} days".format(inactive_days)
        values.append(row)

    headings = [
        'Patron Name',
        'Membership Number',
        'Category Code',
        'Email ID',
        'Remarks'
    ]
    total_patrons = Borrowers.objects.all().count()
    context = {
        'count':count,
        'total': total_patrons,
        'values':values,
        'headings':headings,
        'report_type':'Circulation Report - Inactive Patrons'
    }

    return render(request, 'portal/circulation_reoprt.html', context=context)

@login_required
def inactive_books(request):
    sql_query='''
            SELECT concat( biblio.title, ' ', ExtractValue((
                    SELECT metadata
                    FROM biblio_metadata b2
                    WHERE biblio.biblionumber = b2.biblionumber),
                      '//datafield[@tag="245"]/subfield[@code="b"]') ) AS book_title,
            biblio.author, items.barcode
            FROM biblio, items
            WHERE NOT EXISTS (
                SELECT itemnumber FROM statistics
                WHERE items.itemnumber = itemnumber)
            AND biblio.biblionumber=items.biblionumber
            AND items.itype = 'C';
            '''
    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):
        count+=1
        values.append(row)

    headings = [
        'Book title',
        'Book author',
        'Book barcode (Accession Number)',
    ]

    context = {
        'count':count,
        'values':values,
        'headings':headings,
        'report_type':'Circulation Report - Inactive Books'
    }

    return render(request, 'portal/circulation_reoprt.html', context=context)


class Search(View):

    def get(self, request):
        # Do not delete this function
        search_text = request.GET.get('search_txt', "$#@%^")
        items = Items.objects.filter(biblionumber__title__icontains=search_text)
        results = []
        for item in items:
            results.append(item.biblionumber.title)
        resp = json.dumps(results)
        print(resp)
        return HttpResponse(resp, content_type='application/json')

@login_required
def holds_waiting(request):
    if request.POST['type'] == 'waiting':
        # sql_query='''
        #         SELECT
        #             TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) ),
        #             borrowers.email, borrowers.cardnumber,
        #             items.barcode, biblio.title, reserves.reservedate
        #         FROM reserves
        #         LEFT JOIN borrowers USING (borrowernumber)
        #         LEFT JOIN items USING (itemnumber)
        #         LEFT JOIN biblio ON (reserves.biblionumber = biblio.biblionumber)
        #         WHERE
        #             (reserves.itemnumber IS NOT NULL
        #             AND NOT EXISTS(SELECT issue_id FROM issues WHERE items.itemnumber = issues.itemnumber)
        #             )
        #             OR
        #             (reserves.itemnumber IS NULL
        #             AND EXISTS(
        #                 SELECT itemnumber FROM items i2 WHERE i2.biblionumber=reserves.biblionumber
        #                 AND NOT EXISTS(
        #                     SELECT issue_id FROM issues iss WHERE iss.itemnumber=i2.itemnumber
        #                     )
        #                 )
        #             )
        #         '''
        report_type = 'Circulation Report - Holds Waiting'

        # SQL Query provided by koha devel mailing list
        sql_query = '''
        SELECT TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) ),
        borrowers.email, borrowers.cardnumber,
        IF(it1.barcode IS NOT NULL, it1.barcode, ""), biblio.title, reserves.reservedate
         FROM reserves
         LEFT JOIN borrowers USING (borrowernumber)
         LEFT JOIN biblio USING (biblionumber)
         LEFT JOIN items AS it1 USING (itemnumber)
         LEFT JOIN issues AS iss1 USING (itemnumber)
         LEFT JOIN items AS it2 ON (reserves.biblionumber = it2.biblionumber)
         LEFT JOIN issues AS iss2 ON(it2.itemnumber = iss2.itemnumber)
        WHERE iss1.date_due IS NULL AND iss2.date_due IS NULL'''

        headings = [
            'Patron Name',
            'Patron email',
            'Patron membership number',
            'Book barcode (Accession Number)',
            'Book title',
            'Reserve Date'
        ]

    elif request.POST['type'] == 'queue':
        # Doubt in SQL query. Rectify this.
        sql_query='''
                SELECT
                    TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) ) AS full_name,
                    borrowers.email, borrowers.cardnumber,
                    items.barcode, biblio.title, reserves.reservedate,
                    If (reserves.priority=1 AND issues.date_due IS NOT NULL, issues.date_due,
                        IF( priority=1 AND MIN(is2.date_due) IS NOT NULL, MIN(is2.date_due), "Not Available")
                    )
                FROM reserves
                LEFT JOIN borrowers USING (borrowernumber)
                LEFT JOIN items USING (itemnumber)
                LEFT JOIN biblio ON (reserves.biblionumber = biblio.biblionumber)
                LEFT JOIN issues USING (itemnumber)
                LEFT JOIN items AS it2 ON (it2.biblionumber = biblio.biblionumber)
                LEFT JOIN issues AS is2 ON (is2.itemnumber = it2.itemnumber)
                WHERE
                    (reserves.itemnumber IS NOT NULL
                    AND EXISTS(SELECT issue_id FROM issues is1 WHERE items.itemnumber = issues.itemnumber)
                    )
                    OR
                    (reserves.itemnumber IS NULL
                    AND NOT EXISTS(
                        SELECT itemnumber FROM items i2 WHERE i2.biblionumber=reserves.biblionumber
                        AND NOT EXISTS(
                            SELECT issue_id FROM issues is2 WHERE is2.itemnumber=i2.itemnumber
                            )
                        )
                    )
                GROUP BY biblio.biblionumber, borrowers.borrowernumber, items.barcode, reserves.reservedate, issues.issue_id, reserves.priority
                ORDER BY reservedate
                '''

        report_type = 'Circulation Report - Holds Queue'

        headings = [
            'Patron Name',
            'Patron email',
            'Patron membership number',
            'Book barcode (Accession Number)',
            'Book title',
            'Reserve Date',
            'Remarks'
        ]

    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):
        row = list(row)
        count+=1
        if request.POST['type'] == 'queue' and row[-1] != "Not Available":
            row[-1] = "Will be available on " + row[-1]
        values.append(row)



    context = {
        'count':count,
        'values':values,
        'headings':headings,
        'report_type':'Circulation Report - Holds Waiting'
    }

    return render(request, 'portal/circulation_reoprt.html', context=context)

class BookAutocomplete(autocomplete.Select2QuerySetView):
    #Using Django-autocomplete library

    def get_queryset(self):
        items = Items.objects.filter(itype='C').order_by('itemnumber')
        print("Helloiui")
        items_list = []
        if self.q:
            start = self.q
            # Optimized sql query for efficient search of books. Reduced the seach time by around 10-12 seconds.
            sql_query =f'''
                SELECT items.itemnumber, concat( b.title, ' ', ExtractValue((
                    SELECT metadata
                    FROM biblio_metadata b2
                    WHERE b.biblionumber = b2.biblionumber),
                      '//datafield[@tag="245"]/subfield[@code="b"]') ) AS 'booktitle' FROM biblio b, items
                    WHERE b.biblionumber=items.biblionumber AND
                    (
                        b.title LIKE CONCAT('{start}', '%%')
                        OR
                        '{start}' LIKE CONCAT(b.title, '%%')
                    )
                    HAVING booktitle REGEXP '^{start}'
                  '''
            items_list = items.raw(sql_query)
            return items_list
            # items = items.annotate(full_name = Concat(
            #     'biblionumber__title',
            #     Value(' '),
            #     XMLExtractValue('biblionumber__bibliometadata__metadata','//datafield[@tag="245"]/subfield[@code="b"]') )
            #     )
            # items_list = items.filter(full_name__istartswith=self.q)
        return items

class VendorAutocomplete(autocomplete.Select2QuerySetView):
    #Using Django-autocomplete library

    def get_queryset(self):
        vendors = Aqbooksellers.objects.all().order_by('name')

        vendors_list = []
        if self.q:
            vendors_list = vendors.filter(name__icontains=self.q)
            return vendors_list

        return vendors

@login_required
def book_detail(request):
    '''
    Display details of a book
    '''
    if request.method == 'POST':
        data = request.POST
        try:
            itemnumber = data['itemnumber']
            item = Items.objects.get(itemnumber=itemnumber)
            biblio = item.biblionumber

            context = {
                'title': item.full_title,
                'author': biblio.author,
                'barcode': item.barcode,
                'call_number': item.itemcallnumber
            }
            return render(request, 'portal/book_detail.html', context)

        except KeyError:
            return JsonResponse({'message':'Invalid Request'})
    else:
        return JsonResponse({'message':'Invalid Request'})


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


class NoDue(View):

    @method_decorator(login_required)
    def get(self, request):
        '''
        Input the IC number of members.
        '''
        # Get all the addressee
        addressee_list = Addressee.objects.all()
        context = {'addressee_list':addressee_list}
        return render(request, 'portal/no_due_input.html', context=context)

    @method_decorator(login_required)
    def post(self, request):
        '''
        Get the IC numbers and generate corresponding No-Due Certificate
        '''

        ic_numbers = request.POST.getlist('ic_no')
        if not ic_numbers:
            messages.error(request,'Please Enter IC numbers')
            return redirect('portal:no_due')

        invalid = []
        valid_patrons = []

        # Validate if all IC numbers are valid
        # If invalid, make a list of invalid IC numbers and display an error message
        for ic_number in ic_numbers:
            try:
                # IC numbers are stored in database in a column called sort1
                if not ic_number:
                    continue
                borrower = Borrowers.objects.get(sort1=ic_number)
                valid_patrons.append(borrower)
            except:
                invalid.append(ic_number)

        if invalid:
            context = {
                'invalid': invalid
            }
            messages.error(request,'Following IC number(s) is/are invalid: {}'.format(invalid))
            return redirect('portal:no_due')

        if not valid_patrons:
            return JsonResponse({'message': 'Please Enter IC numbers'})

        all_books = []
        all_fines=[]
        failed_patrons = []

        temp_patrons = valid_patrons.copy()
        for patron in temp_patrons:
            # Filter the Issues by the patron
            print(patron.surname)
            issues = Issues.objects.filter(borrowernumber = patron)
            accountlines = Accountlines.objects.filter(borrowernumber = patron)
            balance = accountlines.aggregate(Sum('amountoutstanding'))['amountoutstanding__sum']

            # Checking if user's balance is positive or negative
            if balance:
                if balance < 0:
                    fine = 0
                else:
                    fine = balance
            else:
                fine = 0

            if issues or fine:
                valid_patrons.remove(patron)
                failed_patrons.append(patron)

                items = [issue.itemnumber for issue in issues]
                all_books.append(items) # Will apend empty list if there is no issue

                all_fines.append(fine) # Will append None is no fine exists


        # Creating a python zip for patrons and their respective fines and issued books
        failed_data = zip(
            failed_patrons,
            all_books,
            all_fines
        )
        print(failed_data)

        date = datetime.date.today()
        print(failed_patrons)
        if failed_patrons:
            for data_value in failed_data:
                message = "No-Due Certificate could not be generated for the following patron "
                message += "{name} - {ic} : ".format(name=data_value[0].surname, ic=data_value[0].sort1)
                if data_value[1]:
                    message+= "Following books are issued in his/her name - "
                    for book in data_value[1]:
                        message += book.full_title + "- " + str(book.barcode) + "| "
                if data_value[2]:
                    message += "Total fine: {}".format( data_value[2] ) + " "
                messages.info(request, message)

        # Get the report number by incrementing the maximum report number by 1
        max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
        if max_report_no:
            report_number = max_report_no + 1
        else:
            report_number = 1

        ref_number_list = []

        # Get the maximum reference number
        max_ref_no = PatronInfo.objects.aggregate(Max('ndc_ref_number'))['ndc_ref_number__max']
        # We are starting reference numbers from 3001, as this software will be used after 3000 reports
        if not max_ref_no or max_ref_no < 3001:
            refer_number = 3001
        else:
            refer_number = max_ref_no + 1

        for ref_no in range(refer_number, refer_number + len(valid_patrons)):
            ref_number_list.append(ref_no)

        # Get the ref_no/date
        try:
            ref_no_date_list = request.POST.getlist('ref_no_date')
        except KeyError:
            messages.info(request,'Enter the Ref no. / Date')
            return redirect('portal:no_due')

        valid_data = zip( valid_patrons, ref_number_list, ref_no_date_list )

        if not valid_patrons:
            display = False
        else:
            display = True
        # Get the chosen addressee
        try:
            addressee_id = request.POST['addressee']
            addressee = Addressee.objects.get(id=addressee_id)
        except KeyError:
            messages.error(request, 'Please choose Addressee')
            return redirect('portal:no_due')
        except AttributeError:
            return JsonResponse({'message':'Invalid Addressee'})


        context = {
            'report_number': report_number,
            'valid_data':valid_data,
            'report_number': report_number,
            'date':date,
            'failed_data':failed_data,
            'addressee':addressee,
            'display': display
        }

        print(context)

        patrons = [patron.borrowernumber for patron in valid_patrons]
        data = {
            'patrons': patrons,
            'ref_numbers': ref_number_list,
            'report_number': report_number,
            'ref_no_date_list': ref_no_date_list,
            'addressee':addressee_id
        }

        # Save the data in session to use while storing the no due in database
        request.session['saved'] = data

        return render(request, 'portal/no_due.html', context)

@login_required
def no_due_save(request):
    '''
    View to save the information of No Due CERTIFICATE
    '''
    if not request.session['saved']:
        return JsonResponse({"message": "Invalid Request"})
    data = request.session['saved']
    try:
        patrons_ids = data['patrons']
        ref_no_date_list = data['ref_no_date_list']
        addressee_id = data['addressee']
        addressee = Addressee.objects.get(id=addressee_id)

        # Get the report number by incrementing the maximum report number by 1
        max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
        if max_report_no:
            report_number = max_report_no + 1
        else:
            report_number = 1

        ref_number_list = []

        # Get the maximum reference number
        max_ref_no = PatronInfo.objects.aggregate(Max('ndc_ref_number'))['ndc_ref_number__max']
        # We are starting reference numbers from 3001, as this software will be used after 3000 reports
        if not max_ref_no or max_ref_no < 3001:
            refer_number = 3001
        else:
            refer_number = max_ref_no + 1

        for ref_no in range(refer_number, refer_number + len(patrons_ids)):
            ref_number_list.append(ref_no)

    except KeyError:
        return JsonResponse({'message': "Invalid Request"})

    # Saving the Patrons info and NDC in the database
    patrons=[]
    for patron_id, ref_number, ref_no_date in zip(patrons_ids, ref_number_list, ref_no_date_list):
        borrower = Borrowers.objects.get(borrowernumber=patron_id)
        pi = PatronInfo.objects.create(
            name = borrower.full_name,
            ic_number = borrower.sort1,
            division = borrower.address,
            mem_number = borrower.cardnumber,
            ndc_ref_number = ref_number,
            ref_no_date = ref_no_date
            )
        patrons.append(pi)

    ndc = NoDueCertificate.objects.create(
    report_number = report_number,
    date=datetime.date.today(),
    addressee = addressee
    )
    for patron in patrons:
        ndc.patrons.add(patron)
        ndc.save()

    messages.success(request, 'Data successfully saved')

    patrons = [Borrowers.objects.get(borrowernumber=id) for id in patrons_ids]
    valid_data = zip( patrons, ref_number_list, ref_no_date_list )

    context = {
        'valid_data':valid_data,
        'report_number': report_number,
        'date':datetime.date.today(),
        'addressee': addressee,
        'message': f.decrypt(message).decode()
    }

    return render(request,'portal/no_due_final.html', context)

class NoDueNonMembers(View):
    '''
    Generate No Due Certificate for people who do not exist in the library database
    '''

    @method_decorator(login_required)
    def get(self, request):
        # Get all the addressee
        addressee_list = Addressee.objects.all()
        context = {'addressee_list':addressee_list}
        return render(request, 'portal/non_members_input.html', context=context)

    @method_decorator(login_required)
    def post(self,request):
        try:
            data = request.POST
            print(data)
            ic_number_list = data.getlist('ic_no')
            name_list = data.getlist('name')
            div_list = data.getlist('div')
            ref_no_date_list = data.getlist('ref_no_date')

            # Remove null values from the list
            index = 0
            for ic,name,div,ref_no_date in zip(ic_number_list.copy(), name_list.copy(), div_list.copy(), ref_no_date_list.copy()):
                if not (ic or name or div or ref_no_date):
                    ic_number_list.pop(index)
                    name_list.pop(index)
                    div_list.pop(index)
                    ref_no_date_list.pop(index)
                else:
                    index+=1

            addressee_id = request.POST['addressee']
            addressee = Addressee.objects.get(id=addressee_id)

            # Get the report number by incrementing the maximum report number by 1
            max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
            if max_report_no:
                report_number = max_report_no + 1
            else:
                report_number = 1

            ref_number_list = []

            # Get the maximum reference number
            max_ref_no = PatronInfo.objects.aggregate(Max('ndc_ref_number'))['ndc_ref_number__max']
            # We are starting reference numbers from 3001, as this software will be used after 3000 reports
            if not max_ref_no or max_ref_no < 3001:
                refer_number = 3001
            else:
                refer_number = max_ref_no + 1

            for ref_no in range(refer_number, refer_number + len(name_list)):
                ref_number_list.append(ref_no)

            valid_data = zip(
                name_list,
                ic_number_list,
                div_list,
                ref_number_list,
                ref_no_date_list
            )
            date = datetime.date.today()

            context = {'date':date, 'valid_data':valid_data, 'report_number': report_number,'addressee':addressee}

            data = {
                'names':name_list,
                'ic_numbers': ic_number_list,
                'divs': div_list,
                'ref_number_list': ref_number_list,
                'ref_no_date_list': ref_no_date_list,
                'addressee': addressee.id,
                'report_number': report_number
            }
            request.session['saved'] = data
            return render(request, 'portal/non_member.html', context=context)


        except KeyError:
            messages.warning(request, 'Please enter all details')
            return redirect('portal:no_due_non_members')

@login_required
def non_member_save(request):
    '''
    View to save the information of No Due CERTIFICATE - Non members
    '''
    if not request.session['saved']:
        return JsonResponse({"message": "Invalid Request"})
    data = request.session['saved']
    try:
        names = data['names']
        ic_numbers = data['ic_numbers']
        divs = data['divs']
        ref_no_date_list = data['ref_no_date_list']
        addressee_id = data['addressee']
        addressee = Addressee.objects.get(id=addressee_id)

        # Get the report number by incrementing the maximum report number by 1
        max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
        if max_report_no:
            report_number = max_report_no + 1
        else:
            report_number = 1

        ref_number_list = []

        # Get the maximum reference number
        max_ref_no = PatronInfo.objects.aggregate(Max('ndc_ref_number'))['ndc_ref_number__max']
        # We are starting reference numbers from 3001, as this software will be used after 3000 reports
        if not max_ref_no or max_ref_no < 3001:
            refer_number = 3001
        else:
            refer_number = max_ref_no + 1

        for ref_no in range(refer_number, refer_number + len(names)):
            ref_number_list.append(ref_no)

    except KeyError:
        return JsonResponse({'message': "Invalid Request"})

    data_zip = zip(
        names,
        ic_numbers,
        divs,
        ref_number_list,
        ref_no_date_list
    )
    patrons = []
    for name, ic_number, division, ref_number, ref_no_date in data_zip:
        pi = PatronInfo.objects.create(
            name = name,
            ic_number = ic_number,
            division = division,
            mem_number = 'Non. Mem.',
            ndc_ref_number = ref_number,
            ref_no_date = ref_no_date,
        )
        patrons.append(pi)

    ndc = NoDueCertificate.objects.create(
        report_number = report_number,
        date=datetime.date.today(),
        addressee = addressee
        )

    for patron in patrons:
        ndc.patrons.add(patron)
        ndc.save()

    messages.success(request, 'Data successfully saved')

    valid_data = zip(
        names,
        ic_numbers,
        divs,
        ref_number_list,
        ref_no_date_list
    )
    date = datetime.date.today()

    context = {'date':date, 'valid_data':valid_data, 'report_number': report_number,'addressee':addressee}

    return render(request,'portal/non_member_final.html', context)

class NDCArchive(View):

    @method_decorator(login_required)
    def get(self, request):
        ndc_report_numbers = NoDueCertificate.objects.all().order_by('-report_number').values('full_ref').distinct()
        full_ref_list = [rn['full_ref'] for rn in ndc_report_numbers]
        dates = [NoDueCertificate.objects.filter(full_ref=ref)[0].date for ref in full_ref_list]
        ndcs = zip(full_ref_list, dates)
        return render(request, 'portal/ndc_archive.html', {'ndcs':ndcs})

    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        try:
            full_ref = data['ndc_rn']
            ndc = NoDueCertificate.objects.get(full_ref=full_ref)
            date = ndc.date
            addressee = ndc.addressee
            patrons = ndc.patrons.all()
            report_number = ndc.report_number

            context = {
                'ndc': ndc,
                'patrons': patrons,
                'date': date,
                'report_number': report_number,
                'addressee': addressee
            }
            return render(request, 'portal/ndc_archive_print.html', context)
        except (KeyError, AttributeError) as e:
            print(e)
            return JsonResponse({'message': 'Invalid Request'})

class FineReportsSummary(View):

    @method_decorator(login_required)
    def get(self, request):
        # Get all the addressee
        addressee_list = Addressee.objects.all()

        # Available Units:
        units = [
            'AERB',
            'BARCF',
            'BHAVINI',
            'DPS'
            'GSO',
            'IGCAR',
            'MAPS',
            'PRP',
        ]
        return render(request, 'portal/fine_input.html', {"addressee_list": addressee_list, 'units':units})

    @method_decorator(login_required)
    def post(self, request):
        try:
            data = request.POST
            from_date = data['from_date']
            to_date = data['to_date']
            addressee_id = data['addressee']
            unit = data['unit']
            if unit == "BHAVINI":
                unit_substr = 'BH'
            else:
                unit_substr = unit[0]
            try:
                addressee = Addressee.objects.get(id=addressee_id)
            except AttributeError:
                return JsonResponse({"Message": "Invalid Addressee"})

            # Raw SQL query to get details of all fines
            sql_query = '''
                SELECT emp AS 'Employee Name',icno AS 'IC No', divi AS 'Division', pat AS 'Membership No.', sum(tfa) AS 'Total Fine Amount' FROM (SELECT
                   b.cardnumber as 'pat',b.address as 'divi', TRIM(LEADING '0' FROM if(substr(b.sort1,1,2)='BH',substr(b.sort1,3),substr(b.sort1,2))) as 'icno', b.surname as 'emp',  Sum(round(a.amountoutstanding,2)) as 'tfa'
                FROM accountlines a
                  LEFT JOIN borrowers b ON ( b.borrowernumber = a.borrowernumber )
                  LEFT JOIN items i ON ( a.itemnumber = i.itemnumber )
                  LEFT JOIN biblio bib ON ( i.biblionumber = bib.biblionumber )
                  LEFT JOIN ( SELECT * FROM issues UNION SELECT * FROM old_issues ) ni ON ( ni.itemnumber = i.itemnumber AND ni.borrowernumber = a.borrowernumber )
                WHERE
                    a.amountoutstanding > 0 and ni.returndate is not null AND Date(ni.returndate) BETWEEN \'{from_date}\' AND \'{to_date}\'
                    AND b.sort1 LIKE \'{unit}%\'
                GROUP BY a.description, b.cardnumber, b.sort1, b.surname, ni.timestamp, b.address
                ORDER BY b.surname,  ni.timestamp DESC) as res1 group by pat, icno, emp, divi order by icno, emp
                '''.format(from_date=from_date, to_date=to_date, unit=unit_substr)

            count = 0 # To count the total number of rows
            values = []

            ref_number_list = []
            names = []
            ic_nos = []
            divisions = []
            mem_nos = []
            fines = []

            for row in execute_query(sql_query):
                count+=1
                values.append(row)

                names.append(row[0])
                ic_nos.append(row[1])
                divisions.append(row[2])
                mem_nos.append(row[3])
                fines.append(float(row[4]))

            # Get the report number by incrementing the maximum report number by 1
            f = FineReportSummary()
            reports = FineReportSummary.objects.all()
            max_report_no = reports.aggregate(Max('report_number'))['report_number__max']
            if max_report_no:
                report_number = max_report_no + 1
            else:
                report_number = 1

            # Get the maximum reference number
            max_ref_no = PatronInfo.objects.aggregate(Max('fine_ref_number'))['fine_ref_number__max']
            # We are starting reference numbers from 3001, as this software will be used after 3000 reports
            if not max_ref_no or max_ref_no < 3001:
                refer_number = 3001
            else:
                refer_number = max_ref_no + 1


            for ref_no in range(0,count):
                ref_number_list.append(refer_number)
                refer_number += 1

            valid_data = zip(values, ref_number_list)

            context = {
                'report_number': report_number,
                'valid_data': valid_data,
                'addressee': addressee,
                'date': datetime.date.today(),
                'unit': unit,
                'from_date': datetime.datetime.strptime(from_date, "%Y-%M-%d").strftime("%d-%m-%Y"),
                'to_date': datetime.datetime.strptime(to_date, "%Y-%M-%d").strftime("%d-%m-%Y")
            }
            print(fines)
            data = {
                'names': names,
                'ic_nos':ic_nos,
                'divisions':divisions,
                'mem_nos':mem_nos,
                'fines':fines,
                'addressee_id': addressee.id,
                'unit': unit,
                'from_date': from_date,
                'to_date': to_date
            }
            request.session['saved'] = data

            return render(request, 'portal/fine_report.html', context=context)

        except KeyError:
            return JsonResponse({'message': "Invalid Request"})
        except MySQLdb.Error as e:
            print(e)
            return JsonResponse({"message": "Error in sql query"})

@login_required
def fine_report_summary_save(request):
    # Extract data saved in django sessions
    data = request.session['saved']
    names = data['names']
    ic_nos = data['ic_nos']
    divisions = data['divisions']
    mem_nos = data['mem_nos']
    fines = data['fines']
    addressee_id = data['addressee_id']
    addressee = Addressee.objects.get(id=addressee_id)
    unit = data['unit']
    from_date = data['from_date']
    to_date = data['to_date']
    # Get the report number by incrementing the maximum report number by 1
    reports = FineReportSummary.objects.all()
    max_report_no = reports.aggregate(Max('report_number'))['report_number__max']
    if max_report_no:
        report_number = max_report_no + 1
    else:
        report_number = 1

    # Get the maximum reference number
    max_ref_no = PatronInfo.objects.aggregate(Max('fine_ref_number'))['fine_ref_number__max']
    # We are starting reference numbers from 3001, as this software will be used after 3000 reports
    if not max_ref_no or max_ref_no < 3001:
        refer_number = 3001
    else:
        refer_number = max_ref_no + 1

    ref_number_list = []
    for ref_no in range(0,len(names)):
        ref_number_list.append(refer_number)
        refer_number += 1

    data_zip = zip(names, ic_nos, divisions, mem_nos, fines, ref_number_list)

    patrons = []
    for name, ic_no, division, mem_no, fine, ref_number in data_zip:
        pi = PatronInfo.objects.create(
            name = name,
            ic_number = ic_no,
            division = division,
            mem_number = mem_no,
            fine_ref_number = ref_number,
            fine=fine
        )
        patrons.append(pi)

    fr = FineReportSummary.objects.create(
        report_number = report_number,
        date = datetime.date.today(),
        addressee = addressee,
        unit = unit,
        from_date = from_date,
        to_date = to_date
    )
    fr.patrons.add(*patrons)

    valid_data = zip(names, ic_nos, divisions, mem_nos, fines, ref_number_list )
    context = {
        'valid_data': valid_data,
        'date': datetime.date.today(),
        'report_number': report_number,
        "addressee": addressee,
        'unit': unit,
        'from_date': from_date,
        'to_date': to_date
        }

    messages.success(request, 'Successfully saved')
    return render(request, 'portal/fine_report_final.html', context=context)

class FineSummaryArchive(View):
    @method_decorator(login_required)
    def get(self, request):
        fine_summary_reports = FineReportSummary.objects.all().order_by('-report_number')
        return render(request, 'portal/fine_archive_input.html', context = {'fine_summary_reports': fine_summary_reports})

    @method_decorator(login_required)
    def post(self, request):
        try:
            data = request.POST
            report_id = data['report_id']
            fine_summary = FineReportSummary.objects.get(id=report_id)
            patrons = fine_summary.patrons.all()
            context = {'patrons': patrons, 'report': fine_summary}
            return render(request, 'portal/fine_archive_print.html', context=context)

        except KeyError:
            return JsonResponse({"message": "invalid report chosen"})

class FineReport(View):

    @method_decorator(login_required)
    def get(self, request):
        # Get all the addressee
        addressee_list = Addressee.objects.all()

        # Available Units:
        units = [
            'AERB',
            'BARCF',
            'BHAVINI',
            'DPS'
            'GSO',
            'IGCAR',
            'MAPS',
            'PRP',
        ]
        return render(request, 'portal/fine_report_input.html', {"addressee_list": addressee_list, 'units':units})

    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        from_date = data['from_date']
        to_date = data['to_date']
        unit = data['unit']
        if unit == 'BHAVINI':
            unit_substr = "BH"
        else:
            unit_substr = unit[0]
        sql_query='''
            SELECT
                b.cardnumber as 'Membership No.',TRIM(LEADING '0' FROM if(substr(b.sort1,1,2)='BH',substr(b.sort1,3),substr(b.sort1,2))) as 'IC No.',
                TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) ),
                concat( bib.title, ' ', ExtractValue((
                        SELECT metadata
                        FROM biblio_metadata b2
                        WHERE bib.biblionumber = b2.biblionumber),
                          '//datafield[@tag="245"]/subfield[@code="b"]') ) AS book_title,
                i.barcode as 'Accession Number',
                ni.issuedate as 'Issue Date', ni.date_due as 'Due Date',
                ni.returndate AS 'Return Date' , round(a.amountoutstanding,2) as 'Fine Amount'
            FROM accountlines a
              LEFT JOIN borrowers b ON ( b.borrowernumber = a.borrowernumber )
              LEFT JOIN items i ON ( a.itemnumber = i.itemnumber )
              LEFT JOIN biblio bib ON ( i.biblionumber = bib.biblionumber )
              LEFT JOIN ( SELECT * FROM issues UNION SELECT * FROM old_issues ) ni ON ( ni.itemnumber = i.itemnumber AND ni.borrowernumber = a.borrowernumber )
            WHERE
                a.amountoutstanding > 0 and ni.returndate is not null and DATE (ni.returndate)  BETWEEN \'{from_date}\' AND \'{to_date}\'
                AND b.sort1 LIKE \'{unit}%\'
            GROUP BY a.description, b.cardnumber, b.sort1, b.surname,b.firstname, bib.title, i.barcode, ni.issuedate, ni.date_due, ni.returndate, ni.date_due, a.amountoutstanding, ni.timestamp, bib.biblionumber
            ORDER BY b.sort1, b.surname, ni.timestamp DESC
        '''.format(from_date=from_date, to_date=to_date, unit=unit_substr)

        count=0 #To count the total number of entries

        values = []
        for row in execute_query(sql_query):
            count+=1
            row=list(row)
            # Replace Null with empty string for Return date
            if not row[-2]:
                row[-2] = " "
            values.append(row)

        headings = [
            'Membership Number',
            'IC Number',
            'Employee Name',
            'Book Title',
            'Accession Number(Barcode)',
            'Issue Date',
            'Due Date',
            'Return Date',
            'Fine Amount'
        ]

        context = {
            'count':count,
            'values':values,
            'headings':headings,
            'report_type':'Patron Report - Fines',
            'from_date': from_date,
            'to_date': to_date,
            'unit': unit
        }

        return render(request, 'portal/circulation_reoprt.html', context=context)

class VendorOrders(View):

    @method_decorator(login_required)
    def get(self, request):
        form = AqBasketForm()
        return render(request, 'portal/vendor_orders.html', {'form':form})

    @method_decorator(login_required)
    def post(self, request):
        try:
            data = request.POST
            from_date = data['from_date']
            to_date = data['to_date']
            booksellerid = data['booksellerid']
            vendor = Aqbooksellers.objects.get(id=booksellerid)
            sql_query = '''
                        SELECT concat( biblio.title, ' ', ExtractValue((
                                    SELECT metadata
                                    FROM biblio_metadata b2
                                    WHERE biblio.biblionumber = b2.biblionumber),
                                      '//datafield[@tag="245"]/subfield[@code="b"]') ) AS book_title,
                                biblio.author,
                                biblioitems.publishercode,
                                ba.basketno,
                                ba.creationdate,
                                o.orderstatus,
                                borrowers.surname,
                                format(o.listprice,2) AS 'list price',
                                format(o.unitprice,2) AS 'actual price',
                                ba.basketno
                        FROM aqorders o
                        LEFT JOIN aqbasket ba USING (basketno)
                        LEFT JOIN aqbooksellers v ON (v.id = ba.booksellerid)
                        LEFT JOIN biblio USING (biblionumber)
                        LEFT JOIN biblioitems ON (biblioitems.biblionumber = biblio.biblionumber)
                        LEFT JOIN borrowers ON (borrowers.borrowernumber = ba.authorisedby)
                        WHERE o.entrydate BETWEEN \'{from_date}\' AND \'{to_date}\'
                        AND v.id = {vendor_id}
                        ORDER BY o.entrydate, o.orderstatus
                        '''.format(from_date=from_date, to_date=to_date, vendor_id=vendor.id)

            count=0 #To count the total number of entries

            values = []
            for row in execute_query(sql_query):
                count+=1
                row=list(row)
                values.append(row)

            headings = [
                'Book Title',
                'Author',
                'Publisher',
                'Basket Number',
                'Creation Date',
                'Order Status',
                'Authorised By',
                'List Price',
                'Actual Price',
                'Basket ID'
            ]

            context = {
                'count':count,
                'values':values,
                'headings':headings,
                'report_type':'Acquisition Report - DateWise requested items',
                'from_date': from_date,
                'to_date': to_date,
                'vendor': vendor
            }

            return render(request, 'portal/circulation_reoprt.html', context=context)

        except KeyError:
            return JsonResponse({'message': 'Invalid Request'})

@login_required
def overdue_orders(request):

    sql_query = '''
                SELECT concat( biblio.title, ' ', ExtractValue((
                            SELECT metadata
                            FROM biblio_metadata b2
                            WHERE biblio.biblionumber = b2.biblionumber),
                              '//datafield[@tag="245"]/subfield[@code="b"]') ) AS book_title,
                        biblio.author,
                        biblioitems.publishercode,
                        o.orderstatus,
                        borrowers.surname,
                        format(o.listprice,2) AS 'list price',
                        format(o.unitprice,2) AS 'actual price',
                        ba.basketno
                FROM aqorders o
                LEFT JOIN aqbasket ba USING (basketno)
                LEFT JOIN aqbooksellers v ON (v.id = ba.booksellerid)
                LEFT JOIN biblio USING (biblionumber)
                LEFT JOIN biblioitems ON (biblioitems.biblionumber = biblio.biblionumber)
                LEFT JOIN borrowers ON (borrowers.borrowernumber = ba.authorisedby)
                WHERE o.entrydate BETWEEN \'{from_date}\' AND \'{to_date}\'
                AND v.id = {vendor_id}
                ORDER BY o.entrydate, o.orderstatus
                '''.format(from_date=from_date, to_date=to_date, vendor_id=vendor.id)

    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):
        count+=1
        row=list(row)
        values.append(row)

    headings = [
        'Book Title',
        'Author',
        'Publisher',
        'Order Status',
        'Suggested By',
        'List Price',
        'Actual Price',
        'Basket ID'
    ]

    context = {
        'count':count,
        'values':values,
        'headings':headings,
        'report_type':'Acquisition Report - DateWise requested items',
        'from_date': from_date,
        'to_date': to_date,
        'vendor': vendor
    }

    return render(request, 'portal/circulation_reoprt.html', context=context)

@login_required
def suggested_books(request):
    sql_query = '''
                SELECT r.title 'Title',r.author 'Author', r.publishercode 'Publisher',r.copyrightdate 'Year', r.STATUS,
                TRIM(CONCAT(COALESCE(bb.firstname,""), " ",  COALESCE(bb.surname,"") ) ) 'Suggested By',
                r.quantity 'Quantity', r.price

                FROM suggestions r

                LEFT JOIN aqbudgets b ON r.budgetid=b.budget_id
                LEFT JOIN borrowers bb ON r.suggestedby=bb.borrowernumber

                WHERE STATUS LIKE 'ASKED'
                '''
    headings = [
        'Title',
        'Author',
        'Publisher',
        'Year',
        'Status',
        'Suggested By',
        'Quantity',
        'Price',
    ]
    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):
        values.append(row)

    context = {
        'headings': headings,
        'values': values,
        'report_type': 'Acquisition Report: Titles For Placing Orders'
    }

    return render(request, 'portal/circulation_reoprt.html', context)

@login_required
def overdue_orders_30(request):
    sql_query = '''
                SELECT
                    concat( biblio.title, ' ', ExtractValue((
                        SELECT metadata
                        FROM biblio_metadata b2
                        WHERE biblio.biblionumber = b2.biblionumber),
                          '//datafield[@tag="245"]/subfield[@code="b"]') ) AS title,
                    biblio.author,
                    biblioitems.publishercode,
                    biblioitems.publicationyear,
                    aqorders.entrydate,
                    aqbooksellers.name,
                    aqorders.orderstatus
                FROM
                    aqorders
                    LEFT JOIN biblio
                        USING (biblionumber)
                    LEFT JOIN biblioitems
                        USING (biblionumber)
                    LEFT JOIN aqinvoices
                        USING (invoiceid)
                    LEFT JOIN aqbudgets
                        USING (budget_id)
                    LEFT JOIN aqbasket
                        USING (basketno)
                    LEFT JOIN aqbooksellers
                        ON (aqbooksellers.id = aqbasket.booksellerid)
                WHERE
                    aqorders.ordernumber IS NOT NULL
                    AND aqorders.datecancellationprinted IS NULL
                    AND aqorders.datereceived IS NULL
                    AND aqorders.entrydate < DATE(DATE_SUB(NOW(), INTERVAL 30 DAY))
                ORDER BY aqbudgets.budget_name ASC
                '''
    headings = [
        'Book Name',
        'Author',
        'Publisher',
        'Year',
        'Entry Date',
        'Vendor',
        'Status',
    ]
    count=0 #To count the total number of entries

    values = []
    for row in execute_query(sql_query):
        count+=1
        values.append(row)

    context = {
        'count': count,
        'headings': headings,
        'values': values,
        'report_type': 'Acquisition Report: Overdue Notice (Order Placed > 30 days)'
    }

    return render(request, 'portal/circulation_reoprt.html', context)

class InvoiceRegister(View):
    @method_decorator(login_required)
    def get(self, request):
        form = AqBasketForm()
        return render(request, 'portal/invoice_register.html', {'form':form})


    @method_decorator(login_required)
    def post(self, request):
        try:
            data = request.POST
            booksellerid = data['booksellerid']
            from_date = data['from_date']
            to_date = data['to_date']
            vendor = Aqbooksellers.objects.get(id=booksellerid)

            sql_query = '''
                SELECT
                    aqbasket.basketname 'Basket Name',
                    invoice.invoicenumber 'Invoice Number',invoice.billingdate 'Bill Date',
                    round( SUM(
                        case
                            when invoice.shipmentcost IS NOT NULL THEN aqorders.unitprice_tax_included*aqorders.quantityreceived+invoice.shipmentcost
                            ELSE aqorders.unitprice_tax_included*aqorders.quantityreceived
                        END
                    ),2) 'Total Invoice Amount',
                    SUM(aqorders.discount) 'Discount', round(SUM(aqorders.tax_value_on_receiving),2),
                    invoice.closedate 'Invoice Close Date',SUM(aqorders.quantityreceived) 'Quantity Received'

                FROM aqbasket

                LEFT JOIN aqorders ON (aqorders.basketno = aqbasket.basketno)
                LEFT JOIN aqbooksellers vendor ON (vendor.id=aqbasket.booksellerid)
                LEFT JOIN aqinvoices invoice ON (invoice.invoiceid=aqorders.invoiceid)
                LEFT JOIN aqbudgets budget ON (budget.budget_id=aqorders.budget_id)
                LEFT JOIN biblio ON (biblio.biblionumber = aqorders.biblionumber)

                WHERE aqorders.orderstatus LIKE 'complete' AND vendor.id={vendor_id}

                GROUP BY aqorders.basketno, invoice.invoicenumber, invoice.billingdate,invoice.closedate

                ORDER BY vendor.name ASC'''.format(vendor_id=vendor.id)

            headings = [
                'Basket Name',
                'Invoice Number',
                'Bill Date',
                'Amount',
                'Discount',
                'GST',
                'Invoice Close Date',
                'Quantity Received'
            ]
            count=0 #To count the total number of entries

            values = []
            for row in execute_query(sql_query):
                count+=1
                values.append(row)

            context = {
                'vendor': vendor,
                'count': count,
                'values': values,
                'headings': headings,
                'report_type': 'Invoice Register'
            }
            return render(request, 'portal/circulation_reoprt.html', context)
        except Exception as e:
            print(e)


#####################################   SERIAL REPORTS        ##########################
class RecentArrivals(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'portal/recent_arrivals.html')

    @method_decorator(login_required)
    def post(self, request):
        try:
            data = request.POST
            from_date = data['from_date']
            to_date = data['to_date']
            # Source of SQL - https://wiki.koha-community.org/wiki/SQL_Reports_Library#Serial_reports
            sql_query = '''
                SELECT
                    concat( biblio.title, ' ', ExtractValue((
                    SELECT metadata
                    FROM biblio_metadata b2
                    WHERE biblio.biblionumber = b2.biblionumber),
                    '//datafield[@tag="245"]/subfield[@code="b"]') ) AS title,
                    IF( biblioitems.publishercode IS NOT NULL, biblioitems.publishercode, ""),
                    serial.subscriptionid,
                    serial.biblionumber,
                    serial.serialid,
                    serial.serialseq,
                    serial.planneddate,
                    IF(serial.publisheddate IS NOT NULL, serial.publisheddate, ""),
                    ExtractValue(biblio_metadata.metadata, '//datafield[@tag="310"]/subfield[@code="a"]') AS FREQUENCY
                    FROM serial, biblio_metadata, biblio
                    LEFT JOIN biblioitems USING (biblionumber)
                    WHERE serial.biblionumber = biblio.biblionumber AND serial.biblionumber=biblio_metadata.biblionumber  AND (STATUS)=2
                        AND DATE(planneddate) BETWEEN \'{from_date}\' AND \'{to_date}\'
                    ORDER BY serial.subscriptionid ASC
                '''.format(from_date=from_date, to_date=to_date)

            # Extracting frequency credit - koha-devel mailing list

            print(sql_query)
            headings = [
                'Title',
                'Publisher',
                'Subscription ID',
                'Biblionumber',
                'Serial ID',
                'Serial Seq',
                'Planned Date',
                'Published Date',
                'Frequency'
            ]
            count=0 #To count the total number of entries

            values = []
            for row in execute_query(sql_query):
                count+=1
                values.append(row)

            context = {
                'count': count,
                'values': values,
                'headings': headings,
                'report_type': f'Serial Report - Recent Arrivals [FROM: {from_date} TO: {to_date}]'
            }
            return render(request, 'portal/circulation_reoprt.html', context)
        except Exception as e:
            print(e)

class BarcodeCSV(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'portal/csv_upload.html')

    @method_decorator(login_required)
    def post(self, request):
        if not request.FILES['csv']:
            messages.warning(request,'No file uploaded')
            return redirect('portal:barcode_csv')


        csv_files = request.FILES.getlist('csv')

        # Checking if the files are in CSV format
        failure = 0
        for csv in csv_files:
            if not csv.name.endswith('.csv'):
                messages.warning(request, 'The file: \'{name}\' is not in CSV format.'.format(name=csv.name))
                failure = 1
        if failure:
            return redirect('portal:barcode_csv')

        barcodes = []
        status = []
        incorrect_count = correct_count =0
        for csv in csv_files:
            # Reading the uploaded CSV file
            data = csv.read()
            # Split along new line
            file_barcodes = re.split('\n', data.decode('utf-8'))

            #Remove carriage return from the barcodes
            barcodes += [barcode.replace('\r','') for barcode in file_barcodes]
            #
            # for index,barcode in enumerate(file_barcodes):
            #     if barcode:
            #         try:
            #             # Verify if an item with the given barcode exists in the database
            #             item = Items.objects.get(barcode=int(barcode))
            #             status.append(item)
            #             correct_count+=1
            #             print(correct_count)
            #         except Exception as e:
            #             status.append("")
            #             incorrect_count += 1
            #     else:
            #         continue

        # Remove duplicate entries
        barcodes = list(set(barcodes))
        sql_query = '''
                    SELECT barcode,
                    concat( b.title, ' ', ExtractValue((
                        SELECT metadata
                        FROM biblio_metadata b2
                        WHERE b.biblionumber = b2.biblionumber),
                          '//datafield[@tag="245"]/subfield[@code="b"]') ) AS title,
                    author, itype,
                    IF(location IS NOT NULL, location, ""),
                    IF(v.lib IS NOT NULL, v.lib, ""),items.itemcallnumber, "Available"
                    FROM items
                    LEFT JOIN biblio b USING (biblionumber)
                    LEFT JOIN authorised_values v ON (items.itemlost=v.authorised_value AND v.category = 'LOST')
                    WHERE barcode IN {barcodes}
                    AND itype IN ('C', 'DIVB', 'R', 'SPR', 'STB')

                    UNION ALL

                    SELECT barcode,
                    concat( b.title, ' ', ExtractValue((
                        SELECT metadata
                        FROM biblio_metadata b2
                        WHERE b.biblionumber = b2.biblionumber),
                          '//datafield[@tag="245"]/subfield[@code="b"]') ) AS title,
                    author, itype,
                    IF(location IS NOT NULL, location, ""),
                    IF(v.lib IS NOT NULL, v.lib, ""),items.itemcallnumber, "Unavailable"
                    FROM items
                    LEFT JOIN biblio b USING (biblionumber)
                    LEFT JOIN authorised_values v ON (items.itemlost=v.authorised_value AND v.category = 'LOST')
                    WHERE barcode NOT IN {barcodes}
                    AND itype IN ('C', 'DIVB', 'R', 'SPR', 'STB')
                    '''.format(barcodes = tuple(barcodes))

        correct_count = 0
        incorrect_count = 0
        values = []
        try:
            query_results = execute_query(sql_query)
        except:
            messages.warning(request, "Please check the format of csv files uploaded. They should contain only 1 column with barcodes.")
            return redirect('portal:barcode_csv')
        if query_results == 'Error':
            return JsonResponse({"message": "Sorry, error in SQL query"})

        for row in query_results:
            if row[-1] == 'Available':
                correct_count +=1
            else:
                incorrect_count +=1
            values.append(row)

        context = {
            'values': values,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'total': len(values)
        }
        return render(request, 'portal/barcode_report.html', context=context)

class AdminUserRecords(View):
    '''
    Reference: https://wiki.koha-community.org/wiki/SQL_Reports_Library#action_logs
    '''

    @method_decorator(login_required)
    def get(self,request):
        modules = [
            'CATALOGUING',
            'CIRCULATION',
            'FINES',
            'MEMBERS',
            'SERIAL',
        ]
        patron_numbers = ActionLogs.objects.values('user').distinct()
        patrons = []
        for borrower_dict in patron_numbers:
            borrowernumber = borrower_dict['user']
            if Borrowers.objects.filter(borrowernumber = borrowernumber).exists():
                patrons.append(Borrowers.objects.get(borrowernumber = borrowernumber))
            else:
                continue
        print(len(patrons))
        patrons.sort(key=lambda x: x.full_name.upper())
        print(len(patrons))

        return render(request, 'portal/admin_user_records.html', context={'modules': modules, 'patrons': patrons})

    @method_decorator(login_required)
    def post(self, request):
        try:
            module = request.POST['module']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            borrowernumber = request.POST['patron']
        except:
            return JsonResponse({'message': 'Invalid Request'})

        if module == 'FINES':
            sql_query = '''
                SELECT
                    TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) ) AS patron_name,
                    action_logs.timestamp, action,
                    TRIM(CONCAT(COALESCE(b2.firstname,""), " ",  COALESCE(b2.surname,"") ) ),
                    info, interface
                    FROM action_logs
                    LEFT JOIN borrowers b ON (action_logs.user = b.borrowernumber)
                    LEFT JOIN borrowers b2 ON (action_logs.object = b2.borrowernumber)
                    '''
            headings = [
                'Patron Name',
                'Time',
                'Action',
                'Borrower',
                'Info',
                'Interface'
            ]

        elif module == 'CIRCULATION':
             sql_query = '''
                 SELECT
                     TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) ) AS patron_name,
                     action_logs.timestamp, action,
                     TRIM(CONCAT(COALESCE(b2.firstname,""), " ",  COALESCE(b2.surname,""), " - (", b2.sort1, ")" ) ),
                     concat( biblio.title, ' ', ExtractValue((
                         SELECT metadata
                         FROM biblio_metadata b2
                         WHERE biblio.biblionumber = b2.biblionumber),
                           '//datafield[@tag="245"]/subfield[@code="b"]'), ' - (', items.barcode, ")" ),
                     interface
                     FROM action_logs
                     LEFT JOIN borrowers b ON (action_logs.user = b.borrowernumber)
                     LEFT JOIN borrowers b2 ON (action_logs.object = b2.borrowernumber)
                     LEFT JOIN items ON (action_logs.info = items.itemnumber)
                     LEFT JOIN biblio USING (biblionumber)
                     '''
             headings = [
                 'Patron Name',
                 'Time',
                 'Action',
                 'Borrower',
                 'Item',
                 'Interface'
             ]

        elif module == 'MEMBERS':
             sql_query = '''
                 SELECT
                     TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) ) AS patron_name,
                     action_logs.timestamp, action,
                     TRIM(CONCAT(COALESCE(b2.firstname,""), " ",  COALESCE(b2.surname,"") ) ),
                     info, interface
                     FROM action_logs
                     LEFT JOIN borrowers b ON (action_logs.user = b.borrowernumber)
                     LEFT JOIN borrowers b2 ON (action_logs.object = b2.borrowernumber)
                     '''
             headings = [
                 'Patron Name',
                 'Time',
                 'Action',
                 'Borrower',
                 'Info',
                 'Interface'
             ]

        elif module == 'SERIAL':
            sql_query = '''
                SELECT
                    TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) ) AS patron_name,
                    action_logs.timestamp, action,
                    object,interface
                    FROM action_logs
                    LEFT JOIN borrowers b ON (action_logs.user = b.borrowernumber)
                    '''
            headings = [
                'Patron Name',
                'Time',
                'Action',
                'Subscription ID',
                'Interface'
            ]

        elif module == 'CATALOGUING':
            sql_query = '''
                SELECT
                    TRIM(CONCAT(COALESCE(b.firstname,""), " ",  COALESCE(b.surname,"") ) ) AS patron_name,
                    action_logs.timestamp, action,object,info,interface,
                    IF(bib.title IS NOT NULL, bib.title, db.title)
                    FROM action_logs
                    LEFT JOIN borrowers b ON (action_logs.user = b.borrowernumber)
                    LEFT JOIN items it ON (info LIKE 'item%' AND object = it.itemnumber )
                    LEFT JOIN deleteditems di
                        ON (it.itemnumber IS NULL AND info LIKE 'item%' AND object=di.itemnumber)
                    LEFT JOIN biblio bib
                        ON (info LIKE 'biblio%' AND bib.biblionumber=object)
                            OR (info NOT LIKE 'biblio%' AND bib.biblionumber=it.biblionumber)
                                OR (info NOT LIKE 'biblio%' AND bib.biblionumber=di.biblionumber)
                    LEFT JOIN deletedbiblio db
                        ON (info LIKE 'biblio%' AND db.biblionumber=object)
                            OR (info NOT LIKE 'biblio%' AND db.biblionumber=it.biblionumber)
                                OR (info NOT LIKE 'biblio%' AND db.biblionumber=di.biblionumber)

                    '''
            headings = [
                'Patron Name',
                'Time',
                'Action',
                'Object',
                'Info',
                'Interface',
                'Title'
            ]

        sql_query += f'''
            WHERE module='{module}'
                AND Date(action_logs.timestamp) BETWEEN '{from_date}' AND '{to_date}'
                AND user={borrowernumber}
            ORDER BY action_logs.timestamp DESC
            '''

        print(sql_query)
        query_results = execute_query(sql_query)
        print('yes')
        if query_results == 'Error':
            return JsonResponse({"message": "Sorry, error in SQL query"})
        count = 0
        values = []
        for row in query_results:
            row = list(row)
            # if row[-1].startswith('item'):
            #     print(row[-1])
            #     try:
            #         item = Items.objects.get(itemnumber=row[-2])
            #         title = item.full_title
            #         row[-2] = title + ' - ' + item.barcode
            #     except:
            #         row[-2] = 'Item with itemnumber {} does not exist'.format(row[-2])
            # elif row[-1].startswith('biblio'):
            #     try:
            #         biblio = Biblio.objects.get(biblionumber=row[-2])
            #         row[-2] = biblio.full_title
            #     except:
            #         row[-2] = 'Biblio with biblionumber {} does not exist'.format(row[-2])

            values.append(row)
            count += 1


        context = {
        'headings': headings,
        'values': values,
        'count': count,
        'report_type': 'User Records',
        'url' : request.META['HTTP_REFERER']
        }
        return render(request, 'portal/circulation_reoprt.html', context)

def calculate_population_stats():
    '''
    Helper function to calculate population mean and variance for DSS
    '''
    issues = []
    item_count=[0]
    issue_count = [0]
    data = []
    counter = 0

    biblio_list = Biblio.objects.all()

    for biblio in biblio_list:
        items = biblio.items_set.all() # All the items of the biblio
        book_issues = [] # To store the number of issues of each item of the biblio
        book_item_count = [0] # Total number of items with the appropriate itemtype for the biblio
        for item in items:
            yearwise_issues = [0]*5
            # List of all yearwise issues of a book
            if item.itype in ('R', 'SPR', 'STB', 'DIVB', 'C'):
                book_item_count[0]+=1
                item_count[0]+=1
                issue = [0]
                try:
                    iss = item.issue
                    # Find the index number for yearwise_issues from the last digit of issuedate.year If year is 2018, index=8-4 = 4
                    index = iss.issuedate.year%10 - 4
                    if index in range(0,5):
                        yearwise_issues[index]+=1
                    if iss.issuedate.year in (2014,2015,2016,2017,2018):
                        issue[0]+=1
                except IndexError:
                    print(index)
                    raise Exception('Invalid Index debug')
                except Items.issue.RelatedObjectDoesNotExist:
                    # No issue exists
                    pass
                for old_issue in item.oldissues_set.all():
                    index = old_issue.issuedate.year%10 - 4
                    if index in range(0,5):
                        yearwise_issues[index]+=1
                data += yearwise_issues
                issue_count[0] += issue[0]
                book_issues.append(issue[0])
            else:
                continue
        issues.append(book_issues)
        print(counter)
        counter+=1

    import statistics
    from math import sqrt

    N = len(data)

    stdev = sigma/sqrt(N)
    population_stats = {
        'population_mean': statistics.mean(data),
        'variance': statistics.variance(data),
        'sigma': statistics.stdev(data),
        'stdev': statistics.stdev(data)/(sqrt(N))
    }
    return population_stats


class DSS(View):
    def get(self, request):
        form = ReservesForm()
        return render(request, 'portal/dss_input.html', {'form': form})

    def post(self, request):
        data = request.POST
        itemnumber = data['itemnumber']
        if not itemnumber:
            return JsonResponse({"message": 'Invalid Request'})
        biblio = Items.objects.get(itemnumber=itemnumber).biblionumber
        items = biblio.items_set.all() # All the items of the biblio
        item_count = 0
        book_issues=[]
        for item in items:
            if item.itype in ('R', 'SPR', 'STB', 'DIVB', 'C'):
                issue=[0]
                item_count+=1
                try:
                    iss = item.issue
                    if iss.issuedate.year in (2014,2015,2016,2017,2018):
                        issue[0]+=1
                except Items.issue.RelatedObjectDoesNotExist:
                    # No issue exists
                    pass
            for old_issue in item.oldissues_set.all():
                if old_issue.issuedate.year in (2014,2015,2016,2017,2018):
                    issue[0]+=1
            book_issues.append(issue[0])
        if item_count > 0:
            sample_mean = sum(book_issues) / (item_count*5)
        else:
            messages.info(request, 'No circulation book')

        # To get new values of population stats, use the helper function calculate_population_stats()
        # Change the years from 2014 to 2018 in the function to accomodate more data

        population_mean = 0.09937969311132876 # based on record generated on 8/07/2019
        variance = 0.20907310223569503
        sigma = 0.45724512270301476
        stdev = 0.0008261817232007021

        z_calc = (sample_mean - population_mean)/(stdev)

        if z_calc > 1.96:
            message = f'''Based on 95% confidence interval, new copies of the book need to be ordered'''
        else:
            message = f'''Based on 95% confidence interval, This book is not much used and new books need not be ordered.'''

        context = {
            'biblio': biblio,
            'item_count': item_count,
            'z_calc': z_calc,
            'message': message
        }

        return render(request, 'portal/dss.html', context)



def handler404(request, exception):
    '''
    Custom 404 Error Page template
    '''
    try:
        url = request.META['HTTP_REFERER']
    except:
        url = request.build_absolute_uri(reverse('portal:report_types'))
    print(url)
    return render(request, 'portal/404.html', status=404, context={'url':url})
