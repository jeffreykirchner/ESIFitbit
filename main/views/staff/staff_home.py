from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging

from main.models import Session,Parameterset,Session_day

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

    return JsonResponse({"sessions" :[s.json() for s in  Session.objects.filter(softDelete=False)],
                                },safe=False) 

#create new session
def createSession(data):
    logger = logging.getLogger(__name__) 
    logger.info("Create Session")
    logger.info(data)

    #create parameter set
    p = Parameterset()
    p.save()

    #create session
    s = Session()
    s.parameterset = p
    s.save()    

    #setup first session day
    sd = Session_day()
    sd.session=s
    sd.period_number = 1
    sd.save()

    return getSessions(data) 


def deleteSession(data):
    logger = logging.getLogger(__name__) 
    logger.info("Delete Session")
    logger.info(data)

    id = data["id"] 

    s = Session.objects.get(id=id)
    s.softDelete=True
    s.save()

    return getSessions(data) 

