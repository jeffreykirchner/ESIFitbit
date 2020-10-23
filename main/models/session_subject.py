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

#subject in session
class Session_subject(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_subjects")

    login_key = models.UUIDField(default=uuid.uuid4, editable=False,verbose_name = 'Login Key')                         #log in key used to ID subject for URL login
    name = models.CharField(max_length = 300,default = 'Subject Name', verbose_name = 'Subject Name')                   #subject name 
    contact_email = models.CharField(max_length = 300,default = 'Subject Email',verbose_name = 'Subject Email')         #contact email address
    student_id = models.CharField(max_length = 300,default = 'Student ID Number',verbose_name = 'Student ID Number')    #student ID number
    gmail_address = models.CharField(max_length = 300,default = 'Gmail Address',verbose_name = 'Gmail Address')         #gmail address asigned to subject for experiment 
    gmail_password = models.CharField(max_length = 300,default = 'Gmail Password',verbose_name = 'Gmail Password')      #password for above 
 
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
        }
    
    def getFitbitSleep(self,sleep_date):
        logger = logging.getLogger(__name__)
        logger.info("Fitbit sleep")
        logger.info(sleep_date) 

        temp_s = sleep_date.strftime("%Y-%m-%d")
        temp_s = "today"

        fitbit_response = self.getFitbitInfo('https://api.fitbit.com/1.2/user/-/sleep/date/' + temp_s + '.json')

        return fitbit_response
    
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