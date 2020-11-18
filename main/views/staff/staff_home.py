from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from django.conf import settings

from main.globals.todaysDate import todaysDate

from main.models import Session,Parameterset,Session_day,Parameters

@login_required
def Staff_Home(request):
    logger = logging.getLogger(__name__) 
   
    
    # logger.info("some info")

    if request.method == 'POST':     


        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "createSession":
            return createSession(data)
        elif data["action"] == "deleteSession":
            return deleteSession(data)
        elif data["action"] == "getSessions":
             return getSessions(data)
           
        return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        
        return render(request,'staff/home.html',{"a":"a",
                                                   "b":"b"})     

#get list of experiment sessions
def getSessions(data):
    logger = logging.getLogger(__name__) 
    logger.info("Get Sessions")
    logger.info(data)

    return JsonResponse({"sessions" :[s.json() for s in  Session.objects.filter(soft_delete=False)],
                                },safe=False) 

#create new session
def createSession(data):
    logger = logging.getLogger(__name__) 
    logger.info("Create Session")
    logger.info(data)

    p = Parameters.objects.first()

    #create parameter set
    ps = Parameterset()
    ps.save()

    #create session
    s = Session()
    s.parameterset = ps
    s.invitation_text=p.invitationText
    s.invitation_text_subject=p.invitationTextSubject
    s.cancelation_text=p.cancelationText
    s.cancelation_text_subject=p.cancelationTextSubject
    s.start_date = todaysDate().date()
    s.calcEndDate()
    s.save()    

    #setup first session day
    sd = Session_day()
    sd.session=s
    sd.period_number = 1
    sd.save()

    return getSessions(data) 

#delete sesssion
def deleteSession(data):
    logger = logging.getLogger(__name__) 
    logger.info("Delete Session")
    logger.info(data)

    id = data["id"] 

    s = Session.objects.get(id=id)

    if settings.DEBUG==True:
        s.delete()
    else:
        s.soft_delete=True
        s.save()

    return getSessions(data) 

