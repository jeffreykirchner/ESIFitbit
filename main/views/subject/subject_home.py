from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from main.models import Session_subject,Session_day_subject_actvity,Session_day

def Subject_Home(request,id):
    logger = logging.getLogger(__name__) 
   
    
    # logger.info("some info")
    #u=request.user  

    session_subject = Session_subject.objects.get(login_key = id)
    session_day = session_subject.session.getCurrentSessionDay()

    logger.info(session_subject)

    if request.method == 'POST':     

        if session_subject:
            data = json.loads(request.body.decode('utf-8'))

            if data["action"] == "getSessionDaySubject":
                return getSessionDaySubject(data,session_subject,session_day)
            # elif data["action"] == "acceptInvitation":
            #     return acceptInvitation(data,u)
            # elif data["action"] == "cancelAcceptInvitation":
            #     return cancelAcceptInvitation(data,u)
            # elif data["action"] == "showAllInvitations":
            #     return showAllInvitations(data,u)
            # elif data["action"] == "acceptConsentForm":
            #     return acceptConsentForm(data,u)
        else:   
            logger.info("Session subject day, user not found: " + str(id))
            return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        
        heart_maintenance_minutes = session_subject.session.parameterset.heart_maintenance_minutes
        immune_maintenance_hours = session_subject.session.parameterset.immune_maintenance_minutes/60
        return render(request,'subject/home.html',{"id":id,
                                                   "heart_maintenance_minutes":heart_maintenance_minutes,
                                                   "immune_maintenance_hours": immune_maintenance_hours,
                                                   "session_subject":session_subject}) 

#get session subject day
def getSessionDaySubject(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    logger.info("Session subject day")
    logger.info(data)

    #mark subject checkin as true

    #pull data from fitbit

    #calc today's actvity
    session_subject.calcTodaysActivity(session_day.period_number)

    session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()
                
    return JsonResponse({"status":"success",
                        "session_day_subject_actvity" : session_day_subject_actvity.json(),},safe=False)                         
                                
     