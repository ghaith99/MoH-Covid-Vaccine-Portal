import json
import requests

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
