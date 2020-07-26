from django.db import models
from datetime import datetime
from users.models import CustomUser
from django.urls import reverse

class Patient(models.Model):

    city = models.CharField(max_length = 25, verbose_name= ('City'))
    gender = models.CharField(blank=True, max_length=1, choices=(('M', "Male"),('F', "Female")), verbose_name= ('Gender'))
    civilID = models.CharField(max_length = 25, verbose_name= ('Civil ID'))
    civilSerial = models.CharField(max_length = 25, verbose_name= ('Civil Serial'))
    birthday  =  models.DateTimeField(null=True, blank=True, verbose_name= ('Birthday'))
    firstname  = models.CharField(max_length = 25, verbose_name= ('First Name'))
    lastname  = models.CharField(max_length = 25, verbose_name= ('Last Name'))
    symptoms  = models.TextField(blank=True, max_length=250, verbose_name= ('Symptoms'))
    phone = models.CharField(blank=True, max_length=20, verbose_name= ('Phone'))

    #Med Info

    BLOOD = (
        ('A+', 'A+ Type'),
        ('B+', 'B+ Type'),
        ('AB+', 'AB+ Type'),
        ('O+', 'O+ Type'),
        ('A-', 'A- Type'),
        ('B-', 'B- Type'),
        ('AB-', 'AB- Type'),
        ('O-', 'O- Type'),
    )
    bloodType = models.CharField(null=True, blank=True, max_length=10, choices=BLOOD, verbose_name= ('Blood Type'))
    allergy = models.TextField(null=True, blank=True, max_length=100, verbose_name= ('Allergy'))
    alzheimer = models.BooleanField(null=True, blank=True, verbose_name= ('Alzheimer'))
    asthma = models.BooleanField(null=True, blank=True, verbose_name= ('Asthma'))
    diabetes = models.BooleanField(null=True, blank=True, verbose_name= ('Diabetes'))
    stroke = models.BooleanField(null=True, blank=True, verbose_name= ('Stroke'))
    comments= models.TextField(null=True, blank=True, max_length=700, verbose_name= ('Comments'))
   
    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.civilID


class Hospital(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Test(models.Model):
    datatime = models.DateTimeField(default=datetime.now, blank=True, verbose_name= ('Created Data time'))
    lastModified = models.DateTimeField(auto_now = True, blank=True, verbose_name= ('Last Modified'))
    resultDate = models.DateTimeField(null=True, blank=True, verbose_name= ('Result Date'))
    testNotes =  models.TextField(verbose_name= ('Test Notes'))
    testResult =  models.NullBooleanField(choices=((None,''), (True,'Positive'), (False, 'Negative')),max_length=3, blank=True, null=True, default=None, verbose_name= ('Test Result'))
    completed = models.BooleanField(null=True, blank=True, verbose_name= ('Completed'))
    author = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE, verbose_name= ('Author'))
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name= ('Patient'), related_name ='patient_tests')
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE, verbose_name= ('Hospital'))
  
    def get_absolute_url(self):
        return reverse("test_detail", kwargs={"pk": self.pk})


class SMSNotification(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    sent_timestamp = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    startTime = models.TimeField()
    endTime = models.TimeField()
    date = models.DateField()
    