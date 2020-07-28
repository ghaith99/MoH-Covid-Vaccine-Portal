from django.contrib import admin

from .models import Test, Patient, TestingCenter, Appointment, SMSNotification

admin.site.register(Test)
admin.site.register(Patient)
admin.site.register(TestingCenter)
admin.site.register(Appointment)
admin.site.register(SMSNotification)