'''
session day model
'''

import logging

from django.db import models
from django.utils.timezone import now

import main

from . import Session



#subject in session
class Session_day(models.Model):
    '''
    session day model
    '''
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="session_days")
    
    period_number = models.IntegerField()
    date = models.DateField(default=now)                            #date and time of session day

    payments_sent = models.BooleanField(default=False)                                #true once paypal payments are sent
    payments_result_message = models.CharField(max_length=200, default="No Payment")  #display message about payment status

    survey_required = models.BooleanField(default=False, verbose_name="Survey Complete")
    survey_link = models.CharField(max_length = 1000, default = '', verbose_name = 'Survey Link')  

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return (f'{self.session.title} : date + {self.date} id {self.id}')
    
    def __title__(self):
        return str(self.session.title)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'period_number'], name='unique_SD_period_number'),
            #models.UniqueConstraint(fields=['session', 'date'], name='unique_SD_date')
        ]
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Days'
        ordering = ['period_number']
        
    
    #add session day user actvities for testing
    def addSessionDayUserActivites(self):
        logger = logging.getLogger(__name__)

        # session_subjects = self.session.session_subjects

        for s in self.session.session_subjects.filter(soft_delete=False):
            self.addNewSessionDayUserActivity(s)
                
    #add new session day user activity for a session_subject        
    def addNewSessionDayUserActivity(self, session_subject):
        logger = logging.getLogger(__name__)

        if not main.models.Session_day_subject_actvity.objects.filter(session_day=self,session_subject=session_subject):
            sdsa = main.models.Session_day_subject_actvity()
            sdsa.session_day=self
            sdsa.session_subject=session_subject
            sdsa.heart_activity_minutes=-1
            sdsa.immune_activity_minutes=-1
            sdsa.survey_complete = False if self.survey_required else True
            sdsa.save()

            return sdsa
        else:
            return None
    
    #return the session day before this one
    def getPreviousSessionDay(self):
        logger = logging.getLogger(__name__)

        if self.period_number ==1:
            return None
        
        try:
            return main.models.Session_day.objects.get(period_number=self.period_number-1,session=self.session)
        except Exception  as e: 
            logger.info(e)
            return None
    
    #return the current maximum payment for heart activty
    def getCurrentHeartPay(self):
        return self.session.getHeartPay(self.period_number)

    def get_current_heart_pay_display(self):
        '''
        return the heart pay as it should be displayed to subjects
        '''
        if self.session.treatment=="I":
            return self.getCurrentHeartPay()/100
        else:
            return self.getCurrentHeartPay()

    #return the current maximum payment for heart activty
    def getCurrentImmunePay(self):
        return self.session.getImmunePay(self.period_number)

    def get_current_immune_pay_display(self):
        '''
        return the sleep pay as it should be displayed to subjects
        '''
        if self.session.treatment=="I":
            return self.getCurrentImmunePay()/100
        else:
            return self.getCurrentImmunePay()

    #get the formatted date string
    def getDateStr(self):
        return self.date.strftime("%m/%d/%Y")

    #true if this session day is the last day in a session
    def lastDay(self):
        if self.date==self.session.end_date:
            return True
        else:
            return False

    #return CSV response for data download
    def getCSVResponse(self,writer):
        sdsa_list = self.Session_day_subject_actvities_SD.filter(session_subject__soft_delete=False).order_by('session_subject__id_number')
        
        if self.session.treatment == "I" or self.session.treatment == "Base":
            for sdsa in sdsa_list:
                sdsa.getCSVResponse(writer)
        else:
            for sdsa in sdsa_list:
                sdsa.getCSVResponseABC(writer)

    def calc_a_b_c_block_payments(self):
        '''
        if today is payday, calc payments
        '''

        last_period = self.session.parameterset.get_block_last_period(self.period_number)

        #check if this period is last period in block
        if self.period_number != last_period:
            return {"session day": str(self), "payments": []}
        
        result = []

        for session_a in self.Session_day_subject_actvities_SD.all():
            result.append({"subject": str(session_a.session_subject),
                           "payment": session_a.calc_a_b_c_block_payments()})

        return {"session day": str(self), "payments": result}

    #return json object of class
    def json(self):
        return{
            "id":self.id,
            "period_number" : self.period_number,
            "date" : self.date,
            "payments_sent" : self.payments_sent,
            "payments_result_message" : self.payments_result_message,
            "survey_required" : 1 if self.survey_required else 0,
            "survey_link" : self.survey_link,
        }