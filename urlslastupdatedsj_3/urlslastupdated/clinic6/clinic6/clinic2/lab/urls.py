from django.urls import re_path, include, path
from .views import register,login1,verify,cmail
from . import views

app_name = 'lab'

urlpatterns = [

    # path('', views.login, name='login'),
  #  path('pregister', views.patientregister, name='patientregister'),
    path('register', views.register, name='register'),
    path('l4', views.login1, name='login1'),
    path('verify', views.verify, name='verify'),
    path('logout', views.logout, name='logout'),
    path('confirmationmail', views.cmail, name='cmail'),
    path('lab1', views.labPage, name='lab1'),
    path('LInfo', views.labs, name='LInfo'),
    path('sendmail', views.sendmail, name='sendmail'),

    path('labtechupdate/',views.labtech_update,name='labtechupdate'),


    path('della', views.della, name='della'),
    path('updla', views.updla, name='updla'),    
    path('updLA', views.updLA, name='updLA'),

   
]