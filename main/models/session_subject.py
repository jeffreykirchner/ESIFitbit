from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session,Parameters
import uuid
from django.conf import settings
import requests

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
    fitBitAccessToken = models.CharField(max_length=200, default="",verbose_name = 'FitBit Access Token')
    fitBitRefreshToken = models.CharField(max_length=200, default="",verbose_name = 'FitBit Refresh Token')
    fitBitUserId = models.CharField(max_length=200, default="",verbose_name = 'FitBit User ID')  

    soft_delete =  models.BooleanField(default=False)                                                 #hide subject if true

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Session Subject'
        verbose_name_plural = 'Session Subjects'

    #return json object of class
    def json(self):
        p = Parameters.objects.first()

        tempURL = p.siteURL+"fitBit/"
        tempURL = tempURL.replace(":","%3A")
        tempURL = tempURL.replace("/","%2F")

        tempClientID = settings.FITBIT_CLIENT_ID

        tempState = str(self.id) + ";" + str(self.session.id)
        fitBitLink = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={tempClientID}&redirect_uri={tempURL}&scope=activity%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&expires_in=604800&prompt=login%20consent&state={tempState}"

        return{
            "id":self.id,
            "name":self.name,
            "contact_email":self.contact_email,
            "student_id":self.student_id,
            "gmail_address":self.gmail_address,
            "gmail_password":self.gmail_password,
            "login_url": p.siteURL +'subjectHome/' + str(self.login_key),
            "fitBitLink" : fitBitLink,
        }

    def getFitbitInfo(self,url,u):
        logger = logging.getLogger(__name__)         

        r = self.getFitbitInfo2(url,u)

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

            r = self.getFitbitInfo2(url,u)
        
        return r

    def getFitbitInfo2(self,url,u):
        logger = logging.getLogger(__name__)     

        headers = {'Authorization': 'Bearer ' + u.profile.fitBitAccessToken,
                   'Accept-Language' :	'en_US'}    

        r = requests.get(url, headers=headers).json()

        logger.info("Fitbit request:" + url)
        logger.info(r)

        return r