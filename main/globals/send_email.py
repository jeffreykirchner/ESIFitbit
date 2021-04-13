
'''
send email via ESI mass email service
'''
import logging
import requests

from django.conf import settings

def send_mass_email_service(user_list, message_subject, message_text, memo):
    '''
    send mass email through ESI mass pay service
    user_list : [{email:email, variables:[{name:text},{name:text}}, ]
    message_subject : string subject header of message
    message_text : string message template, variables : [name]
    memo : string note about message's purpose
    '''

    data = {"user_list" : user_list,
            "message_subject" : message_subject,
            "message_text" : message_text,
            "memo" : memo}

    logger = logging.getLogger(__name__)
    logger.info(f"ESI mass email API: users: {user_list}, message_subject : {message_subject}, message_text : {message_text}")

    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}

    request_result = requests.post(f'{settings.EMAIL_MS_HOST}/send-email/',
                        json=data,
                        auth=(str(settings.EMAIL_MS_USER_NAME), str(settings.EMAIL_MS_PASSWORD)),
                        headers=headers)

    logger.info(f"ESI mass email API response: {request_result.json()}")

    return request_result.json()