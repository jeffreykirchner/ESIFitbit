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
import math
from main.globals import todaysDate

#subject in session
class Session_subject(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_subjects")

    id_number = models.IntegerField(null=True,verbose_name = 'ID Number in Session')                   #local id number in session

    login_key = models.UUIDField(default=uuid.uuid4, editable=False,verbose_name = 'Login Key')                         #log in key used to ID subject for URL login
    name = models.CharField(max_length = 300,default = 'Subject Name', verbose_name = 'Subject Name')                   #subject name 
    contact_email = models.CharField(max_length = 300,default = 'Subject Email',verbose_name = 'Subject Email')         #contact email address
    student_id = models.CharField(max_length = 300,default = 'Student ID Number',verbose_name = 'Student ID Number')    #student ID number
    gmail_address = models.CharField(max_length = 300,default = 'Gmail Address',verbose_name = 'Gmail Address')         #gmail address asigned to subject for experiment 
    gmail_password = models.CharField(max_length = 300,default = 'Gmail Password',verbose_name = 'Gmail Password')      #password for above 
    
    consent_required = models.BooleanField(default=True,verbose_name = 'Consent Form Signed')          #true if subject has done consent form  
    consent_signature = models.CharField(max_length = 300,default = '',verbose_name = 'Consent Form Signature')

    questionnaire1_required = models.BooleanField(default=True,verbose_name = 'Pre-questionnaire Complete')   #pre experiment questionnaire
    questionnaire2_required = models.BooleanField(default=True,verbose_name = 'Post-questionnaire Complete')   #post experiment questionnaire          

    display_color = models.CharField(max_length = 300,default = '#000000',verbose_name = 'Graph Color')                                       

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
        constraints = [
            models.UniqueConstraint(fields=['id_number', 'session'], name='Session_subject')
        ]
        verbose_name = 'Session Subject'
        verbose_name_plural = 'Session Subjects'
    
    #fill session subject activity with test data
    def fillWithTestData(self):
        logger = logging.getLogger(__name__)         

        sada_set = self.Session_day_subject_actvities.order_by('session_day__period_number')
        
        d_today = todaysDate()

        heart_activity_minutes = random.randint(0,90)
        immune_activity_minutes = random.randint(240,600)

        previous_i = None
        for i in sada_set:
            if i.session_day.date == d_today.date():
                break
            
            if random.randrange(1,100) == 1:
                i.heart_activity_minutes = 0
                i.immune_activity_minutes = 0
            else:
                i.heart_activity_minutes = heart_activity_minutes
                i.immune_activity_minutes = immune_activity_minutes

            heart_activity_minutes += random.randrange(-5,5)
            immune_activity_minutes += random.randrange(-10,10)  

            if heart_activity_minutes < 0:
                heart_activity_minutes = 0

            if immune_activity_minutes < 0:
                immune_activity_minutes =0
                  
            i.check_in_today = True

            if random.randrange(1,50) == 1:
                i.paypal_today=False
            else:
                i.paypal_today=True

            i.save()
        
        self.reCalcAllActvity()

        #save earnings
        sada_set = self.Session_day_subject_actvities.order_by('session_day__period_number')

        for i in sada_set:
            if i.session_day.date == d_today.date():
                break
            
            i.paypal_today = True
            i.storeTodaysTotalEarnings()
            i.save()

        #consent form
        self.consent_required=False
        self.consent_signature=self.name
        self.save()

        #questionnaires
        #logger.info(f"fillWithTestData {self.Session_subject_questionnaire1}")
        if not self.Session_subject_questionnaire1.all():
            q1 = main.models.Session_subject_questionnaire1()
            q1.session_subject=self
            q1.save()
           
        self.Session_subject_questionnaire1.first().fillWithTestData()

        if todaysDate().date()>self.session.end_date:
            if not self.Session_subject_questionnaire2.all():
                q2 = main.models.Session_subject_questionnaire2()
                q2.session_subject=self
                q2.save()
           
            self.Session_subject_questionnaire2.first().fillWithTestData()

    #re calculate all activity scores from period 1
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

    #get questionnaire 1 required status
    def getQuestionnaire1Required(self):
        p = Parameters.objects.first()

        if not p.questionnaire1Required:
            return False
        
        return self.questionnaire1_required
    
    #get questionnaire 2 required status
    def getQuestionnaire2Required(self):
        p = Parameters.objects.first()

        #check that questionnaire 2 is enabled
        if not p.questionnaire2Required:
            return False

        #check that today is the last day of sessoin
        if todaysDate().date() != self.session.end_date:
            return False
        
        return self.questionnaire2_required

    #get the fitbit html connection link
    def getFitBitLink(self,request_type):
        p = Parameters.objects.first()

        #link to setup fitbit
        tempURL = p.siteURL+"fitBit/"
        tempURL = tempURL.replace(":","%3A")
        tempURL = tempURL.replace("/","%2F")

        tempClientID = settings.FITBIT_CLIENT_ID
        tempState = str(self.id) + ";" + str(self.session.id) + ";" + request_type
        fitBit_Link = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={tempClientID}&redirect_uri={tempURL}&scope=activity%20heartrate%20sleep&expires_in=604800&prompt=login%20consent&state={tempState}"

        return fitBit_Link

    #test if a fitbit connection is working for this subject
    def getFitBitAttached(self):
       
        if self.fitBitAccessToken != "":
            fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1.2/user/-/sleep/date/today.json')
            
            if 'sleep' in fitbit_response:
                return True
            else:
                return False

    #return json object of class
    def json(self,get_fitbit_status,request_type):

        p = Parameters.objects.first()

        fitBit_Attached = False
        if get_fitbit_status:
            fitBit_Attached = self.getFitBitAttached()
              
        return{
            "id":self.id,
            "name":self.name,
            "contact_email":self.contact_email,
            "student_id":self.student_id,
            "gmail_address":self.gmail_address,
            "gmail_password":self.gmail_password,
            "login_url": p.siteURL +'subjectHome/' + str(self.login_key),
            "fitBit_Link" : self.getFitBitLink(request_type),
            "fitBit_Attached" : fitBit_Attached,
            "get_fitbit_status" : get_fitbit_status,
            "consent_required": self.consent_required,
            "questionnaire1_required":self.questionnaire1_required,
            "questionnaire2_required":self.questionnaire2_required,
            "todays_stats":self.jsonTodayServerStats(),
            "heart_minutes":self.jsonHeartMinutesList(),
            "immune_minutes":self.jsonImmuneMinutesList(),
            "display_color":self.display_color,

        }
    
    #get json object of current stats to show on server
    def jsonTodayServerStats(self):

        sada = self.Session_day_subject_actvities.filter(session_day__date = todaysDate().date()).first()

        check_in = False
        pay_pal = False
        earnings = "---"
        heart_score = "---"
        heart_time = "---"
        immune_score = "---"
        immune_time = "---"

        if sada:
            sada_yesterday = self.Session_day_subject_actvities.filter(session_day__period_number = sada.session_day.period_number - 1).first()

            check_in = sada.check_in_today
            pay_pal = sada.paypal_today
            earnings = f'${sada.getTodaysTotalEarnings():0.2f}'
            heart_score = f'{sada.heart_activity:0.2f}'
            immune_score = f'{sada.immune_activity:0.2f}'
        else:
            sada_yesterday = None

        if sada_yesterday:
            if sada_yesterday.heart_activity_minutes >= 0:
                heart_time =  f'{int(sada_yesterday.heart_activity_minutes)}mins'
            if sada_yesterday.immune_activity_minutes >= 0:
                immune_time =  f'{math.floor(sada_yesterday.immune_activity_minutes/60)}hrs {sada_yesterday.immune_activity_minutes%60}mins'

        return{
            "check_in":check_in,
            "pay_pal":pay_pal,
            "earnings":earnings,
            "heart_score":heart_score,
            "heart_time":heart_time,
            "immune_score":immune_score,
            "immune_time":immune_time,
        }

    #get json object of daily minutes exercising
    def jsonHeartMinutesList(self):
        sdsa_list = self.Session_day_subject_actvities.all().order_by('session_day__period_number')

        return [sdsa.heart_activity_minutes for sdsa in sdsa_list]
    
    #get json object of daily hours exercising
    def jsonImmuneMinutesList(self):
        sdsa_list = self.Session_day_subject_actvities.all().order_by('session_day__period_number')

        return [sdsa.immune_activity_minutes/60 for sdsa in sdsa_list]
    
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