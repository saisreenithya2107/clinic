from django.urls import re_path, include, path
from .views import register,login1,verify,cmail
from . import views

app_name = 'doctor'

urlpatterns = [

    # path('', views.login, name='login'),
  #  path('pregister', views.patientregister, name='patientregister'),
    path('register', views.register, name='register'),
    path('l2', views.login1, name='login1'),
    path('logout', views.logout, name='logout'),
    path('verify', views.verify, name='verify'),
    path('confirmationmail', views.cmail, name='cmail'),
    path('dhome/', views.dhome, name='dhome'),
    path('Pappointment/',views.Pappointment,name='Pappointment'),
    path('doctorupdate/',views.doctor_update,name='doctorupdate')

]