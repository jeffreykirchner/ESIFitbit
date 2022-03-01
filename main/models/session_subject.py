'''
session subject model
'''
import logging
import traceback
import requests
import uuid
import pytz
import random
import main
import math

from . import Session, Parameters

from datetime import datetime, timedelta, timezone, date

from django.db.models import Avg
from django.conf import settings
from django.utils.timezone import now
from django.db import models

from main.globals import todaysDate, round_half_away_from_zero

#subject in session
class Session_subject(models.Model):
    '''
    session subject model
    '''
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_subjects")

    id_number = models.IntegerField(null=True,verbose_name = 'ID Number in Session')                   #local id number in session

    login_key = models.UUIDField(default=uuid.uuid4, verbose_name='Login Key',unique=True)                              #log in key used to ID subject for URL login
    name = models.CharField(max_length = 300,default = 'Subject Name', verbose_name='Subject Name')                     #subject name 
    contact_email = models.CharField(max_length = 300,default = 'abc@123.edu',verbose_name = 'Subject Email')         #contact email address
    student_id = models.CharField(max_length = 300,default = 'Student ID Number',verbose_name = 'Student ID Number')    #student ID number
    
    consent_required = models.BooleanField(default=True,verbose_name = 'Consent Form Signed')          #true if subject has done consent form  
    consent_signature = models.CharField(max_length = 300,default = '',verbose_name = 'Consent Form Signature')

    questionnaire1_required = models.BooleanField(default=True,verbose_name = 'Pre-questionnaire Complete')   #pre experiment questionnaire
    questionnaire2_required = models.BooleanField(default=True,verbose_name = 'Post-questionnaire Complete')   #post experiment questionnaire          

    display_color = models.CharField(max_length = 300, default = '#000000', verbose_name = 'Graph Color')                                       
    group_number = models.IntegerField(default = 1, verbose_name="Group Number")

    #fitbit    
    fitBitAccessToken = models.CharField(max_length=1000, default="",verbose_name = 'FitBit Access Token')
    fitBitRefreshToken = models.CharField(max_length=1000, default="",verbose_name = 'FitBit Refresh Token')
    fitBitUserId = models.CharField(max_length=100, default="",verbose_name = 'FitBit User ID')  
    fitBitLastSynced =  models.DateTimeField(default=None,null=True,verbose_name = 'FitBit Last Synced')
    fitBitTimeZone = models.CharField(max_length=1000, default="",verbose_name = 'FitBit Time Zone')

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

        #save earnings if treatment I or B
        if self.session.treatment == "I" or self.session.treatment == "Base":
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

        if not self.getFitBitAttached():
            logger.warning(f'fitBitCatchUp error not attached {d_today.date()} subject activities {sa_list}')
            return

        #pull in actvity for days not checked in
        for s in sa_list:
            #if s.session_day.date < d_today.date():

            logger.info(f'fitBitCatchUp {s.id}')

            previous_sa = s.getPreviousActivityDay()

            if previous_sa:
                fitbiterror = previous_sa.pullFitbitActvities()

                if not fitbiterror:
                    previous_sa.pullFibitBitHeartRate(True)

                    s.check_in_today=True
                    s.save()        
                else:
                    logger.warning(f'fitBitCatchUp error date {d_today.date()} subject activities {sa_list}')
                    break
        
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

            # if p.trackerDataOnly:
            #     for s in r['sleep']:
            #         if s['type']=='stages':
            #             v+=s['minutesAsleep']

            # else:
            v = r['summary']['totalMinutesAsleep']

            logger.info(v)
            return v
        except Exception  as e: 
            logger.info(e)
            return -1
    
    #return total sleep from date specified
    def getFibitActivityMinutes(self,search_date,search_parameter):
        logger = logging.getLogger(__name__)
        logger.info(f"getFibitActivityMinutes ID {self.id} Name {self.name} date {search_date} parameter {search_parameter}")
        
        p = Parameters.objects.first()

        try:
            keyStr = ""
            v = 0
            response_key=""

            #very active minutes
            if p.trackerDataOnly:
                response_key = f"activities-tracker-{search_parameter}"
            else:
                response_key = f"activities-{search_parameter}"
        
            r = self.getFitbitActivies(search_date,search_parameter)
            v =  0

            for a in r[response_key]:
                logger.info(a)
                v += int(a['value'])
           
            # v += self.getFibitHeartMinutes2(search_date,response_key,search_parameter)

            # #fairly active minutes
            # if p.trackerDataOnly:
            #     response_key = "activities-tracker-minutesFairlyActive"
            # else:
            #     response_key = "activities-minutesFairlyActive"
           
            # v += self.getFibitHeartMinutes2(search_date,response_key,"minutesFairlyActive")

            logger.info(f'getFibitActivityMinutes minutes {v}')
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
        #temp_s="2021-1-25"

        fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1.2/user/-/sleep/date/{temp_s}.json')

        return fitbit_response

    #get fitbit activity object
    def getFitbitActivies(self,activity_date,activity_key):
        logger = logging.getLogger(__name__)
        logger.info("Fitbit activity")
        logger.info(activity_date) 

        p = Parameters.objects.first()

        temp_s = activity_date.strftime("%Y-%m-%d")
        #temp_s = "today"
        #temp_s="2020-11-20"

        if p.trackerDataOnly:
            fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1/user/-/activities/tracker/{activity_key}/date/{temp_s}/1d.json')
        else:
            fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1/user/-/activities/{activity_key}/date/{temp_s}/1d/15min.json')

        return fitbit_response

    def getFibitProfile(self):
        '''
        pull profile info from fitbit
        '''

        # /1/user/[user-id]/profile.json
        fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1/user/-/profile.json')

        return fitbit_response

    #get fitbit heart rate object
    def getFitbitHeartRate(self,heart_date):
        logger = logging.getLogger(__name__)
        logger.info("Fitbit heart rate")
        logger.info(heart_date) 

        temp_s = heart_date.strftime("%Y-%m-%d")
        #temp_s = "today"
        #temp_s="2020-11-20"

        fitbit_response = self.getFitbitInfo(f'https://api.fitbit.com/1/user/-/activities/heart/date/{temp_s}/1d.json')

        return fitbit_response

    #calc subject's activity today  
    def calcTodaysActivity(self, current_period):
        logger = logging.getLogger(__name__) 
        
        #get session day
        session_day = main.models.Session_day.objects.filter(session = self.session, period_number = current_period)

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
            sada_today.saveHeartActivity(sada_yesterday.heart_activity_minutes, sada_yesterday.heart_activity)
            sada_today.saveImmuneActivity(sada_yesterday.immune_activity_minutes, sada_yesterday.immune_activity)

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
    # def getQuestionnaire1Required(self):
    #     p = Parameters.objects.first()

    #     if not p.questionnaire1Required:
    #         return False
        
    #     return self.questionnaire1_required
    
    #get questionnaire 2 required status
    def getQuestionnaire2Required(self):
        #p = Parameters.objects.first()

        #check that questionnaire 2 is enabled
        # if not p.questionnaire2Required:
        #     return False

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
        fitBit_Link = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={tempClientID}&redirect_uri={tempURL}&scope=activity%20heartrate%20sleep%20settings%20profile%20weight&expires_in=604800&prompt=login%20consent&state={tempState}"

        return fitBit_Link

    #test if a fitbit connection is working for this subject
    def getFitBitAttached(self):
        logger = logging.getLogger(__name__) 

        if self.fitBitAccessToken != "":
            #fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1.2/user/-/sleep/date/today.json')
            fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1/user/-/devices.json')
            
            logger.info(f'getFitBitAttached {fitbit_response} {self.id}')

            v = -1
            
            try:
                v = fitbit_response[0].get("lastSyncTime",-1)                
            except Exception  as e: 
                logger.info(e)
                return False

            if v == -1:                   
                return False
            else:
                a=[]
                
                for i in fitbit_response:

                    v = datetime.strptime(i.get("lastSyncTime"),'%Y-%m-%dT%H:%M:%S.%f')

                    #test synced today
                    #v = v-timedelta(days=1)

                    logger.info(f'getFitBitAttached sync time {v}')

                    d = datetime.now(pytz.UTC)
                    d = d.replace(hour=v.hour,minute=v.minute, second=v.second,microsecond=v.microsecond,
                               year=v.year,month=v.month,day=v.day)

                    logger.info(f'getFitBitAttached sync time {d}')

                    a.append(d)
                
                a.sort(reverse=True)

                self.fitBitLastSynced = a[0] #datetime.strptime(v,'%Y-%m-%dT%H:%M:%S.%f')
                self.save()

                return True
        else:
            return False

    #true if the subject has synced their fitbit today
    def fitbitSyncedToday(self):
        logger = logging.getLogger(__name__) 
        d_today = todaysDate().date()

        if not self.fitBitLastSynced:
            return False

        d_fitbit=self.fitBitLastSynced.date()

        logger.info(f'fitbitSyncedToday {self} Today:{d_today} Last Synced:{d_fitbit}')

        if d_fitbit>=d_today:
            return True
        else:
            return False

    #get subject's local timzone
    def getFitbitTimeZone(self):
        logger = logging.getLogger(__name__) 

        if self.fitBitAccessToken != "":
            #fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1.2/user/-/sleep/date/today.json')
            fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1/user/-/profile.json')
            
            u = fitbit_response.get("user",-1)

            if u != -1:
                v = u.get("timezone",-1)

                logger.info(f'getFitTimeZone {v} {self.id}')

                if v == -1:                   
                    return False
                else:
                    self.fitBitTimeZone = v
                    self.save()
                    return True
            else:
                return False

    #get the formatted date string
    def getFitbitLastSyncStr (self,show_tz):

        if not self.fitBitLastSynced:
            return "---"

        if show_tz and self.fitBitTimeZone == "":
            return "---"

        t = self.fitBitLastSynced.strftime("%#m/%#d/%Y %#I:%M %p")

        if show_tz:
            p = Parameters.objects.first()
            tz = pytz.timezone(self.fitBitTimeZone)

            tz = tz.localize(datetime.now(), is_dst=None)

            v = t + " " + tz.tzname()
        else:
            v = t

        return  v

    def get_average_heart_score(self, period_number):
        '''
        return the current average heart score of eligable days
        '''
        logger = logging.getLogger(__name__)

        #period_number = self.session.getCurrentSessionDay().period_number

        start_period_number = self.session.parameterset.get_block_first_period(period_number)

        if not start_period_number:
            return -1

        heart_activity_average = self.Session_day_subject_actvities.filter(paypal_today = True) \
                                                                   .filter(session_day__period_number__gte = start_period_number) \
                                                                   .filter(session_day__period_number__lte = period_number) \
                                                                   .aggregate(Avg('heart_activity'))

        logger.info(f'get_average_heart_score {heart_activity_average}, start period {start_period_number}, end period {period_number}')

        if not heart_activity_average["heart_activity__avg"]:
            return -1

        return round_half_away_from_zero(heart_activity_average["heart_activity__avg"], 2)
    
    def get_average_sleep_score(self, period_number):
        '''
        return the current average sleep score of eligable days
        '''
        logger = logging.getLogger(__name__)

        #period_number = self.session.getCurrentSessionDay().period_number
        start_period_number = self.session.parameterset.get_block_first_period(period_number)

        sleep_activity_average = self.Session_day_subject_actvities.filter(paypal_today = True) \
                                                                   .filter(session_day__period_number__gte = start_period_number) \
                                                                   .filter(session_day__period_number__lte = period_number) \
                                                                   .aggregate(Avg('immune_activity'))

        logger.info(f'get_average_sleep_score {sleep_activity_average}, start period {start_period_number}, end period {period_number}')

        if not sleep_activity_average["immune_activity__avg"]:
            return -1

        return round_half_away_from_zero(sleep_activity_average["immune_activity__avg"], 2)

    def get_missed_checkins(self, period_number):
        logger = logging.getLogger(__name__)

        #period_number = self.session.getCurrentSessionDay().period_number
        
        start_period_number = self.session.parameterset.get_block_first_period(period_number)

        if not start_period_number:
            return 0

        missed_count = self.Session_day_subject_actvities.filter(paypal_today = False) \
                                                         .filter(session_day__period_number__gte = start_period_number) \
                                                         .filter(session_day__period_number__lte = period_number) \
                                                         .count()

        return missed_count
    
    def get_daily_payment_A_B_C(self, period_number):
        '''
        return what the current payment is for treatments A, B and C
        '''
        logger = logging.getLogger(__name__)
        
        #period_number = self.session_day.period_number

        payment = 0
        parameterset = self.session.parameterset

        if self.session.treatment=="A":
            payment = float(parameterset.get_fixed_pay(period_number))

            if parameterset.getHeartPay(period_number) > 0:
                heart_score = self.get_average_heart_score(period_number)
                sleep_score = self.get_average_sleep_score(period_number)

                if heart_score < 0.0 :
                    heart_score = 0.0
                
                if sleep_score < 0.0 :
                    sleep_score = 0.0

                payment = payment + heart_score * float(parameterset.getHeartPay(period_number)) + \
                                    sleep_score * float(parameterset.getImmunePay(period_number))

                logger.info(f'get_daily_payment_A heart score {heart_score}, sleep score {sleep_score}')

        elif self.session.treatment=="B" or self.session.treatment=="C":
            payment = float(parameterset.get_fixed_pay(period_number))

            if parameterset.getHeartPay(period_number) > 0:
                heart_score = self.get_average_heart_score(period_number)
                sleep_score = self.get_average_sleep_score(period_number)

                if heart_score < 0.0 :
                    heart_score = 0.0
                
                if sleep_score < 0.0 or not parameterset.sleep_tracking:
                    sleep_score = 0.0

                payment = payment + heart_score * float(parameterset.get_treatment_b_c_paylevel(heart_score)) + \
                                    sleep_score * float(parameterset.get_treatment_b_c_paylevel(sleep_score))

                logger.info(f'get_daily_payment_B_C heart score {heart_score}, sleep score {sleep_score}')

        return round_half_away_from_zero(payment, 2)

    def get_earnings_in_block_so_far(self, period_number):
        '''
        return the earnings a subject has made up to this point
        '''

        missed_checkins = self.get_missed_checkins(period_number)
        total_days = self.session.parameterset.get_block_day_count(period_number)

        if not total_days:
            return 0

        return round_half_away_from_zero((total_days - missed_checkins) * self.get_daily_payment_A_B_C(period_number), 2)

    #get list of group members in json
    def get_group_list_json(self):
        if not self.session.parameterset.show_group:
            return []

        session_subjects_group=[]

        session_subjects_group.append(self.jsonGroup())

        for i in self.session.session_subjects.filter(group_number=self.group_number).exclude(id=self.id).order_by('id_number'):
             session_subjects_group.append(i.jsonGroup())

        return session_subjects_group

    #return json object of class
    def json(self,get_fitbit_status,request_type):

        p = Parameters.objects.first()

        fitBit_Attached = False
        if get_fitbit_status:
            fitBit_Attached = self.getFitBitAttached()

        q1 = self.Session_subject_questionnaire1.first()
              
        return{
            "id":self.id,
            "name":self.name,
            "contact_email":self.contact_email,
            "student_id":self.student_id,
            "login_url": p.siteURL +'subjectHome/' + str(self.login_key),
            "fitBit_Link" : self.getFitBitLink(request_type),
            "fitBit_Attached" : fitBit_Attached,
            "fitBit_last_synced":self.getFitbitLastSyncStr(False),
            "get_fitbit_status" : get_fitbit_status,
            "consent_required": self.consent_required,
            "questionnaire1_required":self.questionnaire1_required,
            "questionnaire2_required":self.questionnaire2_required,
            "todays_stats":self.jsonTodayServerStats(),
            "heart_minutes":self.jsonHeartMinutesList(),
            "immune_minutes":self.jsonImmuneMinutesList(),
            "display_color":self.display_color,
            "address_full_name":q1.address_full_name if q1 else "---",
            "address_line_1":q1.address_line_1 if q1 else "---",
            "address_line_2":q1.address_line_2 if q1 else "---",
            "address_city":q1.address_city if q1 else "---",
            "address_state":q1.address_state if q1 else "---",
            "address_zip_code":q1.address_zip_code if q1 else "---",
            "birthdate" : q1.birthdate.strftime("%#m/%#d/%Y") if q1 and q1.birthdate else "---",
            "group_number" : self.group_number,
        }
    
    #get json object of current stats to show on server
    def jsonTodayServerStats(self):

        sada = self.Session_day_subject_actvities.filter(session_day__date = todaysDate().date()).first()

        check_in = False
        pay_pal = False
        earnings = "---"
        heart_score = "---"
        heart_time = "---"
        heart_bpm = "---"
        immune_score = "---"
        immune_time = "---"
        wrist_time = "---|---"
        missed_days = "---"

        if sada:
            #sada_yesterday = self.Session_day_subject_actvities.filter(session_day__period_number = sada.session_day.period_number - 1).first()
            sada_yesterday = sada.getPreviousActivityDay()

            check_in = sada.check_in_today
            pay_pal = sada.paypal_today

            if self.session.treatment == "I" or self.session.treatment == "Base":
                earnings = f'${sada.getTodaysTotalEarnings():0.2f}'
            else:
                earnings = f'${self.get_earnings_in_block_so_far(sada.session_day.period_number):0.2f}'

            missed_days = self.get_missed_checkins(sada.session_day.period_number)

            if check_in:
                heart_score = f'{sada.heart_activity:0.2f}'
                heart_bpm = f'{sada.fitbit_min_heart_rate_zone_bpm}bpm'       
                immune_score = f'{sada.immune_activity:0.2f}' 
        else:
            sada_yesterday = None

        if sada_yesterday:
            wrist_time = f'{sada_yesterday.getFormatedWristMinutes()} | {sada.getFormatedWristMinutes()}'

            if sada_yesterday.heart_activity_minutes >= 0:
                heart_time =  f'{int(sada_yesterday.heart_activity_minutes)}mins'
                
            if sada_yesterday.immune_activity_minutes >= 0:
                immune_time =  f'{math.floor(sada_yesterday.immune_activity_minutes/60)}hrs {sada_yesterday.immune_activity_minutes%60}mins'
                
        elif sada:
            wrist_time = f'---| {sada.getFormatedWristMinutes()}'

        return{
            "check_in" : check_in,
            "pay_pal" : pay_pal,
            "earnings" : earnings,
            "heart_score" : heart_score,
            "heart_time" : heart_time,
            "heart_bpm" : heart_bpm,
            "immune_score" : immune_score,
            "immune_time" : immune_time,
            "wrist_time" : wrist_time, 
            "missed_days" : missed_days,          
        }

    #get json object of daily minutes exercising
    def jsonHeartMinutesList(self):
        sdsa_list = self.Session_day_subject_actvities.all().order_by('session_day__period_number')

        return [sdsa.heart_activity_minutes for sdsa in sdsa_list]
    
    #get json object of daily hours exercising
    def jsonImmuneMinutesList(self):
        sdsa_list = self.Session_day_subject_actvities.all().order_by('session_day__period_number')

        return [sdsa.immune_activity_minutes/60 for sdsa in sdsa_list]

    #return json for group info
    def jsonGroup(self):

        sada = self.Session_day_subject_actvities.filter(session_day__date = todaysDate().date()).first()
        sada_yesterday = sada.getPreviousActivityDay()

        if sada_yesterday:

            immune_activity_minutes=int(sada_yesterday.immune_activity_minutes)
            immune_activity_hours = f'{math.floor(immune_activity_minutes/60)}hrs {immune_activity_minutes%60}mins'

            return {"heart_score":sada_yesterday.heart_activity_formatted(),
                    "heart_min":f'{int(sada_yesterday.heart_activity_minutes)}mins',
                    "id":sada_yesterday.id,
                    "sleep_score":sada_yesterday.immune_activity_formatted(),
                    "sleep_hours":immune_activity_hours,
                    }
        else:
             return {"heart_score":"---",
                     "heart_min":"---",
                     "id":sada.id,
                     "sleep_score":"---",
                     "sleep_hours":"---",
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
                logger.warning("Fitbit refresh failed:")
                logger.warning(r) 

            r = self.getFitbitInfo2(url)
        
        return r

    def getFitbitInfo2(self,url):
        logger = logging.getLogger(__name__)     

        headers = {'Authorization': 'Bearer ' + self.fitBitAccessToken,
                   'Accept-Language' :	'en_US'}    

        try:            
            r = requests.get(url, headers=headers)

            r = r.json()

            logger.info(f"Fitbit request: {url} ")
            logger.info(f"Fitbit request:{r}")

            return r
        except Exception  as e: 
            logger.warning(f"getFitbitInfo2 error: {e} , response: {r}")
            return  "fail"