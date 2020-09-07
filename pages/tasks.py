from celery import task
from django.core.mail import send_mail
import json
import requests
from .models import Patient, Test 

# @task
# def order_created(order_id):
#     """
#     Task to send an e-mail notification when an order is
#     successfully created.
#     """
#     order = Order.objects.get(id=order_id)
#     subject = f'Order nr. {order.id}'
#     message = f'Dear {order.first_name},\n\n' \
#               f'You have successfully placed an order.' \
#               f'Your order ID is {order.id}.'
#     mail_sent = send_mail(subject,
#                           message,
#                           'admin@myshop.com',
#                           [order.email])
#     return mail_sent

@task
def send_sms(queryset, size):
    print('received', queryset)
    for chunk in generate_chunks(queryset, size):
        r = requests.post(
           'https://trxnc.future-club.com/JsonRestAPI/SendSMSService.svc/sendsmsrest',
           headers={'content-type': 'application/json'},
           data=json.dumps({
               'sendSmsDTOs': [{
                   'D': '965{}'.format(x.test.patient.phone),
                   'L': 'E',
                   'M': x.message,
                   'P': '1503',
                   'Pr': 1,
                   'S': 'MOH',
                   'T': 'T1231231',
                   'U': 'Moh_usr'
               } for x in chunk]
           })
        )
        print(r.content)


def generate_chunks(iterable, size):
    for i in range(0, len(iterable), size):
        yield(iterable[i:i+size])
