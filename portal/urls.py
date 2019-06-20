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
    path('report_types/circulation/',views.CirculationReport.as_view(), name='circulation'),
    path('report_types/checked_out/',views.checked_out, name='checked_out'),
    path('report_types/inactive_patrons/',views.inactive_patrons, name='inactive_patrons'),
    path('search/', views.Search.as_view(), name='search'),
    path('report_types/',views.report_types, name='report_types'),
    path('report_types/inactive_books/',views.inactive_books, name='inactive_books'),
    path('report_types/holds_waiting/',views.holds_waiting, name='holds_waiting'),
    path('search_query/',views.BookAutocomplete.as_view(), name='search_query'),
    path('book_detail/',views.book_detail, name='book_detail'),
    path('report_types/no_due',views.NoDue.as_view(), name='no_due'),
    path('report_types/no_due_save/',views.no_due_save, name='no_due_save'),
    path('report_types/no_due_non_members',views.NoDueNonMembers.as_view(), name='no_due_non_members'),
    path('non_member_save/',views.non_member_save, name='non_member_save'),
    path('report_types/ndc_archive',views.NDCArchive.as_view(), name='ndc_archive'),
    path('report_types/fine_report',views.FineReports.as_view(), name='fine_report'),
    path('report_types/fine_report_save/',views.fine_report_save, name='fine_report_save'),


    path('abc/',views.abc, name='abc'),

    path('demo/',views.demo, name='demo'),
    path('hello/',views.hello, name='hello'),
]
