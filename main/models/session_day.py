from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session
import uuid

from enum import Enum

#subject in session
class Session_day(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_days")
    
    period_number = models.IntegerField()
    date = models.DateField(default=now)                            #date and time of session day

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'period_number'], name='unique_SD')
        ]
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Dat'

    #return json object of class
    def json(self):
        return{
            "id":self.id          
        }