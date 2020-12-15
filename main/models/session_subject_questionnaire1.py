from django.db import models
import logging
import traceback
from django.contrib.auth.models import User

import random
from django.utils.crypto import get_random_string

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

    #address
    address_full_name = models.CharField(max_length = 1000, default = '',verbose_name = 'Full Name Address') 
    address_line_1 = models.CharField(max_length = 1000, default = '',verbose_name = 'Address Line 1')
    address_line_2 = models.CharField(max_length = 1000, default = '',verbose_name = 'Address Line 2') 
    address_city = models.CharField(max_length = 1000, default = '',verbose_name = 'Address City')
    address_state = models.CharField(max_length = 1000, default = '',verbose_name = 'Address State')
    address_zip_code = models.CharField(max_length = 1000, default = '',verbose_name = 'Address Zip Code')


    def __str__(self):
        return "Pre Questionnaire"

    class Meta:
        verbose_name = 'Pre Questionnaire'
        verbose_name_plural = 'Pre Questionnaires'
    
    #fill questionnaire with test data
    def fillWithTestData(self):
        self.sleep_hours = random.randrange(4, 10)
        self.sleep_importance = random.randrange(0, 7)
        self.sleep_explanation = get_random_string(length=100)

        self.exercise_minutes = random.randrange(0, 90)
        self.exercise_importance = random.randrange(0, 7)
        self.exercise_explanation = get_random_string(length=100)

        self.health_importance = random.randrange(0, 7)
        self.health_importance_explanation = get_random_string(length=100)
        self.health_importance_actions = get_random_string(length=100)

        self.health_satisfaction = random.randrange(0, 7)

        self.sleep_variation = random.randrange(0, 7)
        self.sleep_variation_explanation = get_random_string(length=100)

        self.exercise_variation = random.randrange(0, 7)
        self.exercise_variation_explanation = get_random_string(length=100)

        self.save()

    #write to data file
    def getCSVResponse(self,writer):

        # 'Session','Subject ID','Subject Code','Sleep Hours','Sleep Likert','Sleep Explanation','Exercise Minutes',
        #                  'Exercise Likert','Exercise Explanation','Health Importance Likert',
        #                  'Health Importance Explanation','Health Importance Actions','Health Satisfaction Likert',
        #                  'Sleep Variation Likert','Sleep Variation Explanation',
        #                  'Exercise Variation Likert','Exercise Variation Explanation'

        writer.writerow([self.session_subject.session.title,self.session_subject.id_number,self.session_subject.login_key,
                         self.sleep_hours,self.sleep_importance,self.sleep_explanation,
                         self.exercise_minutes,self.exercise_importance,self.exercise_explanation,
                         self.health_importance,self.health_importance_explanation,self.health_importance_actions,
                         self.health_importance_actions,self.sleep_variation,self.sleep_variation_explanation,
                         self.exercise_variation,self.exercise_variation_explanation,self.address_full_name,
                         self.address_line_1,self.address_line_2,self.address_city,self.address_state,self.address_zip_code])

    def json(self):
        return{
           
        }