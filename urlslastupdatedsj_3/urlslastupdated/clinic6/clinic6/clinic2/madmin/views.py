from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login, logout as out, update_session_auth_hash
from django.conf import settings
from .models import Madmin, otp_verify
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import random

from doctor.models import Doctor
from lab.models import Lab
from medicine.models import Meduser
from staff.models import Staff
from homepage.models import Appointment, labAppointment, Medicine, LabTest , Tests_info

from doctor.forms import Doctor_Update_Form


import csv, io
import os
from django.contrib import messages


def cmail(request):
    send_mail('sub', 'body', 'oclinic2020@gmail.com', ['sandeshjatla@gmail.com'], fail_silently= False)
    return render(request, 'home.html')

@login_required(login_url='/madmin/l6')
def registerothers(request):
    return render(request, 'madmin/reg.html')

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
        return render(request, 'madmin/mailconfirmation.html', {'otpc': otpc})
    else:
        return render(request, 'madmin/signup.html', {'user_form': user_form, 'profile_form': profile_form})


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
            doc = get_object_or_404(Madmin, user=request.user)
            print("5")
            print(request.user)
            print(doc)
            return redirect('/madmin/registerothers')
            #return HttpResponse("login successful")
        else:
            return HttpResponse("invalid details!")
    else:
        form = AuthenticationForm()
    return render(request, 'madmin/login6.html', {'form': form,})

def logout(request):
    out(request)
    return HttpResponse("logged out")


# def display(request):
#     doc=Doctor.objects.all()
#     return render(request,'madmin/d.html',{'doc':doc})


def displayd(request):
    doc=Doctor.objects.all()
    return render(request,'madmin/d.html',{'doc':doc})

def displayl(request):
    labu=Lab.objects.all()
    return render(request,'madmin/l.html',{'staff':labu})

def displaym(request):
    medu=Meduser.objects.all()
    return render(request,'madmin/m.html',{'staff':medu})

def displays(request):
    staff=Staff.objects.all()
    return render(request,'madmin/s.html',{'staff':staff})

def displayappointments(request):
    ap=Appointment.objects.all()
    return render(request,'madmin/ap.html',{'ap':ap})

def displaylabappointments(request):
    lap=labAppointment.objects.all()
    return render(request,'madmin/lap.html',{'lap':lap})

def displaylabtest(request):
    lt=LabTest.objects.all()
    return render(request,'madmin/lt.html',{'lt':lt})

def displaymedicines(request):
    med=Medicine.objects.all()
    return render(request,'madmin/med.html',{'med':med})


def displabs(request):
    labs=LabTest.objects.all()
    
    return render(request,'madmin/LInfo.html',{'labs':labs})

def disptests(request):
    tests=Tests_info.objects.all()
    
    return render(request,'madmin/tests.html',{'tests':tests})

def labPage(request):
    
    appointment=labAppointment.objects.all()
    return render(request,'madmin/l1.html',{'appointment':appointment})

def staffPage(request):
    
    appointment=Appointment.objects.all()
    return render(request,'madmin/s1.html',{'appointment':appointment})

def dellabs(request):
    labs=LabTest.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        LabTest.objects.filter(ltid=id1).delete()
        
        return render(request,'madmin/LInfo.html',{'labs':labs,'message': 'success'})
    else:
        return render(request,'madmin/LInfo.html',{'labs':labs})


def updlabs(request):
    labs=LabTest.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        lab=LabTest.objects.get(ltid=id1)
        print(lab.lab_name)
        
        return render(request,'madmin/Lupd.html',{'lab':lab,'message': 'success'})
    else:
        return render(request,'madmin/LInfo.html',{'labs':labs})    

def upd(request):
    labs=LabTest.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        print(id1)
        lab=LabTest.objects.get(ltid=id5)
        # print(lab.lab_name)
        lab.lab_name=id1
        lab.email_id=id2
        lab.phone_num=id3

        lab.save()

        return render(request,'madmin/LInfo.html',{'labs':labs,'message': 'success'})
    else:
        return render(request,'madmin/LInfo.html',{'labs':labs})    


def deltests(request):
    tests=Tests_info.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Tests_info.objects.filter(tid=id1).delete()
        
        return render(request,'madmin/tests.html',{'tests':tests,'message': 'success'})
    else:
        return render(request,'madmin/tests.html',{'tests':tests})


def updtests(request):
    tests=Tests_info.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        test=Tests_info.objects.get(tid=id1)
        #print(lab.lab_name)
        
        return render(request,'madmin/Tupd.html',{'test':test,'message': 'success'})
    else:
        return render(request,'madmin/tests.html',{'tests':tests})    

def updT(request):
    tests=Tests_info.objects.all()
    if request.method=='POST':
        print("mmmmmmmmmmmmmmmm")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        # id4=request.POST.get('name4')
        print(id5)
        test=Tests_info.objects.get(tid=id5)
        # print(lab.lab_name)
        test.test_name=id1
        test.about=id2
        test.cost=id3

        test.save()

        return render(request,'madmin/tests.html',{'tests':tests,'message': 'success'})
    else:
        return render(request,'madmin/tests.html',{'tests':tests})    


def new(request):
    return render(request,'madmin/newtest.html')


def newtest(request):
    test=Tests_info()
    tests=Tests_info.objects.all()
    if request.method=='POST':
        
        
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        
        test.test_name=id1
        test.about=id2
        test.cost=id3

        test.save()

        return render(request,'madmin/tests.html',{'tests':tests,'message': 'success'})
    else:
        return render(request,'madmin/tests.html',{'tests':tests})    








def delmeds(request):
    med=Medicine.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Medicine.objects.filter(mid=id1).delete()
        
        return render(request,'madmin/med.html',{'med':med,'message': 'success'})
    else:
        return render(request,'madmin/med.html',{'med':med})


def updmeds(request):
    med=Medicine.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        test=Medicine.objects.get(mid=id1)
        #print(lab.lab_name)
        
        return render(request,'madmin/Mupd.html',{'test':test,'message': 'success'})
    else:
        return render(request,'madmin/med.html',{'med':med})    

def updM(request):
    med=Medicine.objects.all()
    if request.method=='POST':
        print("mmmmmmmmmmmmmmmm")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        id6=request.POST.get('name5')
        id7=request.POST.get('name6')
        id8=request.POST.get('name7')
        # id4=request.POST.get('name4')
        print(id5)
        test=Medicine.objects.get(mid=id5)
        # print(lab.lab_name)
        test.name=id1
        test.strength=id2
        test.quantity=id3
        test.prandial=id4
        test.times=id6
        test.period=id7
        test.price=id8

        test.save()

        return render(request,'madmin/med.html',{'med':med,'message': 'success'})
    else:
        return render(request,'madmin/med.html',{'med':med})    


def newmeds(request):
    return render(request,'madmin/newmeds.html')


def newMeddicines(request):
    
    
    meds=Medicine.objects.all()
    if request.method=='POST':
        
        test=Medicine()    
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        id5=request.POST.get('name5')
        id6=request.POST.get('name6')
        id7=request.POST.get('name7')
        
        test.name=id1
        test.strength=id2
        test.quantity=id3
        test.prandial=id4
        test.times=id5
        test.period=id6
        test.price=id7

        test.save()

        return render(request,'madmin/med.html',{'med':meds,'message': 'success'})
    else:
        return render(request,'madmin/med.html',{'med':meds})    















def upddoc(request):
    docs=Doctor.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        doc=Doctor.objects.get(did=id1)
        #print(lab.lab_name)
        
        return render(request,'madmin/Dupd.html',{'doc':doc,'message': 'success'})
    else:
        return render(request,'madmin/d.html',{'doc':docs})    



def doctor_update(request):
    docs=Doctor.objects.all()
    if request.method=='POST':
        print("mmmmmmmmmmmmmmmm")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        id6=request.POST.get('name5')
        id7=request.POST.get('name6')
        id8=request.POST.get('name7')
        # id4=request.POST.get('name4')
        print(id5)
        doc=Doctor.objects.get(did=id5)
        # print(lab.lab_name)
        doc.firstname=id1
        doc.lastname=id2
        doc.phone_num=id3
        doc.address=id4
        doc.experience=id6
        doc.specialization=id7
        doc.fee=id8
        doc.phone_num=id3


        doc.save()

        return render(request,'madmin/d.html',{'doc':docs,'message': 'success'})
    else:
        return render(request,'madmin/d.html',{'doc':docs})    

def deldocs(request):
    docs=Doctor.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Doctor.objects.filter(did=id1).delete()
        
        return render(request,'madmin/d.html',{'doc':docs,'message': 'success'})
    else:
        return render(request,'madmin/d.html',{'doc':docs})


def staffupd(request):
    staffs=Staff.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        doc=Staff.objects.get(sid=id1)
        #print(lab.lab_name)
        
        return render(request,'madmin/Supd.html',{'doc':doc,'message': 'success'})
    else:
        return render(request,'madmin/s.html',{'staff':staffs})    



def staff_update(request):
    staff=Staff.objects.all()
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
        doc=Staff.objects.get(sid=id5)
        # print(lab.lab_name)
        doc.firstname=id1
        doc.lastname=id2
        doc.phone_num=id3
        doc.address=id4
        doc.age=id6


        doc.save()

        return render(request,'madmin/s.html',{'staff':staff,'message': 'success'})
    else:
        return render(request,'madmin/s.html',{'staff':staff})    

def delstaff(request):
    staff=Staff.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Staff.objects.filter(sid=id1).delete()
        
        return render(request,'madmin/s.html',{'staff':staff,'message': 'success'})
    else:
        return render(request,'madmin/s.html',{'staff':staff})


def labtechupd(request):
    staff=Lab.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        doc=Lab.objects.get(lid=id1)
        #print(lab.lab_name)
        
        return render(request,'madmin/LTupd.html',{'doc':doc,'message': 'success'})
    else:
        return render(request,'madmin/l.html',{'staff':staff})    



def labtech_update(request):
    staff=Lab.objects.all()
    if request.method=='POST':
        print("mmmmmmmmmmmmmmmm")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        
        # id4=request.POST.get('name4')
        print(id5)
        doc=Lab.objects.get(lid=id5)
        # print(lab.lab_name)
        doc.firstname=id1
        doc.lastname=id2
        doc.phone_num=id3
        doc.address=id4
        


        doc.save()

        return render(request,'madmin/l.html',{'staff':staff,'message': 'success'})
    else:
        return render(request,'madmin/l.html',{'staff':staff})    

def dellabtech(request):
    staff=Lab.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Lab.objects.filter(lid=id1).delete()
        
        return render(request,'madmin/l.html',{'staff':staff,'message': 'success'})
    else:
        return render(request,'madmin/l.html',{'staff':staff})



def meddealerupd(request):
    staff=Meduser.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        doc=Meduser.objects.get(mid=id1)
        #print(lab.lab_name)
        
        return render(request,'madmin/MDupd.html',{'doc':doc,'message': 'success'})
    else:
        return render(request,'madmin/m.html',{'staff':staff})    



def meddealer_update(request):
    staff=Meduser.objects.all()
    if request.method=='POST':
        print("mmmmmmmmmmmmmmmm")
        id5=request.POST.get('upd')
        id1=request.POST.get('name')
        id2=request.POST.get('name2')
        id3=request.POST.get('name3')
        id4=request.POST.get('name4')
        
        # id4=request.POST.get('name4')
        print(id5)
        doc=Meduser.objects.get(mid=id5)
        # print(lab.lab_name)
        doc.firstname=id1
        doc.lastname=id2
        doc.phone_num=id3
        doc.address=id4
        


        doc.save()

        return render(request,'madmin/m.html',{'staff':staff,'message': 'success'})
    else:
        return render(request,'madmin/m.html',{'staff':staff})    

def delmeddealer(request):
    staff=Meduser.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Meduser.objects.filter(mid=id1).delete()
        
        return render(request,'madmin/m.html',{'staff':staff,'message': 'success'})
    else:
        return render(request,'madmin/m.html',{'staff':staff})





def medcsv(request):
    meds=Medicine.objects.all()
    if request.method=='POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        print("kkkkkkkkkk")
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            print("gggggggggggggg")
            print(column[2])
          # user = User.objects.get_or_create(username=column[1],email='supri@gmail.com'),
          # user[0][0].set_password(column[4])
          # print(user[0][0])
          # user[0][0].save(),
            _, created = Medicine.objects.update_or_create(

             name=column[0],
             strength=column[1],
             about=column[3],
             quantity=column[2],
             prandial=column[4],
             times=column[5],
             period=column[6],
             price=float(column[7]),
             



            )
          
        print("enddddddddddddd")
        return render(request,'madmin/med.html',{'med':meds,'message': 'success'})
    else:
        return render(request,'madmin/med.html',{'med':meds})    
