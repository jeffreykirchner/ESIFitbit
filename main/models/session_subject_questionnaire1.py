from django.db import models
import logging
import traceback
from django.contrib.auth.models import User

from main.models import Session_subject
from main.globals.likertScales import Likert_importance,Likert_satisfaction,Likert_variation,Likert_variation2

#gloabal parameters for site
class Session_subject_questionnaire1(models.Model):

    session_subject = models.ForeignKey(Session_subject,on_delete=models.CASCADE,related_name="Session_subject_questionnaire1")

    #Sleep activity
    sleep_hours = models.DecimalField(decimal_places=1, default=0, max_digits=4,verbose_name = 'Sleep Hours')
    sleep_importance = models.CharField(max_length=100, choices=Likert_importance.choices,verbose_name = 'Sleep Likert') 
    sleep_explanation = models.CharField(max_length = 10000, default = '',verbose_name = 'Sleep Explanation')

    #exercise actvity
    exercise_minutes = models.IntegerField(default=0,verbose_name = 'Exercise Minutes')
    exercise_importance  = models.CharField(max_length=100, choices=Likert_importance.choices,verbose_name = 'Exercise Likert') 
    exercise_explanation  = models.CharField(max_length = 10000, default = '',verbose_name = 'Exercise Explanation') 

    #exercise actvity
    health_importance  = models.CharField(max_length=100, choices=Likert_importance.choices,verbose_name = 'Health Importance Likert') 
    health_importance_explanation  = models.CharField(max_length = 10000, default = '',verbose_name = 'Health Importance Explanation') 
    health_importance_actions  = models.CharField(max_length = 10000, default = '',verbose_name = 'Health Importance Actions')

    health_satisfaction  = models.CharField(max_length=100, choices=Likert_satisfaction.choices,verbose_name = 'Health Satisfaction Likert') 

    sleep_variation  = models.CharField(max_length=100, choices=Likert_variation.choices,verbose_name = 'Sleep Variation Likert') 
    sleep_variation_explanation =  models.CharField(max_length = 10000, default = '',verbose_name = 'Sleep Variation Explanation')

    exercise_variation  = models.CharField(max_length=100, choices=Likert_variation2.choices,verbose_name = 'Exercise Variation Likert') 
    exercise_variation_explanation =  models.CharField(max_length = 10000, default = '',verbose_name = 'Exercise Variation Explanation')


    def __str__(self):
        return "Pre Questionnaire"

    class Meta:
        verbose_name = 'Pre Questionnaire'
        verbose_name_plural = 'Pre Questionnaires'
    
    def json(self):
        return{
           
        }