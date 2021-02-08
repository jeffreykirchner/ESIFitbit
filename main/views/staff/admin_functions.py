from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from django.conf import settings

from main.globals import todaysDate
from datetime import datetime,timedelta

from main.models import Session_day_subject_actvity,Parameters

@login_required
def Admin_functions(request):
    logger = logging.getLogger(__name__) 
    
    # logger.info("some info")

    if request.method == 'POST':     

        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "backFillSleep":
            return backFillSleep(data)
                  
        return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        p = Parameters.objects.first()

        return render(request,'staff/adminFunctions.html',{'help_text': ""})     

#back fill missing sleep time series
def backFillSleep(data):
    logger = logging.getLogger(__name__) 
    logger.info("Back Fill Sleep")
    logger.info(data)

    errors="Success"

    try:
        d_today =  todaysDate() - timedelta(days=1)
        session_id = data["backFillSleepSessionId"]

        sda_qs = Session_day_subject_actvity.objects.filter(session_day__session__id = session_id)\
                                                    .filter(session_day__date__lte = d_today.date())\
                                                    .filter(fitbit_immune_time_series = "")

        for i in sda_qs:
            #self.fitbit_immune_time_series = self.session_subject.getFitbitSleep(self.session_day.date)
            i.fitbit_immune_time_series = i.session_subject.getFitbitSleep(i.session_day.date)
            i.save()

    except Exception  as e: 
        logger.warning(e)
        errors = str(e)

    return JsonResponse({"errors" : errors,},safe=False)
                                 

