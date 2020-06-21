#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
import datetime
from datetime import date
import uuid

class Madmin(models.Model):
    maid= models.CharField(max_length=100,primary_key=True,unique=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    #madmin_photo = models.FileField(null=True)
    #email_id = models.CharField(max_length=150,null=True,blank=True)
    #phone_num = models.BigIntegerField(null=True,blank=True)
    #address = models.CharField(null=True,blank=True,max_length=50)
    #date_of_birth = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.firstname+' '+self.lastname



class otp_verify(models.Model):
    name=models.CharField(max_length=50)
    otp=models.IntegerField(default=0)


