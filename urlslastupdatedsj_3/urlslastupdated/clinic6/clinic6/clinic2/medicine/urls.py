from django.urls import re_path, include, path
from .views import register,login1,verify,cmail
from . import views

app_name = 'medicine'

urlpatterns = [

    # path('', views.login, name='login'),
  #  path('pregister', views.patientregister, name='patientregister'),
    path('register', views.register, name='register'),
    path('l5', views.login1, name='login1'),
    path('verify', views.verify, name='verify'),
    path('logout', views.logout, name='logout'),
    path('confirmationmail', views.cmail, name='cmail'),
    path('m', views.MPage, name='m'),
]