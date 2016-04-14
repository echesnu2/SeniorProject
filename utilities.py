import time
from time import mktime
from datetime import datetime
import requests as r


def combine_datetime(date, time_input):
    struct_datetime = time.strptime(date + ' ' + time_input, '%d %B, %Y %I:%M%p')
    final_datetime = datetime.fromtimestamp(mktime(struct_datetime))

    return final_datetime


def get_key(key_name):
    with open('C:/Users/Erik/PycharmProjects/SeniorProject/key.txt', 'r') as key_file:
        for line in key_file:
            if key_name in line:
                return line.split(':')[1].strip()
    return None


def send_email(recipient, subject, message, frm='ActivityMatchMaker@example.com'):
    key = get_key('mailgun_key')
    sandbox = get_key('mailgun_sandbox')
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)

    r.post(request_url, auth=('api', key), data={
        'from': frm,
        'to': recipient,
        'subject': subject,
        'text': message
    })
