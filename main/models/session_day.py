from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session
import uuid

import main
from enum import Enum

#subject in session
class Session_day(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_days")
    
    period_number = models.IntegerField()
    date = models.DateField(default=now)                            #date and time of session day

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id) + " " + str(self.date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'period_number'], name='unique_SD')
        ]
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Days'
    
    #add session day user actvities for testing
    def addSessionDayUserActivites(self):
        logger = logging.getLogger(__name__)

        # session_subjects = self.session.session_subjects

        for s in self.session.session_subjects.filter(soft_delete=False):
            if not main.models.Session_day_subject_actvity.objects.filter(session_day=self,session_subject=s):
                sdsa = main.models.Session_day_subject_actvity()
                sdsa.session_day=self
                sdsa.session_subject=s
                sdsa.heart_activity_minutes=-1
                sdsa.immune_activity_minutes=-1
                sdsa.save()
            

    #return json object of class
    def json(self):
        return{
            "id":self.id          
        }