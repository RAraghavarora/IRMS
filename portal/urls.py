from django.contrib import admin
from django.urls import path, include
from portal import views

app_name='portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.Login.as_view(), name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('generate', views.GenerateReport.as_view(), name='generate_report'),
    path('circulation/',views.CirculationReport.as_view(), name='circulation'),
    path('checked_out/',views.checked_out, name='checked_out'),
    path('inactive_patrons/',views.inactive_patrons, name='inactive_patrons'),

    path('report_types/',views.report_types, name='report_types'),


    path('demo/',views.demo, name='demo'),


]
