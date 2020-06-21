
from django.http import HttpResponse
# Create your views here.
from django.core.mail import send_mail
from .models import *
from doctor.models import *
import random
from django.core.files.storage import FileSystemStorage
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login, logout as out, update_session_auth_hash
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



import datetime
import calendar

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
            send_mail("Hello patient", "Thanks for registering " + str(otp) + " is your verification otp","oclinic2020@gmail.com", [ProfileForm.email_id])
            otpc = otp + 882413
            registered = True
        else:
            return HttpResponse("Invalid details!")
    else:
        user_form = Signup_user_form()
        profile_form = Signup_profile_form()

    if registered:
        request.session['username'] = user_form.cleaned_data.get('username')
        return render(request, 'homepage/mailconfirmation.html', {'otpc': otpc})
    else:
        return render(request, 'homepage/register.html', {'user_form': user_form, 'profile_form': profile_form})


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
            return render(request, 'homepage/home2.html', {'pat': pat,})
            return HttpResponse("login successful")
        else:
            return HttpResponse("invalid details!")
    else:
        form = AuthenticationForm()
    return render(request, 'homepage/login.html', {'form': form,})


def homehos(request):
    return render(request, 'homepage/home3.html')


def homeAfterLogin(request):
    return render(request, 'homepage/home2.html')

def home(request):
	
    return render(request, 'homepage/home1.html')

def docs(request):
	doctors=Doctor.objects.all()
	return render(request, 'homepage/doc.html',{'doctors':doctors})



@login_required(login_url='/home/login')
def appointment(request):
	doctors=Doctor.objects.all()
	temp=1
	# print(doctors[0].user)
	# print(doctors[0])
	return render(request, 'homepage/appointment.html',{'doctors':doctors,'temp':temp})

@login_required(login_url='/home/login')
def labtest(request):
	tests=Tests_info.objects.all()
	lab=LabTest.objects.all()
	return render(request, 'homepage/labtest.html',{'tests':tests,'labs':lab})


@login_required(login_url='/home/login')
def medicines(request):
	meds=Medicine.objects.all()
	return render(request, 'homepage/medicines.html',{'meds':meds})


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
        return render(request,'homepage/appointment1111.html',{'dates':dates,'user':request.user,'doctors':doctors,'D':D})
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


def bookedlab(request):
	if request.method == 'POST':
		labappointment=labAppointment()
		patient=request.POST.get('patient')
		test=request.POST.get('test')
		labs=request.POST.get('labs')
		date=request.POST.get('date')
		time=request.POST.get('time')
		
		myfile=request.FILES['prescription']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)

		print("hhhhhhhhhhhhhh")
		print(filename)
		user=User.objects.get(username = patient)
		t1=Tests_info.objects.get(test_name = test)
		l1=LabTest.objects.get(lab_name=labs)
		P=Patient.objects.get(user=user)
		
		
		labappointment.test_id=t1
		labappointment.lab_name=l1
		labappointment.date=date
		labappointment.time=time
		labappointment.user_name=P
		labappointment.prescription=request.FILES['prescription']
		labappointment.save()
		send_mail('Hello patient', 'your appointment is booked', 'oclinic2020@gmail.com', [P.email_id], fail_silently= False)
	return HttpResponse("Thanksssss again!!!")


def dhome(request):
    user=request.user
    doc=Doctor.objects.get(user=user)
    app=Appointment.objects.filter(doctor_id=doc)
    print(app[0].user_name)
    return render(request,'homepage/dhome.html',{'app':app})

def dh(request):
	user=request.user
	doc=Doctor.objects.get(user=user)
	app=Appointment.objects.filter(doctor_id=doc)
	print(app)
	return render(request,'homepage/dh.html',{'app':app})	



def med(request):
	if request.method == 'POST':
		med=PurchaseItem()
		patient=request.POST.get('patient')
		mname=request.POST.get('mname')
		mq=request.POST.get('mq')
		myfile=request.FILES['prescription']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		
		print("hhhhhhhhhhhhhh")
		
		user=User.objects.get(username = patient)
		m1=Medicine.objects.get(name = mname)
		P=Patient.objects.get(user=user)
		kk=(m1.price)*(float(mq))
		med.medicine=m1
		med.cost=(m1.price)*(float(mq))
		med.quantity=mq
		med.user_name=P
		med.prescription=request.FILES['prescription']
		med.save()
		send_mail('Hello patient', 'your have successfully orderd ' + str(kk) +' is your bill', 'oclinic2020@gmail.com', [P.email_id], fail_silently= False)
	return HttpResponse("Thanksssss again and again!!!")


def logout(request):
    out(request)
    return redirect("/home/home3")


def prescribe(request):
    tests=Tests_info.objects.all()
    meds=Medicine.objects.all()
    print(meds)
    return render(request,'homepage/prescribe.html',{'tests':tests,'meds':meds})



def addpres(request):
    if request.method=='POST':
        id1=request.POST.getlist('test')
        id2=request.POST.getlist('med')
        id3=request.POST.get('det')
        print("aaaaaaa")
        print(id1)
        print(id2)
        f= open("./media/guru99.txt","w+")
        f.write("Doctor's suggestions"+"\n"+str(id3)+"\n\n\n"+"the required tests"+str(id1)+"\n\n"+"the required meds"+str(id2))
        f.close()
        #myfile=request.FILES['prescription']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        

        return HttpResponse("okkk")
    else:
        return HttpResponse("notokk")    

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
    return grid(request,current_year,current_month)


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
	user=request.user
	doc=Doctor.objects.get(user=user)
	
	date_str = request.POST['date_work']
	work = request.POST['data_work']
	date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
	print(type(date))
	print(work)
	Check_date = check_date.objects.create(doctor_id=doc,date = date,work_title = work)
	return grid(request,current_year,current_month)


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


def grid(request,year,month):

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
    doc=request.user
    D=Doctor.objects.get(user=doc)
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
    return render(request,'homepage/put_templates/new1.html',{'month_cal':month_calendar,'zipped_data':zip(month_calendar,dummy_month),'present_year':year_name,'year_number':year_detail})





def displayappointments(request):
    p=request.user
    P=Patient.objects.get(user=p)
    ap=Appointment.objects.filter(user_name=P)
    return render(request,'homepage/ap.html',{'ap':ap})

def displaylabappointments(request):
    p=request.user
    P=Patient.objects.get(user=p)
    lap=labAppointment.objects.filter(user_name=P)
    return render(request,'homepage/lap.html',{'lap':lap})
