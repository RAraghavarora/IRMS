from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView

# Create your views here.

def home(request):
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

class Login(APIView):

    def get(self, request):
        return render(request, 'portal/login.html')
