from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login, logout as out, update_session_auth_hash
from django.conf import settings
from .models import Staff, otp_verify
from django.contrib.auth import authenticate
import random

from django.core.files.storage import FileSystemStorage

from doctor.models import *
from django.db.models import Q
from homepage.models import *

# from datetime import datetime
# from django.utils.timezone import datetime

import datetime
import calendar


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
            send_mail("Hello staff", "Thanks for registering " + str(otp) + " is your verification otp","oclinic2020@gmail.com", [UserForm.email])
            otpc = otp + 882413
            registered = True
        else:
            return HttpResponse("Invalid details!")
    else:
        user_form = Signup_user_form()
        profile_form = Signup_profile_form()

    if registered:
        request.session['username'] = user_form.cleaned_data.get('username')
        return render(request, 'staff/mailconfirmation.html', {'otpc': otpc})
    else:
        return render(request, 'staff/signup.html', {'user_form': user_form, 'profile_form': profile_form})


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
            doc = get_object_or_404(Staff, user=request.user)
            print("5")
            print(request.user)
            print(doc)
            return redirect('/staff/staff1')
            #return HttpResponse("login successful")
        else:
            return HttpResponse("invalid details!")
    else:
        form = AuthenticationForm()
    return render(request, 'staff/login3.html', {'form': form,})

def logout(request):
    out(request)
    return HttpResponse("logged out")


def staffPage(request):
    doctors=Doctor.objects.all()
    now = datetime.now()
    appointment=Appointment.objects.all()
    if request.method=="POST":
        doc=request.POST.get('doc')
        d=Doctor.objects.get(did=doc)
        dapps=Appointment.objects.filter(doctor_id=d)
        return render(request,'staff/s1.html',{'doctors':doctors,'appointment':dapps})
    # appointment=Appointment.objects.filter(Q(date=now.date(),time__gte=now.time())|Q(date__gt=now.date())).order_by('-date')
    return render(request,'staff/s1.html',{'doctors':doctors,'appointment':appointment})

# def del1(request):
#     app=Appointment

#views for calender ------------------------------------------

next_month = 0
next_year = 0
back_month = 0
back_year = 0
current_month = 0
current_year = 0

def currentdate():
    return datetime.date.today()


def index(request):
    return render(request,'homepage/put_calendar/index.html')

def initial(request):

    doc=request.POST.get('doc')
    d=Doctor.objects.get(did=doc)
    print("passsss the best")
    print(d)

    today = currentdate()
    today_str = today.isoformat()
    year  = int(today_str[:4])
    month = int(today_str[5:7])
    global current_month
    current_month = month
    global current_year
    current_year = year
    global next_month
    next_month = current_month
    global next_year
    next_year = current_year
    global back_month
    back_month = current_month
    global back_year
    back_year = current_year
    return grid(request,current_year,current_month,d)


def for_next(request):
    global back_month
    global back_year
    global next_month
    global next_year
    if next_month <12 and next_month >= 1:
       next_month = next_month + 1
       next_year = next_year
    else :
       next_month = 1
       next_year = next_year +1
    back_month = next_month
    back_year = next_year
    print(next_month,next_year)
    global current_month
    current_month = next_month
    global current_year
    current_year = next_year
    return grid(request,next_year,next_month)


def for_prev(request):
    global back_month
    global back_year
    global next_month
    global next_year
    if back_month >1 and back_month <=12:
       back_month = back_month - 1
       back_year = back_year
    else :
       back_month = 12
       back_year = back_year - 1
    next_month = back_month
    next_year = back_year
    global current_month
    current_month = back_month
    global current_year
    current_year = back_year
    return grid(request,back_year,back_month)


def filldata(request):
    # user=request.user
    # doc=Doctor.objects.get(user=user)
    # if request.method=="POST":
    print("passsss the best")
    doc=request.POST.get('doc')
    d=Doctor.objects.get(did=doc)
    #     dapps=Appointment.objects.filter(doctor_id=d)
    #     return render(request,'staff/new1.html',{'doctors':doctors,'appointment':dapps})
    # # appointment=Appointment.objects.filter(Q(date=now.date(),time__gte=now.time())|Q(date__gt=now.date())).order_by('-date')
    # return render(request,'staff/new1.html',{'doctors':doctors,'appointment':appointment})

    # date_str = request.POST['date_work']
    # work = request.POST['data_work']
    # date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
    # print(type(date))
    # print(work)
    # Check_date = check_date.objects.create(doctor_id=d,date = date,work_title = work)
    return grid(request,current_year,current_month,d)


def selectmonth(request):
    month = request.POST['select_month']
    year_int = int(month[0:4])
    month_int = int(month[5:8])
    global current_month
    current_month = month_int
    global current_year
    current_year = year_int
    global next_month
    next_month = current_month
    global next_year
    next_year = current_year
    global back_month
    back_month = current_month
    global back_year
    back_year = current_year
    return grid(request,current_year,current_month)


def grid(request,year,month,D):

    month_calendar = calendar.monthcalendar(year,month)
    year_detail = [month,year]
      #list with dates as nested lists
    month_name = calendar.month_name[month]
    year_name = str(month_name + ' , '+str(year))
    len_month = len(month_calendar)
    dummy_month = []                 #extra month which contains nested lists
    dates_with_works = []            #dates with works contain date as a number
    dates_needed = []                #necessary dates with date format(associated with work)
    date_print = []                  #dates as numbers that are used for printing
    time_list = []                   #list of times allotted for tasks
    date_format = []                 # dates in year format used for checking with special dates
    work_on_date = []                #list of work in dates
    date_dict = {}                   #date time work dictionary
   # month and year print
    for i in range(len(month_calendar)):
     for j in range(len(month_calendar[i])):
        if month_calendar[i][j] > 0:
            if month_calendar[i][j] <10:
                y = str('0'+str(month_calendar[i][j]))
                date_print.append(y)
            if month_calendar[i][j] >= 10:
                y = str(month_calendar[i][j])
                date_print.append(y)

    print(date_print)
    print(month_calendar)
    # getting a date string in yyyy-mm-dd
    for i in range(len(date_print)):
        if month < 10:
            month_str = str('0'+str(month))
        else:
            month_str = str(month)
        each_date = str(str(year)+'-'+month_str+'-'+date_print[i])
        date_format.append(each_date)

    print(date_format)
   # making a dummy calendar.month format
    for i in range(len_month):
        dummy = [0,0,0,0,0,0,0]
        dummy_month.append(dummy)


   #getting all the dates from database and filtering the dates of the present month and making a dictionary with dates as keys
   # value is an empty list
    flag = 1
    date_list = []
    # doc=request.user
    # D=Doctor.objects.get(user=doc)
    #query = check_date.objects.order_by('work_title')
    query = check_date.objects.filter(doctor_id=D)
    for i in range(len(query)):
        query_date = query[i].date
        date_string = query_date.isoformat()
        if int(date_string[5:7]) == month :
          dates_needed.append(date_string)
          # making a list of dates with works
          dates_with_works.append(int(date_string[8:10]))
          date_list= list(date_dict.keys())
          date_list = str(date_list)
          for i in range(len(date_list)):
              if date_string == date_list[i]:
                  flag = 0
                  break
          if flag == 1 :
             date_dict[date_string] = []
    print(dates_needed)

    # assigning tasks in the lists of values for keys in dictionary
    for key in range(len(query)):
        a = query[key].date
        g = a.isoformat()
        b = str(query[key].work_title)
        if g in date_list:
            date_dict[g].append([b])



    # replacing the dummy month elements of dates with

    for m in range(len(date_format)):
      for i in range(len(dummy_month)):
        for j in range(len(dummy_month[i])):
          if len(dates_with_works) != 0:
            for k in range(len(dates_with_works)):
               if month_calendar[i][j] == dates_with_works[k] and date_format[m] == dates_needed[k]:
                  #for check in range(len(work_on_date[k])):
                  #  dummy_month[i][j] = [dates_with_works[k],[work_on_date[k][check]],[time_list[k][check]]]
                  dummy_month[i][j] = [dates_with_works[k],date_dict[dates_needed[k]]]
    print(dummy_month)
    return render(request,'staff/new1.html',{'month_cal':month_calendar,'zipped_data':zip(month_calendar,dummy_month),'present_year':year_name,'year_number':year_detail})





def cal(request):
    doctors=Doctor.objects.all()
    #now = datetime.now()
    appointment=Appointment.objects.all()
    if request.method=="POST":
        doc=request.POST.get('doc')
        d=Doctor.objects.get(did=doc)
        dapps=Appointment.objects.filter(doctor_id=d)
        return render(request,'staff/new1.html',{'doctors':doctors,'appointment':dapps})
    # appointment=Appointment.objects.filter(Q(date=now.date(),time__gte=now.time())|Q(date__gt=now.date())).order_by('-date')
    return render(request,'staff/new1.html',{'doctors':doctors,'appointment':appointment})



def appointment(request):
    doctors=Doctor.objects.all()
    temp=1
    # print(doctors[0].user)
    # print(doctors[0])
    return render(request, 'staff/app.html',{'doctors':doctors,'temp':temp})


def hii(request):
    if request.method=="POST":
        k=request.POST.get("imp")
        doctors=Doctor.objects.all()
        doctor=request.POST.get("doctor")
        user1=User.objects.get(username = doctor)
        D=Doctor.objects.get(user=user1)
        dates=check_date.objects.filter(doctor_id=D)
        print(dates[0].date)
        print("111111111111111111111111111")
        print(k)
        return render(request,'staff/app1111.html',{'dates':dates,'user':request.user,'doctors':doctors,'D':D})
    return HttpResponse("okkkkk")


def booked(request):
    if request.method == 'POST':
        appointment=Appointment()
        patient=request.POST.get('patient')
        doctor=request.POST.get('doctor')
        date=request.POST.get('date')
        time=request.POST.get('time')
        symtoms=request.POST.get('symtoms')
        myfile=request.FILES['reports']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        print("hhhhhhhhhhhhhh")
        print(filename)
        user=User.objects.get(username = patient)
        user1=User.objects.get(username = doctor)
        P=Patient.objects.get(user=user)
        D=Doctor.objects.get(user=user1)
        print(D)
        appointment.user_name=P
        appointment.doctor_id=D
        appointment.date=date
        appointment.time=time
        appointment.symptoms=symtoms
        appointment.reports=request.FILES['reports']

        string= random.randint(100000000,10000000000000)
        viedo_chat_link="https://appr.tc/r/"+str(string)

        appointment.link=viedo_chat_link

        appointment.save()

        
        send_mail('Hello patient', 'your appointment is booked '+ viedo_chat_link + ' join through this', 'oclinic2020@gmail.com', [P.email_id], fail_silently= False)

        send_mail('Hello patient', 'your appointment is booked '+ viedo_chat_link + ' join through this', 'oclinic2020@gmail.com', [D.email_id], fail_silently= False)


    return HttpResponse("Thanksssss!!!")


def staff_update(request):
    temp = 1
    staff = get_object_or_404(Staff, user=request.user)
    if request.method == 'POST':
        staff_form = Staff_Update_Form(request.POST, instance=request.user.staff or None)
        print("aaaaaaaa")
        if staff_form.is_valid():
            print("nnnnn")
            staff_form.save()
            print("kkkkkkkkkk")
            return redirect("/staff/staff1")
    else:
        staff_form = Staff_Update_Form(instance=request.user)
    return render(request, 'staff/staffupdate.html', {'staff_form':staff_form, 'temp':temp, 'staff':staff})


def della(request):
    appointment=Appointment.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('del')
        print(id1)
        Appointment.objects.filter(aid=id1).delete()
        
        return render(request,'staff/s1.html',{'appointment':appointment,'message': 'success'})
    else:
        return render(request,'staff/s1.html',{'appointment':appointment})


def updla(request):
    appointment=Appointment.objects.all()
    if request.method=='POST':
        print("aaaaaaaaaaaaaa")
        id1=request.POST.get('upd')
        print(id1)
        test=Appointment.objects.get(aid=id1)
        #print(lab.lab_name)
        
        return render(request,'staff/LAupd.html',{'test':test,'message': 'success'})
    else:
        return render(request,'staff/s1.html',{'appointment':appointment})    

def updLA(request):
    appointment=Appointment.objects.all()
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
        test=Appointment.objects.get(aid=id5)

        
        # print(lab.lab_name)
        # test.name=id1
        # test.strength=id2
        # test.quantity=id3
        test.date=id4
        test.time=id6
        # test.period=id7
        # test.price=id8

        test.save()

        return render(request,'staff/s1.html',{'appointment':appointment,'message': 'success'})
    else:
        return render(request,'staff/s1.html',{'appointment':appointment})    
