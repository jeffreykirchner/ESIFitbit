from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Session_day,Session_subject
import uuid
import main

from enum import Enum

#one day from session 
class Session_day_subject_actvity(models.Model):
    session_day = models.ForeignKey(Session_day,on_delete=models.CASCADE)
    session_subject = models.ForeignKey(Session_subject,on_delete=models.CASCADE,related_name="Session_day_subject_actvities")

    heart_activity_minutes = models.DecimalField(decimal_places=10, default=0, max_digits=20)       #todays heart activity minutes
    immune_activity_minutes = models.DecimalField(decimal_places=10, default=0, max_digits=20)      #todays immune activity minutes

    heart_activity = models.DecimalField(decimal_places=10, default=0, max_digits=20)               #todays heart activity calculation
    immune_activity = models.DecimalField(decimal_places=10, default=0, max_digits=20)              #todays immune activity calculation
    
    check_in_today = models.BooleanField(default=False)                                             #true if the user checked in today
    paypal_today = models.BooleanField(default=False)                                               #true if the user collected their payment today

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return "Period " + str(self.session_day.period_number) + " Subject " + self.session_subject.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session_day', 'session_subject'], name='unique_SDSA')
        ]
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Days'

    #calc heart activity
    def calcHeartActivity(self,heart_time,heartActivityMinus1):
        logger = logging.getLogger(__name__)

        p_set = self.session_day.session.parameterset

        return self.calcActivity(heart_time,
                                p_set.heart_parameter_1,
                                p_set.heart_parameter_2,
                                p_set.heart_parameter_3,
                                heartActivityMinus1)

    #save heart activity    
    def saveHeartActivity(self,heart_time,heartActivityMinus1):
        self.heart_activity = self.calcHeartActivity(heart_time,heartActivityMinus1)
        self.save()

    #calc immune activity
    def calcImmuneActivity(self,immune_time,immuneActivityMinus1):
        p_set = self.session_day.session.parameterset

        return self.calcActivity(immune_time,
                                p_set.immune_parameter_1,
                                p_set.immune_parameter_2,
                                p_set.immune_parameter_3,
                                immuneActivityMinus1)

    #save immune activity    
    def saveImmuneActivity(self,immune_time,immuneActivityMinus1):
        self.immune_activity = self.calcImmuneActivity(immune_time,immuneActivityMinus1)
        self.save()

    #calc activity
    def calcActivity(self,active_time,p1,p2,p3,activityMinus1): 
        #immuneActivityTodayT-1 * (1 - (1 - immuneActivityTodayT-1) * (immune_parameter_1 / immune_parameter_2  - immuneTimeT-1 / (immuneTimeT-1 + immune_parameter_3))

        v = float(activityMinus1) * (1 - (1 - float(activityMinus1)) * (float(p1) / float(p2)  - float(active_time) / (float(active_time) + float(p3))))

        return min(1,v)     

    #heart activity / 100
    def heart_activity_formatted(self):
        v = round(self.heart_activity * 100,2)
        return f'{v}/100'

    #immune activity /100
    def immune_activity_formatted(self):
        v = round(self.immune_activity * 100,2)
        return f'{v}/100'

    #return the activity day before this one
    def getPreviousActivityDay(self):
        logger = logging.getLogger(__name__)

        if self.session_day.period_number ==1:
            return None
        
        try:
            return main.models.Session_day_subject_actvity.objects.get(session_subject = self.session_subject,
                                                                       session_day__period_number = self.session_day.period_number-1)
        except Exception  as e: 
            logger.info(e)
            return None
    
    #get range of possible heart activities for tomorrow
    def getHeartActivityFutureRange(self):

        v = []

        ps = self.session_day.session.parameterset

        value_step = (ps.x_max_heart-ps.x_min_heart) / 100
        current_value = ps.x_min_heart

        for i in range(99):
            v.append({"x":current_value, "y": self.calcHeartActivity(current_value,self.heart_activity)})
            current_value += value_step

        return v

    #return json object of class
    def json(self):
        return{
            "id":self.id,             
            "heart_activity":self.heart_activity_formatted(),     
            "immune_activity":self.immune_activity_formatted(),
            "heart_activity_minutes":self.heart_activity_minutes,     
            "immune_activity_minutes":self.immune_activity_minutes,
            "check_in_today":self.check_in_today,     
            "paypal_today":self.paypal_today,
            "heart_activity_future":self.getHeartActivityFutureRange(),
        }