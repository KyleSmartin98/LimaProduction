from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogIn, name='login'),
    path('home/', views.home, name='home'),
    path('inventory/', views.Inventory, name='Inventory'),
    path('Method/', views.Method, name='Method'),
    path('Sample/', views.Sample, name='Sample'),
    path('Testing/', views.Testing, name='Testing'),
    path('Trending/', views.Trending, name='Trending'),
    path('Results/', views.Results, name='Results'),

]
