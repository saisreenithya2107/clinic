from django.urls import re_path, include, path
from .views import register,login1,verify,cmail
from . import views

app_name = 'madmin'

urlpatterns = [

    # path('', views.login, name='login'),
  #  path('pregister', views.patientregister, name='patientregister'),
    path('registerothers', views.registerothers, name='registerothers'),
    path('register', views.register, name='register'),
    path('l6', views.login1, name='login1'),
    path('logout', views.logout, name='logout'),
    path('verify', views.verify, name='verify'),
    path('confirmationmail', views.cmail, name='cmail'),
    
    path('d/', views.displayd, name='d'),
    path('m', views.displaym, name='m'),
    path('l', views.displayl, name='l'),
    path('s', views.displays, name='s'),

    path('ap', views.displayappointments, name='ap'),
    path('lap', views.displaylabappointments, name='lap'),
    path('lt', views.displaylabtest, name='lt'),
    path('med', views.displaymedicines, name='med'),

    path('LInfo', views.displabs, name='LInfo'),
    path('TInfo', views.disptests, name='TInfo'),


    path('A', views.staffPage, name='A'),
    path('LA', views.labPage, name='LA'),

    path('dellabs', views.dellabs, name='dellabs'),
    path('updlabs', views.updlabs, name='updlabs'),
    path('upd', views.upd, name='upd'),

    
    path('deltests', views.deltests, name='deltests'),
    path('updtests', views.updtests, name='updtests'),
    path('updT', views.updT, name='updT'),
    path('new', views.new, name='new'),
    path('newtest', views.newtest, name='newtest'),

    path('delmeds', views.delmeds, name='delmeds'),
    path('updmeds', views.updmeds, name='updmeds'),
    path('updM', views.updM, name='updM'),
    path('newmeds', views.newmeds, name='newmeds'),
    path('newMeddicines', views.newMeddicines, name='newMeddicines'),
    path('medcsv', views.medcsv, name='medcsv'),


    path('docupd', views.upddoc, name='docupd'),
    path('doctor_update', views.doctor_update, name='doctor_update'),
    path('deldocs', views.deldocs, name='deldocs'),

    path('staffupd', views.staffupd, name='staffupd'),
    path('staff_update', views.staff_update, name='staff_update'),
    path('delstaff', views.delstaff, name='delstaff'),
    
    path('labtechupd', views.labtechupd, name='labtechupd'),
    path('labtech_update', views.labtech_update, name='labtech_update'),
    path('dellabtech', views.dellabtech, name='dellabtech'),
    
    path('meddealerupd', views.meddealerupd, name='meddealerupd'),
    path('meddealer_update', views.meddealer_update, name='meddealer_update'),
    path('delmeddealer', views.delmeddealer, name='delmeddealer'),
]