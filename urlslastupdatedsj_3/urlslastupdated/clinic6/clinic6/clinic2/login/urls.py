from django.urls import re_path, include, path
from . import views

app_name = 'login'

urlpatterns = [

    path('', views.login, name='login'),
  #  path('pregister', views.patientregister, name='patientregister'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('l1', views.login, name='login'),
    path('verify', views.verify, name='verify'),
    path('confirmationmail', views.cmail, name='cmail'),
   
]