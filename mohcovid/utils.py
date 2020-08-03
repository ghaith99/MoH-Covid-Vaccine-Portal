# from ../pages/models import SMSNotification

import json
import requests

from pages.models import Test

from celery import shared_task


@shared_task
def send_sms(pk, language='E'):
    test = Test.objects.select_related('patient').get(pk=pk)
    msg = 'Good evening {}, your test result is {}'.format(
        test.patient.first_name,
        test.test_result
    )
    body = {
       'sendSmsDTOs': [{
           'D': '965{}'.format(test.patient.phone),
           'L': language,
           'M': msg,
           'P': '1503',
           'Pr': 1,
           'S': 'MOH',
           'T': 'T1231231',
           'U': 'Moh_usr',
       }]
    }
    requests.post(
       'https://trxnc.future-club.com/JsonRestAPI/SendSMSService.svc/sendsmsrest',
       headers={'content-type': 'application/json'},
       data=json.dumps(body)
    )
