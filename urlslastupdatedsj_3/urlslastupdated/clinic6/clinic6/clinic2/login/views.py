from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login, logout as out, update_session_auth_hash
from django.conf import settings
from .models import Patient, otp_verify
from django.contrib.auth import authenticate
import random
# Create your views here.

#def login(request):
    # return render(request, 'home.html', {'name':'sj'})
#    return render(request, 'login.html')

#def register(request):
    # return render(request, 'home.html', {'name':'sj'})
#    return render(request, 'home.html')


def cmail(request):
    send_mail('sub', 'body', 'oclinic2020@gmail.com', ['sandeshjatla@gmail.com'], fail_silently= False)
    return render(request, 'login/home.html')

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
            send_mail("Hello patient", "Thanks for registering " + str(otp) + " is your verification otp","oclinic2020@gmail.com", [UserForm.email])
            otpc = otp + 882413
            registered = True
        else:
            return HttpResponse("Invalid details!")
    else:
        user_form = Signup_user_form()
        profile_form = Signup_profile_form()

    if registered:
        request.session['username'] = user_form.cleaned_data.get('username')
        return render(request, 'login/mailconfirmation.html', {'otpc': otpc})
    else:
        return render(request, 'login/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def verify(request):
    if request.method=='POST':
        otpc = int(request.POST['otpc'])
        otp1 = str(request.POST['otp1'])
        otpc = otpc - 882413
        otpc = str(otpc)
        if otpc == otp1:
            return redirect("/home/home2")
        else:
            username = request.session['username']
            dele = User.objects.get(username=username)
            dele.delete()
            return HttpResponse("mail unverified")
    else:
        return HttpResponse('404 error')

def login(request):
    #
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            temp = 1
            pat = get_object_or_404(Patient, user=request.user)
            print(request.user)
            print(pat)
            #return redirect('/login/home/', {'pat': pat,'doc': doc})
            return HttpResponse("login successful")
        else:
            return HttpResponse("invalid details!")
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form,})

def logout(request):
    out(request)
    return HttpResponse("logged out")

