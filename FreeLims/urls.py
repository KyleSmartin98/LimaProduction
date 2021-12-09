from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogIn, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('home/', views.home, name='home'),
    path('inventory/', views.Inventory, name='Inventory'),
    path('Method/', views.Method, name='Method'),
    path('Sample/', views.Sample_page, name='Sample'),
    path('Testing/', views.Testing, name='Testing'),
    path('Initiate_sample/<str:pk>/', views.Initiatesample, name='Initiate_sample'),
    path('Trending/', views.Trending, name='Trending'),
    path('Results/', views.Results, name='Results'),
    path('Results_submit/<str:pk>/', views.Resultssubmit, name='Results_submit'),
    path('samplecsv/', views.sample_export, name='downloadsamplecsv')
]
