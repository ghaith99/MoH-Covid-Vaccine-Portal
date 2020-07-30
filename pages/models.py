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

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    civil_ID = models.CharField(max_length = 25,  unique=True, verbose_name= ('Civil ID'))
    civil_serial = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('Civil ID Serial'))
    passport_number = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('Passport Number'))
    phone = models.CharField(max_length=20, verbose_name= ('Phone'))
    city = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('City'))
    nationality = models.CharField(null = True, blank = True, max_length = 25, verbose_name= ('Nationality'))
    gender = models.CharField(blank=True, max_length=1, choices=(('M', "Male"),('F', "Female")), verbose_name= ('Gender'))
    birthday  =  models.DateField(null=True, blank=True, verbose_name= ('Birthday'))
    first_name  = models.CharField(max_length = 25, verbose_name= ('First Name'))
    last_name  = models.CharField(max_length = 25, verbose_name= ('Last Name'))
    author = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE, verbose_name= ('Author'))
    comments = models.TextField(null=True, blank=True, max_length=700, verbose_name= ('Comments'))

    #Med Info
    # BLOOD = (
    #     ('A+', 'A+ Type'),
    #     ('B+', 'B+ Type'),
    #     ('AB+', 'AB+ Type'),
    #     ('O+', 'O+ Type'),
    #     ('A-', 'A- Type'),
    #     ('B-', 'B- Type'),
    #     ('AB-', 'AB- Type'),
    #     ('O-', 'O- Type'),
    # )
    # status = (
    #     ('mixed', 'مخالط'),
    #     ('symptoms', 'تواجد أعراض'),
    # )
    # bloodType = models.CharField(null=True, blank=True, max_length=10, choices=BLOOD, verbose_name= ('Blood Type'))
    #status = models.CharField(max_length=15, choices=status, verbose_name= ('Status'))
    # allergy = models.TextField(null=True, blank=True, max_length=100, verbose_name= ('Allergy'))
    # alzheimer = models.BooleanField(null=True, blank=True, verbose_name= ('Alzheimer'))
    # asthma = models.BooleanField(null=True, blank=True, verbose_name= ('Asthma'))
    # diabetes = models.BooleanField(null=True, blank=True, verbose_name= ('Diabetes'))
    # stroke = models.BooleanField(null=True, blank=True, verbose_name= ('Stroke'))
   
    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.civil_ID

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qr_code = models.ImageField(blank=True)
    completed = models.BooleanField(default = False,  verbose_name= ('Completed'))
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name= ('Patient Civil ID'), related_name ='patient_tests')
    mixed = models.CharField(default = 'False', choices=(('False','False'), ('True', 'True')), max_length=10, null=True, blank=True, verbose_name= ('Mixed'))
    symptoms = models.CharField(default = 'False', choices=(('False','False'), ('True', 'True')), max_length=10, null=True, blank=True, verbose_name= ('Covid Symptoms'))
    lab_doctor = models.CharField(max_length=25, null=True, blank=True, verbose_name= ('Lab Doctor'))
    test_result =  models.CharField(choices=((None,''), ('Positive','Positive'), ('Negative', 'Negative'), ('Equivalent', 'Equivalent'), ('Reject', 'Reject')),max_length=10, blank=True, null=True, default=None, verbose_name= ('Test Result'))
    testing_center = models.ForeignKey(TestingCenter, null=True, blank=True, on_delete=models.CASCADE, verbose_name= ('Testing Center'), related_name ='testingcenter_tests')
    screening_center = models.ForeignKey(ScreeningCenter, null=True, blank=True, on_delete=models.CASCADE, verbose_name= ('Screening Center'),related_name ='screeningcenter_tests')
    test_notes =  models.TextField(null=True, blank=True, verbose_name= ('Test Notes'))
    author = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE, verbose_name= ('Author'))
    field_user = models.ForeignKey(settings.AUTH_USER_MODEL,null = True, blank = True,on_delete=models.CASCADE, verbose_name= ('Field User'), related_name='field_user')
    lab_user = models.ForeignKey(settings.AUTH_USER_MODEL,null = True, blank = True, on_delete=models.CASCADE, verbose_name= ('Lab User'), related_name='lab_user')
    sms_status =  models.BooleanField(default = False, null=True, blank=True, verbose_name= ('SMS Sent'))
    result_datetime = models.DateTimeField(null=True, blank=True, verbose_name= ('Result Date'))
    updated_datetime = models.DateTimeField(auto_now = True, blank=True, verbose_name= ('Updated Date'))
    sample_datetime = models.DateTimeField(default=datetime.now, blank=True, verbose_name= ('Sampling Date'))
    
    def save(self, *args, **kwargs):
        img = qrcode.make(str(self.id)) 
        canvas = Image.new('RGB', (350,370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img)
        filename = "qr\\"+str(self.id) +".png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(filename, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("test_detail", kwargs={"pk": self.pk})

class SMSNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datatime = models.DateTimeField(default=datetime.now, blank=True, verbose_name= ('Created Data time'))
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    sent_timestamp = models.DateTimeField(auto_now_add=True)
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
    