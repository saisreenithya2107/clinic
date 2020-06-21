from django.contrib import admin

# Register your models here.
from .models import Doctor,check_date

admin.site.register(Doctor)
admin.site.register(check_date)