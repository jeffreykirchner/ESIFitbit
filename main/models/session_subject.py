from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session,Parameters
import uuid
from django.conf import settings

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

        return{
            "id":self.id,
            "name":self.name,
            "contact_email":self.contact_email,
            "student_id":self.student_id,
            "gmail_address":self.gmail_address,
            "gmail_password":self.gmail_password,
            "login_url": p.siteURL +'subjectHome/' + str(self.login_key)
        }