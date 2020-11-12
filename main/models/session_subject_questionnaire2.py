from django.db import models
import logging
import traceback
from django.contrib.auth.models import User

from main.models import Session_subject
from main.globals.likertScales import Likert_change

#gloabal parameters for site
class Session_subject_questionnaire2(models.Model):

    session_subject = models.ForeignKey(Session_subject,on_delete=models.CASCADE,related_name="Session_subject_questionnaire2")

    sleep_changed = models.CharField(max_length=100, choices=Likert_change.choices,verbose_name = 'Sleep Change Post')
    sleep_changed_explaination = models.CharField(max_length = 10000, default = '',verbose_name = 'Sleep Change Post Explanation')
    
    exercise_changed = models.CharField(max_length=100, choices=Likert_change.choices,verbose_name = 'Exercise Change Post')
    exercise_changed_explaination = models.CharField(max_length = 10000, default = '',verbose_name = 'Exercise Changed Post Explanation')

    health_concern = models.CharField(max_length=100, choices=Likert_change.choices,verbose_name = 'Health Concsern Post')
    health_concern_explaination = models.CharField(max_length = 10000, default = '',verbose_name = 'Health Concern Post Explanation')

    def __str__(self):
        return "Post Questionnaire"

    class Meta:
        verbose_name = 'Post Questionnaire'
        verbose_name_plural = 'Post Questionnaires'
    
    def json(self):
        return{
           
        }