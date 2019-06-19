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
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

#Using django-mysql library to Extract surname from Marctag
from django_mysql.models.functions import XMLExtractValue

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from portal.models import *
from portal.forms import ReservesForm
from portal.apps import *


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
        return render(request, 'portal/profile.html', {'name':user.username.capitalize()})
    except Exception as unknown_exception:
        return JsonResponse({'message':unknown_exception})

def demo(request):
    return JsonResponse(request.session['saved'])


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

    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="igcarlibrary",
        db="library"
    )
    cur = db.cursor()

    total_books = Items.objects.filter(itype='C').count # itype 'C' means the items that are 'Circulated' and ignores the journals, etc.

    try:
        cur.execute(sql_query)

        count=0 #To count the total number of entries

        values = []
        for row in cur.fetchall():

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

    except MySQLdb.Error as e:
        print(e)
        return JsonResponse({"message":"Unable to fetch data"})

@login_required
def report_types(request):
    form = ReservesForm()
    return render(request, 'portal/types.html', {'form':form})

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

    except MySQLdb.Error as e:
        print(e)
        return JsonResponse({'message':"Unable to fetch data"})

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

    except MySQLdb.Error as e:
        print(e)
        return JsonResponse({'message':"Unable to fetch data"})

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

def hello(request):

    items = Items.objects.filter(itype='C', biblionumber__title__icontains='sql')
    data = [item.biblionumber for item in items]
    data = serializers.serialize('json', data)
    print(data)
    return HttpResponse(data, content_type='application/json')

@login_required
def holds_waiting(request):
    sql_query='''
            SELECT TRIM(CONCAT(COALESCE(borrowers.firstname,""), " ",  COALESCE(borrowers.surname,"") ) ),
            borrowers.email, borrowers.cardnumber,
            reserves.waitingdate, items.barcode, biblio.title, reserves.timestamp
            FROM reserves
            LEFT JOIN borrowers USING (borrowernumber)
            LEFT JOIN items USING (itemnumber)
            LEFT JOIN biblio ON (items.biblionumber = biblio.biblionumber)
            WHERE reserves.waitingdate IS NOT NULL;
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
            'Patron email',
            'Patron membership number',
            'Hold Date (Reserve Date)',
            'Book barcode (Accession Number)',
            'Book title',
            'Last updated on'
        ]

        context = {
            'count':count,
            'values':values,
            'headings':headings,
            'report_type':'Circulation Report - Holds Waiting'
        }

    except MySQLdb.Error as e:
        print(e)
        return JsonResponse({'message':"Unable to fetch data"})

    return render(request, 'portal/circulation_reoprt.html', context=context)


class BookAutocomplete(autocomplete.Select2QuerySetView):
    #Using Django-autocomplete library

    def get_queryset(self):
        items = Items.objects.filter(itype='C').order_by('itemnumber')

        items_list = []
        if self.q:
            print("**************88")
            items = items.annotate(full_name = Concat(
                'biblionumber__title',
                Value(' '),
                XMLExtractValue('biblionumber__bibliometadata__metadata','//datafield[@tag="245"]/subfield[@code="b"]') )
                )
            items_list = items.filter(full_name__istartswith=self.q)

        if items_list:
            print('Nah')
            return items_list
        else:
            return items

def abc(request):
    return None

@login_required
def book_detail(request):
    '''
    Display details of a book
    '''
    if request.method == 'POST':
        data = request.POST
        print(data)
        try:
            itemnumber = data['itemnumber']
            item = Items.objects.get(itemnumber=itemnumber)
            biblio = item.biblionumber

            context = {
                'title': item.full_title,
                'author': biblio.author,
                'barcode': item.barcode
            }
            print(context)
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

    def get(self, request):
        '''
        Input the IC number of members.
        '''
        # Get all the addressee
        addressee_list = NoDueAddressee.objects.all()
        context = {'addressee_list':addressee_list}
        print(context)
        return render(request, 'portal/no_due_input.html', context=context)

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
            return render(request, 'portal/no_due_input.html', context)

        if not valid_patrons:
            return JsonResponse({'message': 'Please Enter IC numbers'})


        all_books = []
        all_fines=[]
        failed_patrons = []

        for patron in valid_patrons:
            # Filter the Issues by the patron
            issues = Issues.objects.filter(borrowernumber = patron)

            accountlines = Accountlines.objects.filter(borrowernumber = patron)
            fine = accountlines.aggregate(Sum('amountoutstanding'))['amountoutstanding__sum']


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
        max_ref_no = NoDueCertificate.objects.aggregate(Max('ref_number'))['ref_number__max']
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

        # Get the chosen addressee
        try:
            addressee_id = request.POST['addressee']
            addressee = NoDueAddressee.objects.get(id=addressee_id)
        except KeyError:
            return JsonResponse({'message':'Addressee not chosen'})
        except AttributeError:
            return JsonResponse({'message':'Invalid Addressee'})


        context = {
            'report_number': report_number,
            'valid_data':valid_data,
            'report_number': report_number,
            'date':date,
            'failed_data':failed_data,
            'addressee':addressee
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
        addressee = NoDueAddressee.objects.get(id=addressee_id)

        # Get the report number by incrementing the maximum report number by 1
        max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
        if max_report_no:
            report_number = max_report_no + 1
        else:
            report_number = 1

        ref_number_list = []

        # Get the maximum reference number
        max_ref_no = NoDueCertificate.objects.aggregate(Max('ref_number'))['ref_number__max']
        # We are starting reference numbers from 3001, as this software will be used after 3000 reports
        if not max_ref_no or max_ref_no < 3001:
            refer_number = 3001
        else:
            refer_number = max_ref_no + 1

        for ref_no in range(refer_number, refer_number + len(patrons_ids)):
            ref_number_list.append(ref_no)

    except KeyError:
        return JsonResponse({'message': "Invalid Request"})

    for patron_id, ref_number, ref_no_date in zip(patrons_ids, ref_number_list, ref_no_date_list):
        borrower = Borrowers.objects.get(borrowernumber=patron_id)
        ndc = NoDueCertificate.objects.create(
            report_number = report_number,
            patron_name = borrower.full_name,
            ic_number = borrower.sort1,
            division = borrower.address,
            mem_number = borrower.cardnumber,
            ref_number = ref_number,
            ref_no_date = ref_no_date,
            date=datetime.date.today(),
            addressee_content = addressee.content
            )

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

    def get(self, request):
        # Get all the addressee
        addressee_list = NoDueAddressee.objects.all()
        context = {'addressee_list':addressee_list}
        return render(request, 'portal/non_members_input.html', context=context)

    def post(self,request):
        try:
            data = request.POST
            ic_number_list = data.getlist('ic_no')
            name_list = data.getlist('name')
            div_list = data.getlist('div')
            ref_no_date_list = data.getlist('ref_no_date')
            addressee_id = request.POST['addressee']
            addressee = NoDueAddressee.objects.get(id=addressee_id)

            # Get the report number by incrementing the maximum report number by 1
            max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
            if max_report_no:
                report_number = max_report_no + 1
            else:
                report_number = 1

            ref_number_list = []

            # Get the maximum reference number
            max_ref_no = NoDueCertificate.objects.aggregate(Max('ref_number'))['ref_number__max']
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
        addressee = NoDueAddressee.objects.get(id=addressee_id)

        # Get the report number by incrementing the maximum report number by 1
        max_report_no = NoDueCertificate.objects.aggregate(Max('report_number'))['report_number__max']
        if max_report_no:
            report_number = max_report_no + 1
        else:
            report_number = 1

        ref_number_list = []

        # Get the maximum reference number
        max_ref_no = NoDueCertificate.objects.aggregate(Max('ref_number'))['ref_number__max']
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
        ref_numbers,
        ref_no_date_list
    )
    for name, ic_number, division, ref_number_list, ref_no_date in data_zip:
        ndc = NoDueCertificate.objects.create(
            report_number = report_number,
            patron_name = name,
            ic_number = ic_number,
            division = division,
            mem_number = 'Non. Mem.',
            ref_number = ref_number,
            ref_no_date = ref_no_date,
            date=datetime.date.today(),
            addressee_content = addressee.content
            )

    messages.success(request, 'Data successfully saved')

    valid_data = zip(
        names,
        ic_numbers,
        divs,
        ref_numbers,
        ref_no_date_list
    )
    date = datetime.date.today()

    context = {'date':date, 'valid_data':valid_data, 'report_number': report_number,'addressee':addressee}

    return render(request,'portal/non_member_final.html', context)

class NDCArchive(View):

    def get(self, request):
        ndcs = NoDueCertificate.objects.all().order_by('report_number')
        return render(request, 'portal/ndc_archive.html', {'ndcs':ndcs})

    def post(self, request):
        data = request.POST
        return JsonResponse(data)
