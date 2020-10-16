from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session_day,Session_subject
import uuid

from enum import Enum

#one day from session
class Session_day_user_actvity(models.Model):
    session_day = models.ForeignKey(Session_day,on_delete=models.CASCADE)
    session_subject = models.ForeignKey(Session_subject,on_delete=models.CASCADE)

    heart_activity_minutes = models.DecimalField(decimal_places=10, default=0, max_digits=20)       #todays heart activity minutes
    immune_activity_minutes = models.DecimalField(decimal_places=10, default=0, max_digits=20)      #todays immune activity minutes

    heart_activity = models.DecimalField(decimal_places=10, default=0, max_digits=20)               #todays heart activity calculation
    immune_activity = models.DecimalField(decimal_places=10, default=0, max_digits=20)              #todays immune activity calculation
    
    check_in_today = models.BooleanField(default=False)                                             #true if the user checked in today

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Dat'

    #return json object of class
    def json(self):
        return{
            "id":self.id,
            "treatment":self.treatment,           
        }