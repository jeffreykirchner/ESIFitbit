'''
PPMS
'''
from decimal import Decimal

import logging
import requests

from django.conf import settings

# from main.models import Parameters

def do_ppms(payments_list, payment_id, email_subject):
    '''
    make paypal mass payment through the ppms
    PPMS_HOST, PPMS_USER_NAME, PPMS_PASSWORD defined in settings
    payments_list : dict {"email":__,"amount":__,"note":__,"memo":__}
    '''

    logger = logging.getLogger(__name__)

    # parm = Parameters.objects.first()

    payments = []

    #build payments json
    for payment in payments_list:
        payments.append({"email": payment["email"], #, 'sb-8lqqw5080618@business.example.com'
                         "amount" : float(payment["amount"]),
                         "note" : payment["note"],
                         "memo" : payment["memo"]})

    data = {}
    data["info"] = {"payment_id" : f'{settings.PPMS_USER_NAME}_{payment_id}', #, random.randrange(0, 99999999)
                    "email_subject" : email_subject}

    data["items"] = payments

    logger.info(f"PayPal API Payments input: {data}")

    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}

    req = requests.post(f'{settings.PPMS_HOST}/payments/',
                        json=data,
                        auth=(str(settings.PPMS_USER_NAME), str(settings.PPMS_PASSWORD)),
                        headers=headers)

    logger.info(f"PayPal API Payments response: {req.json()}")

    error_message = ""
    result = ""

    if req.status_code == 401 or req.status_code == 403:
        error_message = "Authentication Error"
    elif req.status_code == 409:        
        error_message = "A mass payment has already been submitted for this session day."
    elif req.status_code != 201:
        error_message = "<div>The payments were not made because of the following errors:</div>"
        for payment in req.json():
            error_message += f'<div>{payment["data"]["email"]}: {payment["detail"]}</div>'
    else:        
        error_message = "Payments complete"
        # for payment in req.json():
        #     result += f'<div>{payment["email"]}: ${float(payment["amount"]):0.2f}</div>'
    
    return {"result" : req.json(), "error_message" : error_message}