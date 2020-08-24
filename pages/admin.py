from django.contrib import admin
from .models import Test, Patient, TestingCenter, Appointment, SMSNotification, HealthCenter, HealthRegion, Area, ScreeningCenter

admin.site.register(Test)
admin.site.register(Patient)
admin.site.register(TestingCenter)
admin.site.register(ScreeningCenter)
admin.site.register(Appointment)
admin.site.register(SMSNotification)
admin.site.register(HealthCenter)
admin.site.register(HealthRegion)
admin.site.register(Area)


