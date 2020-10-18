from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session
import uuid

from enum import Enum

class Treatment(Enum):
    one = "Individual"                                   
    two = "Individual with chat" 
    three = "Individual with chat and bonus" 

#subject in session
class Session_day(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_days")
    
    period_number = models.IntegerField()
    date = models.DateField(default=now)                            #date and time of session day

    treatment = models.CharField(
        max_length=100,
        choices = [(tag.name, tag.value) for tag in Treatment],
        default=Treatment.one
    )    

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
            "id":self.id,
            "treatment":self.treatment,           
        }