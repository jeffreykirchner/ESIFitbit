from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging

from main.forms import Parameterset_form
from main.models import Session,Parameterset,Session_subject,Session_day_subject_actvity

@login_required
def Staff_Session(request,id):
    logger = logging.getLogger(__name__) 
   
    
    # logger.info("some info")

    if request.method == 'POST':     


        data = json.loads(request.body.decode('utf-8'))

        if data["action"] == "getSession":
            return getSession(data,id)
        elif data["action"] == "deleteSubject":
            return deleteSubject(data,id)
        elif data["action"] == "addSubject":
            return addSubject(data,id)
        elif data["action"] == "updateParameters":
            return updateParameters(data,id)
           
        return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        
        parameterset_form = Parameterset_form()
        return render(request,'staff/session.html',{'id': id,
                                                    'parameterset_form':parameterset_form})     

#get list of experiment sessions
def getSession(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Get Session")
    logger.info(data)

    return JsonResponse({"session" : getSessionJSON(id),
                         "session_subjects": getSubjectListJSON(id), 
                                },safe=False)  

#get session json object
def getSessionJSON(id):
    logger = logging.getLogger(__name__) 
    logger.info("Get Session JSON")

    s=Session.objects.get(id=id)

    return s.json()

#get subject list json object
def getSubjectListJSON(id):
    logger = logging.getLogger(__name__) 
    logger.info("Get Subject List JSON")
    
    s=Session.objects.get(id=id)
    ss = s.session_subjects.filter(soft_delete = False)

    return  [i.json() for i in ss]

#add new subject to the session
def addSubject(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Add Subject")
    logger.info(data)

    s=Session.objects.get(id=id)

    ss = Session_subject()
    ss.session=s
    ss.save()

    sda = Session_day_subject_actvity()
    sda.session_subject = ss
    sda.session_day = s.session_days.filter(period_number = 1).first()
    sda.check_in_today = True
    sda.heart_activity_minutes = -1
    sda.immune_activity_minutes = -1
    sda.heart_activity = s.parameterset.heart_activity_inital
    sda.immune_activity = s.parameterset.immune_activity_inital
    sda.save()    

    return JsonResponse({"session_subjects": getSubjectListJSON(id), 
                                },safe=False) 

#remove subject from session
def deleteSubject(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Delete Subject")
    logger.info(data)

    ss_id = data["id"] 

    ss =  Session_subject.objects.get(id=ss_id)
    ss.soft_delete=True
    ss.save()

    # s = Session.objects.get(id=id)
    # s.softDelete=True
    # s.save()

    return JsonResponse({"session_subjects": getSubjectListJSON(id), 
                                },safe=False) 

def updateParameters(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Update parameters")
    logger.info(data)

    form_data_dict = {}

    s=Session.objects.get(id=id)

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    form = Parameterset_form(form_data_dict,instance=s.parameterset)

    if form.is_valid():
        #print("valid form")                
        form.save()               
        return JsonResponse({"status":"success","session" : getSessionJSON(id),},safe=False)                         
                                
    else:
        logger.info("Invalid parameterset form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)
    

    


