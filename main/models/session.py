from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Parameterset

from django.dispatch import receiver
from django.db.models.signals import post_delete

from enum import Enum

class Treatment(Enum):
    one = "Individual"                                   
    two = "Individual with chat" 
    three = "Individual with chat and bonus" 

#experiment sessoin
class Session(models.Model):
    parameterset = models.ForeignKey(Parameterset,on_delete=models.CASCADE)

    title = models.CharField(max_length = 300,default="*** New Session ***")    #title of session
    start_date = models.DateField(default=now)                                  #date of session

    treatment = models.CharField(
        max_length=100,
        choices = [(tag.name, tag.value) for tag in Treatment],
        default=Treatment.one
    )    

    soft_delete =  models.BooleanField(default=False)                            #hide session if true

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Experiment Session'
        verbose_name_plural = 'Experiment Sessions'

    #get the current period number
    def getCurrentPeriod(self):
        return 1

    #get the current treatment for this sesssion
    def getCurrentTreatment(self):
        return 1
    
    #get user readable string of start session date
    def getDateString(self):
        return  self.start_date.strftime("%#m/%#d/%Y")

    #return json object of class
    def json(self):
        return{
            "id":self.id,
            "title":self.title,
            "start_date":self.getDateString(),
            "current_period":self.getCurrentPeriod(),
            "currentTreatment":self.getCurrentTreatment(),
            "parameterset":self.parameterset.json(),
        }

#delete associated user model when profile is deleted
@receiver(post_delete, sender=Session)
def post_delete_parameterset(sender, instance, *args, **kwargs):
    if instance.parameterset: 
        instance.parameterset.delete()