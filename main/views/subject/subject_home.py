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
            elif data["action"] == "payMe":
                return payMe(data,session_subject,session_day)
           
        else:   
            logger.info("Session subject day, user not found: " + str(id))
            return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
               
        session_date = session_day.getDateStr()        

        return render(request,'subject/home.html',{"id":id,           
                                                   "session_started":session_subject.session.started, 
                                                   "start_date":session_subject.session.getDateString(),                                
                                                   "session_date":session_date,
                                                   "session_subject":session_subject}) 

#pay subject for today
def payMe(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    logger.info(f"Pay subject: subject {session_subject.id} session day {session_day.id} date {session_day.date}")
    logger.info(data)

    session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

    status = "success"

    if not session_day_subject_actvity:
        status = "fail"    
        logger.info("Could not find session_day_subject_actvity")
    
    if status == "success":
        try:
            session_day_subject_actvity.paypal_today=True
            session_day_subject_actvity.save()
        except Exception  as e: 
            logger.info(e)
            status = "fail"
    
    if status == "success": 
        #add paypal code here
        pass

    return JsonResponse({"status":status,
                         "session_day_subject_actvity" : session_day_subject_actvity.json()},safe=False)

#get session subject day
def getSessionDaySubject(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    logger.info("Session subject day")
    logger.info(data)

    fitbitError=False

    session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

    session_day_subject_actvity_previous_day = session_day_subject_actvity.getPreviousActivityDay()

    if session_day_subject_actvity_previous_day:
        #create session day if needed
        #session_subject.session.addNewSessionDays()

        #mark subject checkin as true
        session_day_subject_actvity.check_in_today=True
        session_day_subject_actvity.save()
        
        #pull data from fitbit
        immune_activity_minutes = session_subject.getFibitImmuneMinutes(session_day.getPreviousSessionDay().date)
        heart_activity_minutes = session_subject.getFibitHeartMinutes(session_day.getPreviousSessionDay().date)

        if immune_activity_minutes >= 0:
            session_day_subject_actvity_previous_day.immune_activity_minutes = immune_activity_minutes
        else:
            logger.info(f"immune_activity_minutes not found: session subject {session_subject} session day {session_day}")
            fitbitError=True
        
        if heart_activity_minutes >= 0:
            session_day_subject_actvity_previous_day.heart_activity_minutes = heart_activity_minutes
        else:
            logger.info(f"heart_activity_minutes not found: session subject {session_subject} session day {session_day}")
            fitbitError=True

        session_day_subject_actvity_previous_day.save()

        #calc today's actvity
        session_subject.calcTodaysActivity(session_day.period_number)

        #get object again after calculation
        session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()
        session_day_subject_actvity_previous = session_day_subject_actvity.getPreviousActivityDay()

    else:
        #first day check for fitbit connection
        immune_activity_minutes = session_subject.getFibitImmuneMinutes(session_day.date)
        if immune_activity_minutes == -1:
            fitbitError=True

    return JsonResponse({"status":"success",
                        "fitbitError":fitbitError,
                        "session_day_subject_actvity" : session_day_subject_actvity.json(),
                        "session_day_subject_actvity_previous": session_day_subject_actvity_previous_day.json() if session_day_subject_actvity_previous_day else None,
                        "graph_parameters" : session_day.session.parameterset.json_graph(),},safe=False)                         
                                
     