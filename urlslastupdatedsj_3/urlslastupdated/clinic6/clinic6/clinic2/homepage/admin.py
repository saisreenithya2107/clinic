from django.contrib import admin

# Register your models here.
from .models import Patient,Appointment,Tests_info,LabTest,user_reports,labAppointment,Medicine,PurchaseItem#,token


admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Tests_info)
admin.site.register(LabTest)
admin.site.register(user_reports)
admin.site.register(labAppointment)
admin.site.register(Medicine)
admin.site.register(PurchaseItem)
