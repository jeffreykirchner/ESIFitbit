from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from main.models import Session_subject

def Subject_Home(request,id):
    logger = logging.getLogger(__name__) 
   
    
    # logger.info("some info")
    #u=request.user  

    session_subject = Session_subject.objects.get(login_key = id)
    logger.info(session_subject)

    if request.method == 'POST':     

        if session_subject:
            data = json.loads(request.body.decode('utf-8'))

            if data["action"] == "getSessionDaySubject":
                return getSessionDaySubject(data,session_subject)
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
        
        return render(request,'subject/home.html',{"id":id,
                                                   "session_subject":session_subject}) 

#get session subject day
def getSessionDaySubject(data,session_subject):
    logger = logging.getLogger(__name__) 
    logger.info("Session subject day")
    logger.info(data)

    session_subject_day = ""
                  
    return JsonResponse({"status":"success",
                         "session_subject_day" : session_subject_day,},safe=False)                         
                                
     