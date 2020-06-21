from django.urls import re_path, include, path
from .views import register,login1,verify,cmail
from . import views

app_name = 'staff'

urlpatterns = [

    # path('', views.login, name='login'),
  #  path('pregister', views.patientregister, name='patientregister'),
    path('register', views.register, name='register'),
    path('l3', views.login1, name='login1'),
    path('logout', views.logout, name='logout'),
    path('verify', views.verify, name='verify'),
    path('confirmationmail', views.cmail, name='cmail'),
    path('staff1', views.staffPage, name='staff1'),
    path('appointment/',views.appointment,name='appointment'),
    path('booked/',views.booked,name='booked'),
    path('staffupdate/',views.staff_update,name='staffupdate'),

    path('hii/',views.hii,name = "hii"),
    path('cal/',views.cal,name = "cal"),

    path('calendar',views.initial,name = "calendar"),
    path('next/',views.for_next,name = "for_next"),
    path('back/',views.for_prev,name = "for_prev"),
    path('month/',views.filldata,name = "filldata"),
    path('selectmonth/',views.selectmonth,name = "selectmonth"),    


    path('della', views.della, name='della'),
    path('updla', views.updla, name='updla'),    
    path('updLA', views.updLA, name='updLA'),

]