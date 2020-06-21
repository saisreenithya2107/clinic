from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login, logout as out, update_session_auth_hash
from django.conf import settings
from .models import Meduser, otp_verify
from django.contrib.auth import authenticate
import random


from django.db.models import Q
from homepage.models import *

from datetime import datetime
from django.utils.timezone import datetime



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
        return render(request, 'medicine/mailconfirmation.html', {'otpc': otpc})
    else:
        return render(request, 'medicine/signup.html', {'user_form': user_form, 'profile_form': profile_form})


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
            doc = get_object_or_404(Meduser, user=request.user)
            print("5")
            print(request.user)
            print(doc)
            return redirect('/medicine/m')
            #return HttpResponse("login successful")
        else:
            return HttpResponse("invalid details!")
    else:
        form = AuthenticationForm()
    return render(request, 'medicine/login5.html', {'form': form,})

def logout(request):
    out(request)
    return HttpResponse("logged out")


def MPage(request):

    m=PurchaseItem.objects.all()
    print(m)
    return render(request,'medicine/m1.html',{'m':m})
