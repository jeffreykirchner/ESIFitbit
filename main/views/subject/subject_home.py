from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
import logging
from main.models import Session_subject,Session_day_subject_actvity,Session_day,Parameters

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
           
        else:   
            logger.info("Session subject day, user not found: " + str(id))
            return JsonResponse({"response" :  "fail"},safe=False)       
    else:      

        return render(request,'subject/home.html',{"id":id,      
                                                   "before_start_date":session_subject.session.isBeforeStartDate(), 
                                                   "session_started":session_subject.session.started, 
                                                   "start_date":session_subject.session.getDateString(),                                
                                                   "session_subject":session_subject}) 

#subject accepts consent form
def acceptConsentForm(data,session_subject):
    logger = logging.getLogger(__name__) 
    logger.info("acceptConsentForm")
    logger.info(data)

    session_subject.consent_required=False
    session_subject.save()


    return JsonResponse({"consent_required":session_subject.consent_required,},safe=False)

#pay subject for today
def payMe(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    logger.info(f"Pay subject: subject {session_subject.id} session day {session_day.id} date {session_day.date}")
    logger.info(data)

    p = Parameters.objects.first()

    session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

    status = "success"

    if p.consentFormRequired and session_subject.consent_required:
        status = "fail"    
        logger.info("Consent required")

    if not session_day_subject_actvity:
        status = "fail"    
        logger.info("Could not find session_day_subject_actvity")
    
    if status == "success":
        if session_day_subject_actvity.paypal_today:
            status="fail"
            logger.info("Error: Double payment attempt")
    
    if status == "success":
        try:
            session_day_subject_actvity.paypal_today=True
            session_day_subject_actvity.save()
        except Exception  as e: 
            logger.info(e)
            status = "fail"
    
    if status == "success": 
        logger.info("Do PayPal")
        #add paypal code here
        pass

    return JsonResponse({"status":status,
                         "session_day_subject_actvity" : session_day_subject_actvity.json()},safe=False)


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

    if status == "success":
        #check if subject missed past days
        session_subject.fitBitCatchUp()

        session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

        if session_day_subject_actvity:
            session_day_subject_actvity_previous_day = session_day_subject_actvity.getPreviousActivityDay()
    

        if session_day_subject_actvity_previous_day:
            #create session day if needed

            #mark subject checkin as true
            session_day_subject_actvity.check_in_today=True
            session_day_subject_actvity.save()

            #pull data from fitbit
            fitbitError = session_day_subject_actvity_previous_day.pullFitbitActvities()

            # #calc today's actvity
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
        
    if session_day:       
        session_date = session_day.getDateStr()

    consent_required = False

    if p.consentFormRequired and session_subject.consent_required:
        consent_required = True
        consent_form_text = p.consentForm
    else:
        consent_required = False
        consent_form_text=""

    return JsonResponse({"status":status,
                        "fitbitError":fitbitError,
                        "session_date":session_date,
                        "consent_required":consent_required,
                        "consent_form_text":consent_form_text,
                        "session_day_subject_actvity" : session_day_subject_actvity.json() if session_day_subject_actvity else None,
                        "session_day_subject_actvity_previous": session_day_subject_actvity_previous_day.json() if session_day_subject_actvity_previous_day else None,
                        "graph_parameters" : session_day.session.parameterset.json_graph() if session_day else None,},safe=False)                         
                                
     