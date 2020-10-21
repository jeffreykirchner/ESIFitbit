from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from main.models import Session,Session_subject

import requests
import logging
import traceback

from django.conf import settings

#user account info
@login_required
def fitBit(request):
    logger = logging.getLogger(__name__)  
    logger.info("FitBit Connect")   
    status="success"

    fitBit_response = ""
    fitBit_error = ""
    session_subject = None
    session = None
    subject_id = None
    session_id = None

    if not "code" in request.GET:
        status="fail"
    else:

        try:
            logger.info("Register Fitbit, Code: " + request.GET["code"]) 
            logger.info("Register Fitbit, State: " + request.GET["state"]) 

            state_info = request.GET["state"].split(";")
            subject_id = state_info[0]
            session_id = state_info[1]

            session_subject = Session_subject.objects.get(id=subject_id)

            headers = {'Authorization': 'Basic ' + str(settings.FITBIT_AUTHORIZATION),
                        'Content-Type' : 'application/x-www-form-urlencoded'}
            
            data = {'clientId': str(settings.FITBIT_CLIENT_ID),
                    'grant_type' : 'authorization_code',   
                    'redirect_uri' : 'http://localhost:8000/fitBit/',
                    'code': request.GET["code"]}


            fitBit_response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers,data=data).json()

            logger.info("Register Fitbit, Response: ") 
            logger.info(fitBit_response)

            if 'access_token' in fitBit_response:
                session_subject.fitBitAccessToken = fitBit_response['access_token']
                session_subject.fitBitRefreshToken = fitBit_response['refresh_token']
                session_subject.fitBitUserId = fitBit_response['user_id']

                session_subject.save()
            else:
                status="fail"        
        
        except Exception as e:
            fitBit_error = str(e)
            logger.error("fitBit registration: " + fitBit_error)
            logger.error(traceback.format_exc())
            status="fail"
    
    logger.info("Register Fitbit, Status: " + status) 

    if session_id :
        session = Session.objects.get(id = session_id)

    return render(request,'staff/fitBit.html',{'status':status,
                                               'fitBit_response':fitBit_response, 
                                               'fitBit_error':fitBit_error,
                                               'session_subject':session_subject,
                                               'session': session,})

    



