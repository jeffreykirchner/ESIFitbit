from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Parameterset

#experiment sessoin
class Session(models.Model):
    parameterset = models.ForeignKey(Parameterset,on_delete=models.CASCADE)

    title = models.CharField(max_length = 300)                                #title of session
    start_date = models.DateTimeField(default=now)                            #date and time of session

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Experiment Session'
        verbose_name_plural = 'Experiment Sessions'

    #return json object of class
    def json(self):
        return{
            "id":self.id,
            "name":self.name,
            "name":self.start_date,
        }