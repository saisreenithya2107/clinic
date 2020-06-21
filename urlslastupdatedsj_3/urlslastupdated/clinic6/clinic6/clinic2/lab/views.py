from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login, logout as out, update_session_auth_hash
from django.conf import settings
from .models import Lab, otp_verify
from django.contrib.auth import authenticate
import random


from django.db.models import Q
from homepage.models import *

from datetime import datetime
from django.utils.timezone import datetime

from django.core.mail import send_mail, EmailMessage
from clinic.settings import EMAIL_HOST_USER


def cmail(request):
    send_mail('sub', 'body', 'oclinic2020@gmail.com', ['sandeshjatla@gmail.com'], fail_silently= False)
    return render(request, 'home.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = Signup_user_form(request.POST)
        profile_form = Signup_profile_form(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            UserForm = user_form.save()
            print ("1")
            UserForm.set_password(UserForm.password)
            print ("2")
            UserForm.save()
            print ("3")
            ProfileForm = profile_form.save(commit=False)
            print ("4")
            ProfileForm.user = UserForm
            print ("5")
            ProfileForm.save()
            otp = random.randint(100000, 999999)
            send_mail("Hello doctor", "Thanks for registering " + str(otp) + " is your verification otp","oclinic2020@gmail.com", [UserForm.email])
            otpc = otp + 882413
            registered = True
        else:
            return HttpResponse("Invalid details!")
    else:
        user_form = Signup_user_form()
        profile_form = Signup_profile_form()

    if registered:
        request.session['username'] = user_form.cleaned_data.get('username')
        return render(request, 'lab/mailconfirmation.html', {'otpc': otpc})
    else:
        return render(request, 'lab/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def verify(request):
    if request.method=='POST':
        otpc = int(request.POST['otpc'])
        otp1 = str(request.POST['otp1'])
        otpc = otpc - 882413
        otpc = str(otpc)
        if otpc == otp1:
            return redirect("/home/home")
        else:
            username = request.session['username']
            dele = User.objects.get(username=username)
            dele.delete()
            return HttpResponse("mail unverified")
    else:
        return HttpResponse('404 error')

def login1(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print("1")
        if form.is_valid():
            user = form.get_user()
            print("2")
            auth_login(request, user)
            print("3")
            temp = 1
            print("4")
            doc = get_object_or_404(Lab, user=request.user)
            print("5")
            print(request.user)
            print(doc)
            return redirect('/lab/lab1')
            return HttpResponse("login successful")
        else:
            return HttpResponse("invalid details!")
    else:
        form = AuthenticationForm()
    return render(request, 'lab/login3.html', {'form': form,})

def logout(request):
    out(request)
    return HttpResponse("logged out")



def labs(request):
    labs=LabTest.objects.all()
    
    return render(request,'lab/LInfo.html',{'labs':labs})


def sendmail(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        subject = request.POST.get('subject', '')
        mail_id = request.POST.get('email', '')
        email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
        email.content_subtype = 'html'

        file = request.FILES['file']
        email.attach(file.name, file.read(), file.content_type)

        email.send()
        appointment=labAppointment.objects.all()
        return render(request,'lab/l1.html',{'appointment':appointment})
        #return HttpResponse("Sent")
    else:
            # appointment=labAppointment.objects.filter(Q(date=now.date(),time__gte=now.time())|Q(date__gt=now.date())).order_by('-date')
        return render(request, 'lab/sendmail.html')

def labtech_update(request):
    temp = 1
    labtech = get_object_or_404(Lab, user=request.user)
    if request.method == 'POST':
        labtech_form = Lab_Update_Form(request.POST, instance=request.user.lab or None)
        if labtech_form.is_valid():
            labtech_form.save()
            return redirect("/lab/lab1")
    else:
        labtech_form = Lab_Update_Form(instance=request.user)
    return render(request, 'lab/labtechupdate.html', {'labtech_form':labtech_form, 'temp':temp, 'labtech':labtech})


def della(request):
    appointment=labAppointment.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        labAppointment.objects.filter(lappid=id1).delete()
        
        return render(request,'lab/l1.html',{'appointment':appointment,'message': 'success'})
    else:
        return render(request,'lab/l1.html',{'appointment':appointment})


def updla(request):
    appointment=labAppointment.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        test=labAppointment.objects.get(lappid=id1)
        #print(lab.lab_name)
        
        return render(request,'lab/LAupd.html',{'test':test,'message': 'success'})
    else:
        return render(request,'lab/l1.html',{'appointment':appointment})    

def updLA(request):
    appointment=labAppointment.objects.all()
    if request.method=='POST':
        print("mmmmmmmmmmmmmmmm")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        id6=request.POST.get('name5')
        
        # id4=request.POST.get('name4')
        print(id5)
        test=labAppointment.objects.get(lappid=id5)

        
        # print(lab.lab_name)
        # test.name=id1
        # test.strength=id2
        # test.quantity=id3
        test.date=id4
        test.time=id6
        # test.period=id7
        # test.price=id8

        test.save()

        return render(request,'lab/l1.html',{'appointment':appointment,'message': 'success'})
    else:
        return render(request,'lab/l1.html',{'appointment':appointment})    

def labPage(request):
    now = datetime.now()
    appointment=labAppointment.objects.all()
    print("hi1")
    if request.method == 'POST':
        flag = request.POST.get('flag')
        print("one")
        print(flag)
        if flag == '1':
            print("two")
            mailid1 = request.POST.get('mailid1')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            print(mailid1)
            print("hello")
            return render(request, 'lab/sendmail.html', {'mailid1':mailid1,'firstname':firstname,'lastname':lastname})
        else:
            return render(request, 'lab/l1.html',{'appointment':appointment})    

        print(mailid1)
        return render(request,'lab/sendmail.html', {'mailid1':mailid1})
    else:
        return render(request,'lab/l1.html',{'appointment':appointment})

# def labPage(request):
#     now = datetime.now()
#     # appointment=labAppointment.objects.filter(Q(date=now.date(),time__gte=now.time())|Q(date__gt=now.date())).order_by('-date')
#     appointment=labAppointment.objects.all()
#     return render(request,'lab/l1.html',{'appointment':appointment})
