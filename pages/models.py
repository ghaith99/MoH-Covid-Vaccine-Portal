from django.db import models
from datetime import datetime
from users.models import CustomUser
from django.urls import reverse
import uuid
import qrcode
from django.conf import settings
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File 
import string
import shortuuid

class Patient(models.Model):
    id = models.CharField(primary_key=True, max_length=6, editable=False)
    created_datetime = models.DateTimeField(default=datetime.now, blank=True, verbose_name= ('Created Date'))
    civil_ID = models.CharField(max_length = 25,  unique=True, verbose_name= ('Civil ID'))
    civil_serial = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('Civil ID Serial'))
    passport_number = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('Passport Number'))
    phone = models.CharField(max_length=20, verbose_name= ('Phone'))
    city = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('City'))
    nationality = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('Nationality'))
    gender = models.CharField(blank=True, max_length=10, choices=(('M', "Male"),('F', "Female")), verbose_name= ('Gender'))
    birthday  =  models.DateField(null=True, blank=True, verbose_name= ('Birthday'))
    first_name  = models.CharField(max_length = 25, verbose_name= ('First Name'))
    last_name  = models.CharField(max_length = 40, verbose_name= ('Last Name'))
    author = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE, verbose_name= ('Author'))
    comments = models.TextField(null=True, blank=True, max_length=700, verbose_name= ('Comments'))
  
    def save(self):
        if not self.id:
            self.id = shortuuid.ShortUUID(alphabet="01345678ABCDEFG").random(length=6)
            while Patient.objects.filter(id=self.id).exists():
                self.id = id_generator()
        super(Patient, self).save()
        
    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={"pk": self.id})
    
    def __str__(self):
        return self.civil_ID
     
    class Meta:
       ordering = ['-created_datetime']

class TestingCenter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("testingcenter_detail", kwargs={"pk": self.pk})
       
class ScreeningCenter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("screeningcenter_detail", kwargs={"pk": self.pk})

class Test(models.Model):
    id = models.CharField(primary_key=True, max_length=6, editable=False)
    qr_code = models.ImageField(blank=True)
    patient = models.ForeignKey(Patient,  null=True, on_delete=models.SET_NULL, verbose_name= ('Patient Civil ID'), related_name ='patient_tests')
    mixed = models.CharField(default = 'False', choices=(('False','False'), ('True', 'True')), max_length=10, null=True, blank=True, verbose_name= ('Mixed'))
    symptoms = models.CharField(default = 'False', choices=(('False','False'), ('True', 'True')), max_length=10, null=True, blank=True, verbose_name= ('Covid Symptoms'))
    lab_doctor = models.ForeignKey('users.CustomUser',on_delete=models.SET_NULL, null=True, blank=True, verbose_name= ('Lab Doctor'),  related_name='lab_doctor')
    test_result =  models.CharField(choices=((None,''), ('Positive','Positive'), ('Negative', 'Negative'), ('Equivalent', 'Equivalent'), ('Reject', 'Reject')),max_length=10, blank=True, null=True, default=None, verbose_name= ('Test Result'))
    testing_center = models.ForeignKey(TestingCenter, null=True, blank=True, on_delete=models.SET_NULL, verbose_name= ('Testing Center'), related_name ='testingcenter_tests')
    screening_center = models.ForeignKey(ScreeningCenter, null=True, blank=True, on_delete=models.SET_NULL, verbose_name= ('Screening Center'),related_name ='screeningcenter_tests')
    test_notes =  models.TextField(null=True, blank=True, verbose_name= ('Test Notes'))
    author = models.ForeignKey('users.CustomUser', null=True, on_delete=models.SET_NULL, verbose_name= ('Author'))
    field_user = models.ForeignKey(settings.AUTH_USER_MODEL,null = True, blank = True, on_delete=models.SET_NULL, verbose_name= ('Field User'), related_name='field_user')
    lab_user = models.ForeignKey(settings.AUTH_USER_MODEL,null = True, blank = True, on_delete=models.SET_NULL, verbose_name= ('Lab User'), related_name='lab_user')
    sms_status =  models.BooleanField(default = False, null=True, blank=True, verbose_name= ('SMS Sent'))
    result_datetime = models.DateTimeField(null=True, blank=True, verbose_name= ('Result Date'))
    updated_datetime = models.DateTimeField(auto_now = True, blank=True, verbose_name= ('Updated Date'))
    sample_datetime = models.DateTimeField(default=datetime.now, blank=True, verbose_name= ('Sample Date'))
    
    def to_dict_json(self): # for Datatable pagination
        return {
            'pk': self.pk,
            'Civil ID': self.patient.civil_ID,
            'Sample Date': self.sample_datetime,
            'Result Date': self.result_datetime,
        }
    
    def save(self):
        if not self.id:
            self.id = shortuuid.ShortUUID(alphabet="01345678ABCDEFG").random(length=6)
            while Test.objects.filter(id=self.id).exists():
                self.id = id_generator()
        super(Test, self).save()
        
    def get_absolute_url(self):
        return reverse("test_detail", kwargs={"pk": self.id})
    

    class Meta:
        ordering = ['-sample_datetime']


# class SMSMessage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     test = models.OneToOneField(Test)
#     message = models.CharField(max_length=200)


class SMSNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name= ('Created Data time'))
    update_time = models.DateTimeField(auto_now=True)
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='test_smses'
    )
    message = models.CharField(max_length=200)#models.ForeignKey(SMSMessage)
    sent_status = models.BooleanField(default=False)


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    testing_center = models.ForeignKey(TestingCenter, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
