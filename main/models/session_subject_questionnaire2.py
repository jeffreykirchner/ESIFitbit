from django.db import models
import logging
import traceback
from django.contrib.auth.models import User

from main.models import Session_subject
from main.globals.likertScales import Likert_importance,Likert_satisfaction,Likert_variation,Likert_variation2

#gloabal parameters for site
class Session_subject_questionnaire2(models.Model):

    session_subject = models.ForeignKey(Session_subject,on_delete=models.CASCADE,related_name="Session_subject_questionnaire2")

    sleep_changed = models.BooleanField(default=False,verbose_name="Sleep Changed")
    sleep_changed_explaination = models.CharField(max_length = 10000, default = '',verbose_name = 'Sleep Changed Explanation')
    
    exercise_changed = models.BooleanField(default=False,verbose_name="Exercise Changed")
    exercise_changed_explaination = models.CharField(max_length = 10000, default = '',verbose_name = 'Exercise Changed Explanation')

    health_concern = models.BooleanField(default=False,verbose_name="Health Concern")
    health_concern_explaination = models.CharField(max_length = 10000, default = '',verbose_name = 'Health Concern Explanation')

    def __str__(self):
        return "Post Questionnaire"

    class Meta:
        verbose_name = 'Post Questionnaire'
        verbose_name_plural = 'Post Questionnaires'
    
    def json(self):
        return{
           
        }