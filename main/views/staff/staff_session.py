from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from django.db.models.functions import Lower
from datetime import datetime,timedelta
from main.globals.randomHexColor import getRandomHexColor
from main.globals.todaysDate import todaysDate

from main.forms import Parameterset_form,Session_form,Subject_form,Import_parameters_form
from main.models import Session,Parameterset,Session_subject,Session_day_subject_actvity,Parameters

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
        elif data["action"] == "updateSession":
            return updateSession(data,id)
        elif data["action"] == "updateSubject":
            return updateSubject(data,id)
        elif data["action"] ==  "showFitbitStatus":
            return showFitbitStatus(data,id)
        elif data["action"] ==  "importParameters":
            return importParameters(data,id)
        elif data["action"] == "backFillSessionDays":
            return backFillSessionDays(data,id)
        elif data["action"] == "startSession":
            return startSession(data,id)
        elif data["action"] == "sendInvitations":
            return sendInvitations(data,id)
        elif data["action"] == "downloadData":
            return downloadData(data,id)
        elif data["action"] == "sendCancelations":
            return sendCancelations(data,id)
        elif data["action"] == "refreshSubjectTable":
            return refreshSubjectTable(data,id)
        elif data["action"] == "downloadEarnings":
            return downloadEarnings(data,id)
           
        return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        
        parameterset_form = Parameterset_form()
        session_form = Session_form()
        subject_form = Subject_form()
        import_parameters_form = Import_parameters_form()
        p = Parameters.objects.first()
        yesterdays_date = todaysDate() - timedelta(days=1)
        
        return render(request,'staff/session.html',{'id': id,
                                                    'parameterset_form':parameterset_form,
                                                    'session_form':session_form,
                                                    'subject_form':subject_form,
                                                    'help_text': p.manualHelpText,
                                                    'import_parameters_form':import_parameters_form,
                                                    'yesterdays_date' : yesterdays_date.date().strftime("%Y-%m-%d")})     

#get list of experiment sessions
def getSession(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Get Session")
    logger.info(data)

    s=Session.objects.get(id=id)

    return JsonResponse({"session" : getSessionJSON(id),
                         "session_subjects": getSubjectListJSON(id,False), 
                         "graph_parameters" : s.parameterset.json_graph(),
                                },safe=False)  

#get session json object
def getSessionJSON(id):
    logger = logging.getLogger(__name__) 
    logger.info("Get Session JSON")

    s=Session.objects.get(id=id)

    return s.json()

#get subject list json object
def getSubjectListJSON(id,get_fitbit_status):
    logger = logging.getLogger(__name__) 
    logger.info("Get Subject List JSON")
    
    s=Session.objects.get(id=id)
    ss = s.session_subjects.filter(soft_delete = False).order_by(Lower('name'))

    return  [i.json(get_fitbit_status,"staff") for i in ss]

#add new subject to the session
def addSubject(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Add Subject")
    logger.info(data)

    s=Session.objects.get(id=id)

    if not s.started:
        ss = Session_subject()
        ss.session=s
        ss.display_color = getRandomHexColor()
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

    return JsonResponse({"session_subjects": getSubjectListJSON(id,False),
                         "session" : getSessionJSON(id), 
                                },safe=False) 

#refresh subject table
def refreshSubjectTable(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Refresh subject table")
    logger.info(data)

    return JsonResponse({"session_subjects": getSubjectListJSON(id,False),
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

    return JsonResponse({"session_subjects": getSubjectListJSON(id,False), 
                                },safe=False) 

#update session parameters
def updateParameters(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Update parameters")
    logger.info(data)

    form_data_dict = {}

    s=Session.objects.get(id=id)

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    if not s.editable():
        form_data_dict["block_1_day_count"] = s.parameterset.block_1_day_count
        form_data_dict["block_2_day_count"] = s.parameterset.block_2_day_count
        form_data_dict["block_3_day_count"] = s.parameterset.block_3_day_count

    form = Parameterset_form(form_data_dict,instance=s.parameterset)

    if form.is_valid():
        #print("valid form")                
        form.save()           
        s.calcEndDate()
            
        return JsonResponse({"status":"success","session" : getSessionJSON(id),},safe=False)                         
                                
    else:
        logger.info("Invalid parameterset form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)

#update session settings
def updateSession(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Update session")
    logger.info(data)

    form_data_dict = {}

    s=Session.objects.get(id=id)

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    if not s.editable():
        form_data_dict["start_date"] = s.getDateString()

    form = Session_form(form_data_dict,instance=s)

    if form.is_valid():
        #print("valid form")                
        form.save()              

        #set first session day date to start date
        sd = s.session_days.order_by('-date').first()
        sd.date=s.start_date
        sd.save()

        s.calcEndDate()

        return JsonResponse({"status":"success","session" : getSessionJSON(id),},safe=False)                         
                                
    else:
        logger.info("Invalid session form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)

#back fill session with data for testing
def backFillSessionDays(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Back fill session days with random data")
    logger.info(data)

    s=Session.objects.get(id=id)

    #fill with test data
    if s.started:
        s.fillWithTestData()

    return JsonResponse({"session" : getSessionJSON(id),
                         "session_subjects": getSubjectListJSON(id,False), 
                                },safe=False)

#activate session and fill in session days
def startSession(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Start session")
    logger.info(data)

    status = "success"

    s=Session.objects.get(id=id)

    #check for subjects in session before starting
    if s.session_subjects.all():

        if s.started==False:
            s.addNewSessionDays()
            s.assignSubjectIdNumbers()

        s.calcEndDate()
        s.started=True
        s.save()
    else:
        status = "fail"

    return JsonResponse({"session" : getSessionJSON(id), 
                         "status":status,   
                                },safe=False)

#send invitations to subjects
def sendInvitations(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Send invitations")
    logger.info(data)

    success=True

    s=Session.objects.get(id=id)

    s.invitation_text_subject = data["invitation_text_subject"]
    s.invitation_text = data["invitation_text"]

    s.save()

    result = ""

    try:
        result = s.sendInvitations()

        if result['errorMessage'] != "":
            s.invitations_sent=False
        else:
            s.invitations_sent=True
        s.save()
    except Exception  as e: 
        logger.info(e)
        result = e
        success = False   

    return JsonResponse({"success" : success,
                         "result" : result,
                         "session" : getSessionJSON(id), 
                                },safe=False)

#send invitations to subjects
def sendCancelations(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Send cancelation")
    logger.info(data)

    success=True

    s=Session.objects.get(id=id)

    s.cancelation_text_subject = data["cancelation_text_subject"]
    s.cancelation_text = data["cancelation_text"]

    s.save()

    result = ""

    try:
        result = s.sendCancelation()

        if result['errorMessage'] != "":
            s.canceled=False
        else:
            s.canceled=True
        s.save()
    except Exception  as e: 
        logger.info(e)
        result = str(e)
        success = False   

    return JsonResponse({"success" : success,
                         "result" : result,
                         "session" : getSessionJSON(id), 
                                },safe=False)

#import parameterset from another session
def importParameters(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Import Parameters")
    logger.info(data)

    form_data_dict = {}

    s=Session.objects.get(id=id)

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    form = Import_parameters_form(form_data_dict)

    if form.is_valid():
        logger.info(form.cleaned_data['session'])
        ps = form.cleaned_data['session'].parameterset
        s.parameterset.setup(ps)               
        return JsonResponse({"status":"success","session" : getSessionJSON(id),},safe=False)                         
                                
    else:
        logger.info("Invalid session form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)

#update subject settings
def updateSubject(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Update subject")
    logger.info(data)

    form_data_dict = {}

    ss_id =  data["ss_id"]

    ss=Session_subject.objects.get(id=ss_id)

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    form = Subject_form(form_data_dict,instance=ss)

    if form.is_valid():
        #print("valid form")                
        form.save()               
        return JsonResponse({"status":"success","session_subjects": getSubjectListJSON(id,False), },safe=False)                         
                                
    else:
        logger.info("Invalid session form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)
    
#update subject settings
def showFitbitStatus(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Show fitbit status")
    logger.info(data)
            
    return JsonResponse({"status":"success","session_subjects": getSubjectListJSON(id,True), },safe=False)                         

#download session data
def downloadData(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Download data")
    logger.info(data)

    s=Session.objects.get(id=id)

    return s.getCSVResponse()    

#download session earnings
def downloadEarnings(data,id):
    logger = logging.getLogger(__name__) 
    logger.info("Download data")
    logger.info(data)

    s=Session.objects.get(id=id) 

    return s.getCSVEarnings(data["date"])


