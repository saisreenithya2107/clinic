from django.urls import re_path, include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('home1/',views.home,name='home1'),
    path('home2/',views.homeAfterLogin,name='home2'),
    path('home3/',views.homehos,name='home3'),
    path('appointment/',views.appointment,name='appointment'),
    path('labtest/',views.labtest,name='labtest'),
    path('medicines/',views.medicines,name='medicines'),
    path('booked/',views.booked,name='booked'),
    path('bookedlab/',views.bookedlab,name='bookedlab'),
    path('dhome/', views.dhome, name='dhome'),
    path('dh/', views.dh, name='dh'),
    path('med/', views.med, name='med'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('verify', views.verify, name='verify'),
    path('docs', views.docs, name='docs'),
    
    path('prescribe', views.prescribe, name='prescribe'),
    path('addpres', views.addpres, name='addpres'),    

    path('hii/',views.hii,name = "hii"),

    path('calendar',views.initial,name = "calendar"),
    path('next/',views.for_next,name = "for_next"),
    path('back/',views.for_prev,name = "for_prev"),
    path('month/',views.filldata,name = "filldata"),
    path('selectmonth/',views.selectmonth,name = "selectmonth"),    

    path('ap', views.displayappointments, name='ap'),
    path('lap', views.displaylabappointments, name='lap'),


]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
