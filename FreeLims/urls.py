from django.urls import path
from . import views

urlpatterns = [
    path('',views.landingPage, name='landingpage'),
    path('log-in/', views.LogIn, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('home/', views.home, name='home'),
    path('settings/', views.settings_page, name='settings'),
    path('inventory/', views.Inventory, name='Inventory'),
    path('Instrument_management/', views.Instrument, name='Instrument'),
    path('Sample/', views.Sample_page, name='Sample'),
    path('Testing/', views.Testing, name='Testing'),
    path('Initiate_sample/<str:pk>/', views.Initiatesample, name='Initiate_sample'),
    path('Trending/', views.Trending, name='Trending'),
    path('Results/', views.Results, name='Results'),
    path('Documentation/', views.Documentation, name = 'Documentation'),
    path('Results_submit/<str:pk>/', views.Resultssubmit, name='Results_submit'),
    path('Results_review/<str:pk>/', views.Resultsreview, name='Results_review'),
    path('Results_summary/<str:pk>/', views.resultsSummary, name='Results_summary'),
    path('Audit_review/<str:pk>/', views.auditReview, name='Audit_review'),
    path('Inventory_open/<str:pk>/', views.InventoryOpen, name='Inventory_open'),
    path('Barcode_download/<str:pk>/', views.BarcodeDownload, name='Barcode_download'),
    path('sampleBarcode_download/<str:pk>/', views.sampleBarcodeDownload, name='sampleBarcode_download'),
    path('Inventory_create', views.Inventorycreate, name='Inventory_create'),
    path('samplecsv/', views.sample_export, name='downloadsamplecsv'),
    path('resultcsv', views.result_export, name='downloadresultcsv'),
    path('inventorycsv', views.inventory_export, name='inventorycsv'),
]
