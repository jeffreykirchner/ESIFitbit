from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from main.models import Session_subject,Session_day_subject_actvity,Session_day
from main.models import Parameters,Session_subject_questionnaire1,Session_subject_questionnaire2
from main.forms import Session_subject_questionnaire1_form,Session_subject_questionnaire2_form
from main.globals import todaysDate

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
            elif data["action"] == "payMe":
                return payMe(data,session_subject,session_day)
            elif data["action"] == "acceptConsentForm":
                return acceptConsentForm(data,session_subject)
            elif data["action"] == "submitQuestionnaire1":
                return submitQuestionnaire1(data,session_subject)
            elif data["action"] == "submitQuestionnaire2":
                return submitQuestionnaire2(data,session_subject)
           
        else:   
            logger.info("Session subject day, user not found: " + str(id))
            return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        p = Parameters.objects.first()

        #questionnaire 1 setup
        session_subject_questionnaire1_form = Session_subject_questionnaire1_form()

        session_subject_questionnaire1_form_ids=[]

        for f in session_subject_questionnaire1_form:
            session_subject_questionnaire1_form_ids.append(str(f.html_name))

        #questionnaire 2 setup
        session_subject_questionnaire2_form = Session_subject_questionnaire2_form()

        session_subject_questionnaire2_form_ids=[]

        for f in session_subject_questionnaire2_form:
            session_subject_questionnaire2_form_ids.append(str(f.html_name))

        return render(request,'subject/home.html',{"id":id,      
                                                   "before_start_date":session_subject.session.isBeforeStartDate(), 
                                                   "session_canceled":session_subject.session.canceled,
                                                   "session_started":session_subject.session.started,                                                   
                                                   "start_date":session_subject.session.getDateString(),    
                                                   "session_complete":session_subject.session.complete(),  
                                                   "session_subject_questionnaire1_form_ids":session_subject_questionnaire1_form_ids,
                                                   "session_subject_questionnaire1_form":session_subject_questionnaire1_form,
                                                   "session_subject_questionnaire2_form_ids":session_subject_questionnaire2_form_ids,
                                                   "session_subject_questionnaire2_form":session_subject_questionnaire2_form,  
                                                   "heart_help_text":p.heartHelpText,
                                                   "immune_help_text":p.immuneHelpText,
                                                   "payment_help_text":p.paymentHelpText,                       
                                                   "session_subject":session_subject}) 

#take pre session questionnaire
def submitQuestionnaire1(data,session_subject):
    logger = logging.getLogger(__name__) 
    logger.info("submitQuestionnaire1")
    logger.info(data)

    form_data_dict = {}

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    q = Session_subject_questionnaire1()
    q.session_subject = session_subject    

    form = Session_subject_questionnaire1_form(form_data_dict,instance=q)

    if form.is_valid():
        #print("valid form")                
        form.save()         
        q.save()  
        
        session_subject.questionnaire1_required=False
        session_subject.save()
            
        return JsonResponse({"status":"success",
                             "questionnaire1_required":session_subject.questionnaire1_required,},safe=False)                         
                                
    else:
        logger.info("Invalid questionnaire1 form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)

#take post session questionnaire
def submitQuestionnaire2(data,session_subject):
    logger = logging.getLogger(__name__) 
    logger.info("submitQuestionnaire2")
    logger.info(data)

    form_data_dict = {}

    for field in data["formData"]:            
        form_data_dict[field["name"]] = field["value"]

    q = Session_subject_questionnaire2()
    q.session_subject = session_subject    

    form = Session_subject_questionnaire2_form(form_data_dict,instance=q)

    if form.is_valid():
        #print("valid form")                
        form.save()         
        q.save()  
        
        session_subject.questionnaire2_required=False
        session_subject.save()
            
        return JsonResponse({"status":"success",
                             "questionnaire2_required":session_subject.questionnaire2_required,},safe=False)                         
                                
    else:
        logger.info("Invalid questionnaire2 form")
        return JsonResponse({"status":"fail","errors":dict(form.errors.items())}, safe=False)

#subject accepts consent form
def acceptConsentForm(data,session_subject):
    logger = logging.getLogger(__name__) 
    logger.info("acceptConsentForm")
    logger.info(data)

    session_subject.consent_required=False
    session_subject.consent_signature = data['consent_signature']
    session_subject.save()


    return JsonResponse({"consent_required":session_subject.consent_required,},safe=False)

#pay subject for today
def payMe(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    if session_day:
        logger.info(f"Pay subject: subject {session_subject.id} session day {session_day.id} date {session_day.date}")
    else:
        logger.info(f"Pay subject: subject {session_subject.id} session_day none")
    logger.info(data)

    p = Parameters.objects.first()

    session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

    status = "success"
    message = ""

    #check that session is not complete    
    if not session_day:
        status = "fail"  
        message = "Error: Session day not found"
        logger.info(message) 

    #check that session is not complete   
    if status == "success": 
        if not session_day.session.started:
            status = "fail"  
            message = "Error: Session not started"
            logger.info(message) 

    #check for consent form
    if status == "success":
        if p.consentFormRequired and session_subject.consent_required:
            status = "fail"   
            message = "Error: Consent required" 
            logger.info(message)
    
    #check that questionnaire two is done before last payment
    if status == "success":
        if p.questionnaire1Required and session_subject.getQuestionnaire1Required() :
            status = "fail"  
            message = "Error: Questionnaire 1 required"  
            logger.info(message)

    #check that session day activity exists
    if status == "success":
        if not session_day_subject_actvity:
            status = "fail" 
            message = "Error: Could not find session_day_subject_actvity"   
            logger.info(message)

    #check that it is the day of the specified session day
    if status == "success":
        if session_day_subject_actvity.session_day.date != todaysDate().date():
            status = "fail"  
            message = "Error: Session_day.date does not match today's date"  
            logger.info(message)   

    #check that session is not complete
    if status == "success":
        if session_day.session.complete():
            status = "fail"  
            message = "Error: Session is already complete"
            logger.info(message) 

    #check that session is not canceled
    if status == "success":
        if session_day.session.canceled:
            status = "fail"   
            message =  "Error: Session is canceled"
            logger.info(message)      

    #check that subject has not already been paid
    if status == "success":
        if session_day_subject_actvity.paypal_today:
            status="fail"
            message = "Error: Double payment attempt"
            logger.info(message)
    
    #check that questionnaire two is done before last payment
    if status == "success":
        if p.questionnaire2Required and session_subject.getQuestionnaire2Required() :
            status = "fail"  
            message = "Error: Questionnaire 2 required"  
            logger.info(message)
    
    if status == "success":
        try:
            session_day_subject_actvity.paypal_today=True
            session_day_subject_actvity.storeTodaysTotalEarnings()
            session_day_subject_actvity.save()
        except Exception  as e: 
            logger.info(e)
            status = "fail"
    
    if status == "success": 
        logger.info("Do PayPal")
        #add paypal code here
        pass

    return JsonResponse({"status":status,
                         "message":message,
                         "session_complete":session_subject.sessionComplete(),
                         "session_day_subject_actvity" :session_day_subject_actvity.json() if session_day_subject_actvity else {}},safe=False)

#get session subject day
def getSessionDaySubject(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    logger.info("Session subject day")
    logger.info(data)

    p = Parameters.objects.first()

    fitbitError=False
    status = "success"
    session_day_subject_actvity=None
    session_day_subject_actvity_previous_day=None

    if not session_day:
        status = "fail"
        logger.info("Session day not found.")

    if not session_subject:
        status = "fail"
        logger.info("Session subject not found.")
    
    if session_subject.session.complete():
        status = "fail"
        logger.info("The session is complete.")

    if status == "success":
        #check if subject missed past days
        session_subject.fitBitCatchUp()

        session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

        if session_day_subject_actvity:
            session_day_subject_actvity_previous_day = session_day_subject_actvity.getPreviousActivityDay()

        if session_day_subject_actvity_previous_day:
           
            #mark subject checkin as true
            session_day_subject_actvity.check_in_today=True
            session_day_subject_actvity.save()

            #pull data from fitbit
            fitbitError = session_day_subject_actvity_previous_day.pullFitbitActvities()

            #calc today's actvity
            session_subject.calcTodaysActivity(session_day.period_number)

            #get object again after calculation
            session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()
            session_day_subject_actvity_previous = session_day_subject_actvity.getPreviousActivityDay()

        else:
            #first day check for fitbit connection
            if status == "success":
                immune_activity_minutes = session_subject.getFibitImmuneMinutes(session_day.date)
                if immune_activity_minutes == -1:
                    fitbitError=True

    
    session_date = "--/--/----"
    session_last_day = False
        
    if session_day:       
        session_date = session_day.getDateStr()
        session_last_day = session_day.lastDay()

    consent_required = False

    if p.consentFormRequired and session_subject.consent_required:
        consent_required = True
        consent_form_text = p.consentForm
    else:
        consent_required = False
        consent_form_text=""

    if status == "fail":
        return JsonResponse({"status":status,
                             "questionnaire1_required":session_subject.getQuestionnaire1Required(),
                             "consent_required":consent_required,
                             "consent_form_text":consent_form_text,
                             },safe=False)
    else:
        return JsonResponse({"status":status,
                        "fitbitError":fitbitError,
                        "fitbit_link":session_subject.getFitBitLink("subject"),
                        "session_date":session_date,
                        "consent_required":consent_required,
                        "questionnaire1_required":session_subject.getQuestionnaire1Required(),
                        "questionnaire2_required":session_subject.getQuestionnaire2Required(),
                        "consent_form_text":consent_form_text,
                        "session_complete":session_subject.sessionComplete(),
                        "session_canceled":session_subject.session.canceled,
                        "session_last_day":session_last_day,
                        "session_day_subject_actvity" : session_day_subject_actvity.json(),
                        "session_day_subject_actvity_previous": session_day_subject_actvity_previous_day.json() if session_day_subject_actvity_previous_day else None,
                        "graph_parameters" : session_day.session.parameterset.json_graph(),},safe=False)                         
                                
     