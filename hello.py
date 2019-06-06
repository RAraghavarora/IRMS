from portal.models import *

from django.apps import apps
app_models=apps.all_models['portal']

a=[]
for modelname, model in dict(app_models).items():
    try:
        a.append(model._meta.pk)
        model.objects.all()
    except:
            print(modelname,'\t',model)
# print(a)
