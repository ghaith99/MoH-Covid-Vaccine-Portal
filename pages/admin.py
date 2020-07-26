from django.contrib import admin

from .models import Test, Patient, Hospital, Appointment, SMSNotification



admin.site.register(Test)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(SMSNotification)