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
           
        else:   
            logger.info("Session subject day, user not found: " + str(id))
            return JsonResponse({"response" :  "fail"},safe=False)       
    else:      
        
        heart_maintenance_minutes = session_subject.session.parameterset.heart_maintenance_minutes
        immune_maintenance_hours = session_subject.session.parameterset.immune_maintenance_minutes/60

        session_date = session_day.getDateStr()        

        return render(request,'subject/home.html',{"id":id,
                                                   "heart_maintenance_minutes":heart_maintenance_minutes,
                                                   "immune_maintenance_hours": immune_maintenance_hours,
                                                   "session_date":session_date,
                                                   "session_subject":session_subject}) 

#get session subject day
def getSessionDaySubject(data,session_subject,session_day):
    logger = logging.getLogger(__name__) 
    logger.info("Session subject day")
    logger.info(data)

    session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()

    session_day_subject_actvity_previous_day = session_day_subject_actvity.getPreviousActivityDay()

    if session_day_subject_actvity_previous_day:
        #create session day if needed
        session_subject.session.addNewSessionDays()

        #mark subject checkin as true
        session_day_subject_actvity.check_in_today=True
        session_day_subject_actvity.save()
        
        #pull data from fitbit
        # immune_activity_minutes = session_subject.getFibitImmuneMinutes(session_day.getPreviousSessionDay().date)
        # heart_activity_minutes = session_subject.getFibitHeartMinutes(session_day.getPreviousSessionDay().date)

        # if immune_activity_minutes:
        #     session_day_subject_actvity_previous_day.immune_activity_minutes = immune_activity_minutes
        
        # if heart_activity_minutes:
        #     session_day_subject_actvity_previous_day.heart_activity_minutes = heart_activity_minutes

        session_day_subject_actvity_previous_day.save()

        #calc today's actvity
        session_subject.calcTodaysActivity(session_day.period_number)

        #get object again after calculation
        session_day_subject_actvity = Session_day_subject_actvity.objects.filter(session_subject = session_subject,session_day=session_day).first()
        session_day_subject_actvity_previous = session_day_subject_actvity.getPreviousActivityDay()

    return JsonResponse({"status":"success",
                        "session_day_subject_actvity" : session_day_subject_actvity.json(),
                        "session_day_subject_actvity_previous": session_day_subject_actvity_previous.json() if session_day_subject_actvity_previous else None,
                        "graph_parameters" : session_day.session.parameterset.json_graph(),},safe=False)                         
                                
     