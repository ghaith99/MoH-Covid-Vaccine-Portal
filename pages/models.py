from django.db import models
from datetime import datetime
from users.models import CustomUser
from django.urls import reverse


class Test(models.Model):
    datatime = models.DateTimeField(default=datetime.now, blank=True)
    lastModified = models.DateTimeField(auto_now = True, blank=True)
    resultDate = models.DateTimeField(null=True, blank=True)
    testNotes =  models.TextField()
    testResult =  models.NullBooleanField(choices=((None,''), (True,'Yes'), (False, 'No')),max_length=3, blank=True, null=True, default=None,)
    author = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE,)
    
    def get_absolute_url(self):
        return reverse("test_detail", kwargs={"pk": self.pk})

class Citizen(models.Model):
    city = models.CharField(max_length = 25)
    gender = models.CharField(max_length = 25)
    civilID = models.CharField(max_length = 25)
    civilSerial = models.CharField(max_length = 25)
    dob =  models.DateTimeField(null=True, blank=True)
    first  = models.CharField(max_length = 25)
    last = models.CharField(max_length = 25)

    
