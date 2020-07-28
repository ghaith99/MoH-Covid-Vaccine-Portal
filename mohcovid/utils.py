#from ../pages/models import SMSNotification

from celery import shared_task

@shared_task
def checkandSendSMS():
    print("sms done")