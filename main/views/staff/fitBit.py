from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

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

    if not "code" in request.GET:
        status="fail"
    else:

        try:
            logger.info("Register Fitbit, Code: " + request.GET["code"]) 
            logger.info("Register Fitbit, State: " + request.GET["state"]) 
            u=request.user       

            headers = {'Authorization': 'Basic ' + str(settings.FITBIT_AUTHORIZATION),
                        'Content-Type' : 'application/x-www-form-urlencoded'}
            
            data = {'clientId': str(settings.FITBIT_CLIENT_ID),
                    'grant_type' : 'authorization_code',   
                    'redirect_uri' : 'http://localhost:8000/fitBit/',
                    'code': request.GET["code"]}


            r = requests.post('https://api.fitbit.com/oauth2/token', headers=headers,data=data).json()

            logger.info("Register Fitbit, Response: ") 
            logger.info(r)

            if 'access_token' in r:
                # u.profile.fitBitAccessToken = r['access_token']
                # u.profile.fitBitRefreshToken = r['refresh_token']
                # u.profile.fitBitUserId = r['user_id']

                # u.save()

                pass
            else:
                status="fail"        
        
        except Exception as e:
            logger.error("fitBit registration: " + str(e))
            logger.error(traceback.format_exc())
            status="fail"
    
    logger.info("Register Fitbit, Status: " + status) 

    return render(request,'staff/fitBit.html',{'status':status})

    



