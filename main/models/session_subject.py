from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session,Parameters
import uuid
from django.conf import settings
import requests
from datetime import datetime,timedelta,timezone,date
import pytz
import random
import main
from main.globals import todaysDate

#subject in session
class Session_subject(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_subjects")

    login_key = models.UUIDField(default=uuid.uuid4, editable=False,verbose_name = 'Login Key')                         #log in key used to ID subject for URL login
    name = models.CharField(max_length = 300,default = 'Subject Name', verbose_name = 'Subject Name')                   #subject name 
    contact_email = models.CharField(max_length = 300,default = 'Subject Email',verbose_name = 'Subject Email')         #contact email address
    student_id = models.CharField(max_length = 300,default = 'Student ID Number',verbose_name = 'Student ID Number')    #student ID number
    gmail_address = models.CharField(max_length = 300,default = 'Gmail Address',verbose_name = 'Gmail Address')         #gmail address asigned to subject for experiment 
    gmail_password = models.CharField(max_length = 300,default = 'Gmail Password',verbose_name = 'Gmail Password')      #password for above 
    
    consent_required = models.BooleanField(default=True)          #true if subject has done consent form    
    questionnaire1_required = models.BooleanField(default=True)   #pre experiment questionnaire
    questionnaire2_required = models.BooleanField(default=True)   #post experiment questionnaire                                                 

    #fitbit    
    fitBitAccessToken = models.CharField(max_length=1000, default="",verbose_name = 'FitBit Access Token')
    fitBitRefreshToken = models.CharField(max_length=1000, default="",verbose_name = 'FitBit Refresh Token')
    fitBitUserId = models.CharField(max_length=100, default="",verbose_name = 'FitBit User ID')  

    soft_delete =  models.BooleanField(default=False)                                                 #hide subject if true

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Session Subject'
        verbose_name_plural = 'Session Subjects'
    
    #fill session subject activity with test data
    def fillWithTestData(self):
        logger = logging.getLogger(__name__)         

        sada_set = self.Session_day_subject_actvities.order_by('session_day__period_number')
        
        d_today = todaysDate()

        previous_i = None
        for i in sada_set:
            if i.session_day.date == d_today.date():
                break
            
            i.heart_activity_minutes = random.randint(0,30)
            i.immune_activity_minutes = random.randint(240,500)
            i.check_in_today = True

            i.save()
        
        self.reCalcAllActvity()

    def reCalcAllActvity(self):
        logger = logging.getLogger(__name__)    

        d_today = todaysDate()

        sada_set = self.Session_day_subject_actvities.filter(session_day__date__lt=d_today.date()).order_by('session_day__period_number')
        
        logger.info(f"reCalcAllActvity date {d_today.date()}")

        previous_i = None
        for i in sada_set:
           
            if i.session_day.period_number == 1:
                i.heart_activity = self.session.parameterset.heart_activity_inital
                i.immune_activity = self.session.parameterset.immune_activity_inital
            else:
                logger.info(f"previous: {previous_i} current {i}")
                i.saveHeartActivity(previous_i.heart_activity_minutes,previous_i.heart_activity)
                i.saveImmuneActivity(previous_i.immune_activity_minutes,previous_i.immune_activity)

            i.save()

            previous_i = i

    #look back to check for missed days checked in
    def fitBitCatchUp(self):
        logger = logging.getLogger(__name__)
        logger.info(f"fitBitCatchUp name {self.name} session {self.session.id}")

        d_today = todaysDate()

        sa_list  = self.Session_day_subject_actvities.all().filter(check_in_today = False,session_day__date__lt = d_today.date())

        logger.info(f'fitBitCatchUp date {d_today.date()} subject activities {sa_list}')

        #pull in actvity dor days not checked in
        for s in sa_list:
            #if s.session_day.date < d_today.date():

            s.check_in_today=True
            s.save()

            logger.info(f'fitBitCatchUp {s.id}')

            previous_sa = s.getPreviousActivityDay()

            if previous_sa:
                v = previous_sa.pullFitbitActvities()                  
        
        #recalc activtivity scores
        if sa_list:
            self.reCalcAllActvity()

    #return total sleep from date specified
    def getFibitImmuneMinutes(self,search_date):
        logger = logging.getLogger(__name__)
        logger.info("getFibitImmuneMinutes")
        logger.info(search_date)

        p = Parameters.objects.first()

        try:
            r = self.getFitbitSleep(search_date)

            v = 0

            if p.trackerDataOnly:
                for s in r['sleep']:
                    if s['type']=='stages':
                        v+=s['minutesAsleep']

            else:
                v = r['summary']['totalMinutesAsleep']

            logger.info(v)
            return v
        except Exception  as e: 
            logger.info(e)
            return -1
    
    #return total sleep from date specified
    def getFibitHeartMinutes(self,search_date):
        logger = logging.getLogger(__name__)
        logger.info("getFibitHeartMinutes")
        logger.info(search_date)

        p = Parameters.objects.first()

        try:
            r = self.getFitbitActivies(search_date)
            v =  0

            keyStr = ""
            
            if p.trackerDataOnly:
                keyStr = "activities-tracker-minutesVeryActive"
            else:
                keyStr = "activities-minutesVeryActive"

            for a in r[keyStr]:
                logger.info(a)
                v += int(a['value'])


            logger.info(f'getFibitHeartMinutes minutes {v}')
            return v
        except Exception  as e: 
            logger.info(e)
            return -1
        
    #get fitbit sleep object
    def getFitbitSleep(self,sleep_date):
        logger = logging.getLogger(__name__)
        logger.info("Fitbit sleep")
        logger.info(sleep_date) 

        temp_s = sleep_date.strftime("%Y-%m-%d")
        #temp_s = "today"
        #temp_s="2020-10-22"

        fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1.2/user/-/sleep/date/{temp_s}.json')

        return fitbit_response
    
    #get fitbit sleep object
    def getFitbitActivies(self,activity_date):
        logger = logging.getLogger(__name__)
        logger.info("Fitbit activity")
        logger.info(activity_date) 

        p = Parameters.objects.first()

        temp_s = activity_date.strftime("%Y-%m-%d")
        #temp_s = "today"
        #temp_s="2020-10-22"

        if p.trackerDataOnly:
            fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1/user/-/activities/tracker/minutesVeryActive/date/{temp_s}/1d.json')
        else:
            fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1/user/-/activities/minutesVeryActive/date/{temp_s}/1d/15min.json')

        return fitbit_response

    #calc subject's activity today  
    def calcTodaysActivity(self,current_period):
        logger = logging.getLogger(__name__) 
        
        #get session day
        session_day = main.models.Session_day.objects.filter(session = self.session,period_number = current_period)

        if session_day:
            session_day=session_day.first()
        else:
            logger.info("calcTodaysActivity session day not found: period"+ str(current_period) +  " session " + self.session.id)
            return False

        #check period is not 1
        if current_period==1:
            logger.info("calcTodaysActivity current period is 1: period "+ str(current_period) +  " session " + self.session.id)
            return False

        #get yesterday's activity          
        sada_yesterday = self.Session_day_subject_actvities.filter(session_day__period_number = current_period-1)

        if sada_yesterday:
            sada_yesterday=sada_yesterday.first()
        else:
            logger.info("calcTodaysActivity could not find yesterday's activity: period "+ str(current_period) +  " session " + self.session.id)
            return False

        #calc today's activity
        sada_today = self.Session_day_subject_actvities.filter(session_day__period_number = current_period)

        if sada_today:
            sada_today=sada_today.first()
            sada_today.saveHeartActivity(sada_yesterday.heart_activity_minutes,sada_yesterday.heart_activity)
            sada_today.saveImmuneActivity(sada_yesterday.immune_activity_minutes,sada_yesterday.immune_activity)

            sada_today.save()
        else:
            logger.info("calcTodaysActivity could not find today's activity: period "+ str(current_period) +  " session " + self.session.id)
            return False

        return True

    #return true if subject has completed the experiment
    def sessionComplete(self):
        if self.session.complete():
            return True
        
        sa=self.Session_day_subject_actvities.filter(session_day__date = self.session.end_date).first()

        if not sa:
            return False

        if sa.paypal_today:
            return True
        else:
            return False

    #return json object of class
    def json(self,get_fitbit_status):
        p = Parameters.objects.first()

        #link to setup fitbit
        tempURL = p.siteURL+"fitBit/"
        tempURL = tempURL.replace(":","%3A")
        tempURL = tempURL.replace("/","%2F")

        tempClientID = settings.FITBIT_CLIENT_ID
        tempState = str(self.id) + ";" + str(self.session.id)
        fitBit_Link = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={tempClientID}&redirect_uri={tempURL}&scope=activity%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&expires_in=604800&prompt=login%20consent&state={tempState}"

        #test if fitbit is already connected
        fitBit_Attached = False
        if get_fitbit_status and self.fitBitAccessToken != "":
            fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1.2/user/-/body/log/weight/date/today.json')
            
            if 'weight' in fitbit_response:
                fitBit_Attached = True

                tz = pytz.timezone(p.experimentTimeZone)
                d = datetime.now(tz)

                #fitbit_response_sleep = self.getFitbitSleep(d)

        return{
            "id":self.id,
            "name":self.name,
            "contact_email":self.contact_email,
            "student_id":self.student_id,
            "gmail_address":self.gmail_address,
            "gmail_password":self.gmail_password,
            "login_url": p.siteURL +'subjectHome/' + str(self.login_key),
            "fitBit_Link" : fitBit_Link,
            "fitBit_Attached" : fitBit_Attached,
            "get_fitbit_status" : get_fitbit_status,
            "consent_required": self.consent_required,
            "questionnaire1_required":self.questionnaire1_required,
            "questionnaire2_required":self.questionnaire2_required,
        }
    
    #take fitbit api url and return response
    def getFitbitInfo(self,url):
        logger = logging.getLogger(__name__)        

        r = self.getFitbitInfo2(url)

        #try to reauthorize
        if 'success' in r:        
            headers = {'Authorization': 'Basic ' + str(settings.FITBIT_AUTHORIZATION) ,
                       'Content-Type' : 'application/x-www-form-urlencoded'}
            
            data = {'grant_type' : 'refresh_token',
                    'refresh_token' : self.fitBitRefreshToken}    
            
            r = requests.post('https://api.fitbit.com/oauth2/token', headers=headers,data=data).json()

            if 'access_token' in r:
                self.fitBitAccessToken = r['access_token']
                self.fitBitRefreshToken = r['refresh_token']
                self.fitBitUserId = r['user_id']

                self.save()

                logger.info("Fitbit refresh: User" + str(self.id))
                logger.info(r)
            else:
                logger.info("Fitbit refresh failed:")
                logger.info(r) 

            r = self.getFitbitInfo2(url)
        
        return r

    def getFitbitInfo2(self,url):
        logger = logging.getLogger(__name__)     

        headers = {'Authorization': 'Bearer ' + self.fitBitAccessToken,
                   'Accept-Language' :	'en_US'}    

        r = requests.get(url, headers=headers).json()

        logger.info("Fitbit request:" + url)
        logger.info(r)

        return r