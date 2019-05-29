from django.contrib import admin
from django.urls import path, include
from portal import views

app_name='portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.Login.as_view(), name='login'),
    path('generate', views.GenerateReport.as_view(), name='generate_report')
]
