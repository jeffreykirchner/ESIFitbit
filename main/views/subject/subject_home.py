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

       
        # #u=User.objects.get(id=11330)  #tester

        # data = json.loads(request.body.decode('utf-8'))

        # if data["action"] == "getCurrentInvitations":
        #     return getCurrentInvitations(data,u)
        # elif data["action"] == "acceptInvitation":
        #     return acceptInvitation(data,u)
        # elif data["action"] == "cancelAcceptInvitation":
        #     return cancelAcceptInvitation(data,u)
        # elif data["action"] == "showAllInvitations":
        #     return showAllInvitations(data,u)
        # elif data["action"] == "acceptConsentForm":
        #     return acceptConsentForm(data,u)
           
        return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        
        return render(request,'subject/home.html',{"a":"a",
                                                   "b":"b"})      