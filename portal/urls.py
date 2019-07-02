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
    path('report_types/suggested_books/',views.suggested_books, name='suggested_books'),
    path('report_types/overdue_orders/',views.overdue_orders_30, name='overdue_orders'),
    path('report_types/invoice_register/',views.InvoiceRegister.as_view(), name='invoice_register'),

    path('report_types/holds_waiting/',views.holds_waiting, name='holds_waiting'),
    path('search_query/',views.BookAutocomplete.as_view(), name='search_query'),
    path('search_vendor/',views.VendorAutocomplete.as_view(), name='search_vendor'),

    path('book_detail/',views.book_detail, name='book_detail'),
    path('report_types/no_due',views.NoDue.as_view(), name='no_due'),
    path('report_types/no_due_save/',views.no_due_save, name='no_due_save'),
    path('report_types/no_due_non_members',views.NoDueNonMembers.as_view(), name='no_due_non_members'),
    path('non_member_save/',views.non_member_save, name='non_member_save'),
    path('report_types/ndc_archive',views.NDCArchive.as_view(), name='ndc_archive'),
    path('report_types/fine_report_summary',views.FineReportsSummary.as_view(), name='fine_report_summary'),
    path('report_types/fine_report_summary_save/',views.fine_report_summary_save, name='fine_report_summary_save'),
    path('report_types/fine_summary_archive',views.FineSummaryArchive.as_view(), name='fine_summary_archive'),
    path('report_types/fine_report/',views.FineReport.as_view(), name='fine_report'),
    path('report_types/vendor_orders',views.VendorOrders.as_view(), name='vendor_orders'),

    path('report_types/recent_arrivals', views.RecentArrivals.as_view(), name='recent_arrivals'),
    path('report_types/barcode_csv', views.BarcodeCSV.as_view(), name='barcode_csv'),

    path('abc/',views.abc, name='abc'),

    path('demo/',views.demo, name='demo'),
    path('hello/',views.hello, name='hello'),
]
