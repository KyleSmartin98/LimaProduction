from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogIn, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('home/', views.home, name='home'),
    path('inventory/', views.Inventory, name='Inventory'),
    path('Method/', views.Method, name='Method'),
    path('Sample/', views.Sample_page, name='Sample'),
    path('addsample/', views.SampleCreate.as_view(), name = 'addsample'),
    path('Testing/', views.Testing, name='Testing'),
    path('Trending/', views.Trending, name='Trending'),
    path('Results/', views.Results, name='Results'),

]
