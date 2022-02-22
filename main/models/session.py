'''
session model
'''

from datetime import datetime, timedelta

import logging
import csv
import json

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.timezone import now
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder

import main

from main.models import Parameterset
from main.models import InstructionSet
from main.models import Parameters
from main.globals import todaysDate, TimeBlock, NoticeType
class Session(models.Model):
    '''
    session model
    '''

    class Treatment(models.TextChoices):
        '''
        treatment types for session
        '''
        BASE = 'Base', _('Baseline')
        ONE = 'I', _('Individual')
        A = 'A', _('Treatment A')
        B = 'B', _('Treatment B')
        C = 'C', _('Treatment C')       

    parameterset = models.ForeignKey(Parameterset, on_delete=models.CASCADE)
    instruction_set = models.ForeignKey(InstructionSet, null=True, blank=True, on_delete=models.CASCADE)

    title = models.CharField(max_length = 300,default="*** New Session ***")    #title of session
    start_date = models.DateField(default=now)                                  #date of session start
    end_date = models.DateField(default=now)                                    #date of session end

    started =  models.BooleanField(default=False)                               #starts session and filll in session
    allow_delete =  models.BooleanField(default=True)                           #if true allow the session to be deleted

    canceled = models.BooleanField(default=False)                               #true if session needs to be canceled
    cancelation_text =  models.CharField(max_length=10000, default="")          #text sent to subjects if experiment is canceled
    cancelation_text_subject = models.CharField(max_length=1000, default="")    #email subject text for experiment cancelation

    invitations_sent = models.BooleanField(default=False)                        #true once invititations have been sent to subjects
    invitation_text =  models.CharField(max_length=10000, default="")            #text sent to subjects in experiment invititation
    invitation_text_subject = models.CharField(max_length=1000, default="")      #email subject text for experiment invititation

    treatment = models.CharField( max_length=100, choices=Treatment.choices,default=Treatment.ONE)    #payment system used

    auto_pay = models.BooleanField(default=False)                                 #if true automaically send payments to subject via paypal

    consent_required = models.BooleanField(default=True, verbose_name='Consent Form Signed')                 #true if subject has done consent form  
    questionnaire1_required = models.BooleanField(default=True, verbose_name='Pre-questionnaire Complete')   #pre experiment questionnaire
    questionnaire2_required = models.BooleanField(default=True, verbose_name='Post-questionnaire Complete')  #post experiment questionnaire

    soft_delete =  models.BooleanField(default=False)                            #hide session if true

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Experiment Session'
        verbose_name_plural = 'Experiment Sessions'
        ordering = ['-start_date', 'title']

    #get the current session day
    def getCurrentSessionDay(self):
        #logger = logging.getLogger(__name__)

        d_today = todaysDate().date()

        #logger.info(f"getCurrentSessionDay {d_today}")

        return self.session_days.filter(date = d_today).first()
    
    def getYesterdaysSessionDay(self):
        #logger = logging.getLogger(__name__)

        d_yesterday = todaysDate() - timedelta(days=1)

        #logger.info(f"getCurrentSessionDay {d_today}")

        try:
            return self.session_days.get(date = d_yesterday.date())
        except ObjectDoesNotExist:
            return None
        
        return None
    
    #return true if today is before the start date
    def isBeforeStartDate(self):
        logger = logging.getLogger(__name__)

        if todaysDate().date() < self.start_date:
            return True
        else:
            return False

    #assign local id numbers to subjects
    def assignSubjectIdNumbers(self):
        logger = logging.getLogger(__name__)

        c = 1

        ss_list = self.session_subjects.all().order_by('id')

        for ss in ss_list:
            ss.id_number = c
            ss.save()
            
            c+=1       

    #add new sessions days when experiment is started
    def addNewSessionDays(self):
        logger = logging.getLogger(__name__)
        logger.info("Add new sessions: " + str(self.title))

        #get today's date
        d_start = todaysDate()
        d_start = d_start.replace(day=self.start_date.day,month=self.start_date.month, year=self.start_date.year)

        d_start += timedelta(days=1)
        tempPeriod = 2

        logger.info(d_start)
        #logger.info(d_end)     

        #add days for block 1
        for i in range(self.parameterset.block_1_day_count):   
            self.addSessionDay(d_start.date(),tempPeriod)
            d_start += timedelta(days=1)
            tempPeriod+=1

        #add days for block 2
        for i in range(self.parameterset.block_2_day_count):   
            self.addSessionDay(d_start.date(),tempPeriod)
            d_start += timedelta(days=1)
            tempPeriod+=1 
        
        #add days for block 3
        for i in range(self.parameterset.block_3_day_count):   
            self.addSessionDay(d_start.date(),tempPeriod)
            d_start += timedelta(days=1)
            tempPeriod+=1 


        # while d_start <= d_end:
        #     #logger.info("Newest session day: " + str(sd))
        #     self.addSessionDay(d_start.date(),tempPeriod)
        #     d_start += timedelta(days=1)
        #     tempPeriod+=1     

    #add new session day to this session
    def addSessionDay(self,new_day,new_period):
        logger = logging.getLogger(__name__)
        logger.info(f"addSessionDay date {new_day} period number {new_period}")

        #check that this session day does not already exist

        # check_sd = main.models.Session_day.objects.filter(session=self,period_number=new_period,date = new_day)
        # new_sd = None
        
        # if check_sd:
        #     new_sd = check_sd.first()
        #     logger.info(f"Created session day already exists: date {new_day} period {new_period} ")
        # else: 
        new_sd = main.models.Session_day()

        new_sd.date = new_day
        new_sd.session=self
        new_sd.period_number=new_period
        new_sd.save()        

        new_sd.addSessionDayUserActivites()

        logger.info("Created session day: " + str(new_sd))

    #fill subjects with test data    
    def fillWithTestData(self):
        logger = logging.getLogger(__name__) 
        logger.info("fillWithTestData")

        for s in self.session_subjects.all():
            s.fillWithTestData()

    #get user readable string of start session date
    def getDateString(self):
        return  self.start_date.strftime("%#m/%#d/%Y")
    
    #get user readable string of end session date
    def getEndDateString(self):
        return  self.end_date.strftime("%#m/%#d/%Y")
    
    #return true if session parameters can still be edited
    def editable(self):

        if self.started:
            return False
        else:
            return True
        
    #return the current maximum payment for heart activty
    def getHeartPay(self,period):
        return self.parameterset.getHeartPay(period)

    #return the current maximum payment for heart activty
    def getImmunePay(self,period):
        return self.parameterset.getImmunePay(period)

    #return total number of days of session
    def numberOfDays(self):
        return self.parameterset.block_1_day_count+self.parameterset.block_2_day_count+self.parameterset.block_3_day_count+1
    
    #calc and store end date
    def calcEndDate(self):

        d_end = todaysDate()
        d_end = d_end.replace(day=self.start_date.day,month=self.start_date.month, year=self.start_date.year)

        d_end += timedelta(days=self.numberOfDays()-1)

        self.end_date=d_end.date()
        self.save()

    #send email invitations to subject in the session
    def sendInvitations(self):

        p = Parameters.objects.first()
        text = self.invitation_text

        text = text.replace("[start date]", self.getDateString())
        text = text.replace("[number of days]", str(self.numberOfDays()))
        text = text.replace("[end date]", self.getEndDateString())
        text = text.replace("[contact email]", p.contactEmail)

        user_list = []
        for user in self.session_subjects.filter(soft_delete=False):
            user_list.append({"email" : user.contact_email,
                              "variables": [{"name" : "subject name", "text" : user.name},
                                            {"name" : "log in link", "text" : p.siteURL + "subjectHome/" + str(user.login_key)}] })

        memo = f'Session: {self.id}, send invitations'

        return main.globals.send_mass_email_service(user_list, self.invitation_text_subject, text, memo)

    #send email canceling session
    def sendCancelation(self):
        p = Parameters.objects.first()
        text = self.cancelation_text

        text = text.replace("[contact email]", p.contactEmail)

        user_list = []
        for user in self.session_subjects.filter(soft_delete=False):
            user_list.append({"email" : user.contact_email,
                              "variables": [{"name" : "subject name", "text" : user.name},
                                            {"name" : "log in link", "text" : p.siteURL + "subjectHome/" + str(user.login_key)}] })

        memo = f'Session: {self.id}, send cancelations'

        return main.globals.send_mass_email_service(user_list, self.cancelation_text_subject, text, memo)

    #return true if today's date past end date
    def complete(self):
        if todaysDate().date()>self.end_date:
            return True
        else:
            return False

    #return CSV response for data download
    def getCSVResponse(self):
        
        csv_response = HttpResponse(content_type='text/csv')
        csv_response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(csv_response)

        writer.writerow(["Subject Data"])

        if self.treatment == "I" or self.treatment == "Base":

            writer.writerow(["Session","Period","Block","Date","Subject ID", "Email","Heart Activity Minutes",
                            "Immune Activity Minutes","Heart Activity Score","Immune Activity Score",
                            "Fitbit Data Pulled", "Paid Today", "Fixed Payment","Heart Payment","Immune Payment","Total Payment Today",
                            "Minutes Sedentary","Minutes Lightly Active","Minutes Fairly Active","Minutes Very Active","Steps","Calories",
                            "Heart Rate Minutes Out of Range","Heart Rate Minutes Fat Burn","Heart Rate Minutes Cardio",
                            "Heart Rate Minutes Peak","Zone Minutes Minimum BPM","Time On Wrist","First Login Time"])
        else:
             writer.writerow(["Session","Period","Block","Date","Subject ID", "Email","Heart Activity Minutes",
                            "Immune Activity Minutes","Heart Activity Score","Immune Activity Score",
                            "Fitbit Data Pulled", "Paid Today", "Missed Days", "Fixed Payment", "Average Heart Score","Heart Pay Level", "Average Immune Score", "Immune Pay Level", "Total Payment Today",
                            "Minutes Sedentary","Minutes Lightly Active","Minutes Fairly Active","Minutes Very Active","Steps","Calories",
                            "Heart Rate Minutes Out of Range","Heart Rate Minutes Fat Burn","Heart Rate Minutes Cardio",
                            "Heart Rate Minutes Peak","Zone Minutes Minimum BPM","Time On Wrist","First Login Time"])

        sd_list = self.session_days.all().order_by('period_number')

        for sd in sd_list:
            sd.getCSVResponse(writer)

        if self.questionnaire1_required:
            writer.writerow([])
            writer.writerow(["Pre Questionnaire"])

            writer.writerow(['Session','Subject ID', 'Subject Code', 'Email', 'Consent Signature', 'Sleep Hours', 'Sleep Likert', 'Sleep Explanation','Exercise Minutes',
                            'Exercise Likert', 'Exercise Explanation', 'Health Importance Likert',
                            'Health Importance Explanation', 'Health Importance Actions', 'Health Satisfaction Likert',
                            'Sleep Variation Likert', 'Sleep Variation Explanation',
                            'Exercise Variation Likert', 'Exercise Variation Explanation', 'Full Name', 'Address Line 1', 'Address Line 2',
                            'City', 'State', 'Zip Code', 'Birthdate', 'Attended'])

            ss_list = self.session_subjects.order_by('id_number')
            
            for ss in ss_list:
                if ss.Session_subject_questionnaire1.all():
                    ss.Session_subject_questionnaire1.first().getCSVResponse(writer)

        if self.questionnaire2_required:
            writer.writerow([])
            writer.writerow(["Post Questionnaire"])

            writer.writerow(['Session','Subject ID', 'Subject Code', 'Email', 
                            'Sleep Change Post', 'Sleep Change Post Explanation',
                            'Exercise Change Post', 'Exercise Changed Post Explanation',
                            'Health Concern Post', 'Health Concern Post Explanation',
                            'Holiday Break Explaination', 'Sex at Birth', 'Gender Identity', 'Gender Identity Self Describe'])

            ss_list = self.session_subjects.filter(soft_delete=False).order_by('id_number')
            
            for ss in ss_list:
                if ss.Session_subject_questionnaire2.all():
                    ss.Session_subject_questionnaire2.first().getCSVResponse(writer)

        #parameters
        writer.writerow([])
        writer.writerow(["Parameters"])
        writer.writerow(['Session','Treatment',
                          'Heart activity inital','Heart parameter 1','Heart parameter 2','Heart parameter 3',
                          'Immune activity inital','Immune parameter 1','Immune parameter 2','Immune parameter 3',
                          'Block 1 heart pay','Block 2 heart pay','Block 3 heart pay', 
                          'Block 1 immune pay','Block 2 immune pay','Block 3 immune pay',
                          'Block 1 day count','Block 2 day count','Block 3 day count', 
                          'Block 1 fixed pay', 'Block 2 fixed pay', 'Block 3 fixed pay', 'Minutes required on wrist',
                          'Y min heart','Y max heart','Y ticks heart','X min heart','X max heart','X ticks heart',  
                          'Y min immune','Y max immune','Y ticks immune','X min immune','X max immune','X ticks immune',
                          'Sleep Tracking', 'Show Groups'])

        self.parameterset.getCSVResponse(writer,self.title,self.Treatment(self.treatment).label)

        #pay levels
        if self.treatment == "B" or self.treatment == "C":
            writer.writerow([])
            writer.writerow(["Parameters Paylevels"])
            writer.writerow(["Score Start", "Score End", "Value"])
            self.parameterset.get_csv_response_pay_level(writer)

        return csv_response

    #get earnings in csv file for specified date
    def getCSVEarnings(self,date):
        logger = logging.getLogger(__name__)

        csv_response = HttpResponse(content_type='text/csv')
        csv_response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(csv_response)

        date = datetime.strptime(date,"%Y-%m-%d").date()

        logger.info(f'getCSVEarnings date {date}')

        sdsa_list = main.models.Session_day_subject_actvity.objects.filter(session_subject__soft_delete=False,
                                                                           session_day__session=self,
                                                                           session_day__date = date)

        logger.info(sdsa_list)

        for sdsa in sdsa_list:
            # if sdsa.paypal_today:
            writer.writerow([sdsa.session_subject.student_id, f'${sdsa.payment_today:0.2f}'])
            # else:
            #     writer.writerow([sdsa.session_subject.student_id,'$0.00'])

        return csv_response

    def get_current_block(self):
        '''
        get the current time block
        '''

        logger = logging.getLogger(__name__)

        session_day = self.getCurrentSessionDay()
        current_block = 1

        if session_day:
            current_block = self.parameterset.getBlock(session_day.period_number)
        
        if current_block == 1:
            return TimeBlock.ONE
        
        if current_block == 2:
            return TimeBlock.TWO
        
        return TimeBlock.THREE
    
    def get_next_block(self, p_number):
        '''
        get the next time block
        '''

        current_block = self.parameterset.getBlock(p_number)
        
        if current_block == 1:
            return TimeBlock.ONE
        
        if current_block == 2:
            return TimeBlock.TWO
        
        return TimeBlock.THREE
        
    def get_instruction_text(self, page_type):
        '''
        get the page_type of instruction given the current period
        '''

        #no instruction set attached
        if not self.instruction_set:
            return ""

        return self.instruction_set.get_page_text(self.get_current_block(), page_type)

    def get_notice_text(self, p_number):
        '''
        get current notice text
        '''

        if not self.instruction_set:
            return ""        

        p_number_used = p_number

        if self.parameterset.getBlockChangeToday(p_number):
            notice_type = NoticeType.START
            time_block = self.get_current_block()
        elif self.parameterset.getBlockChangeInTwoDays(p_number):
            p_number_used = p_number + 2
            notice_type = NoticeType.ADVANCE
            time_block = self.get_next_block(p_number_used)
        else:
            return ""

        notice_text = self.instruction_set.get_notice_text(time_block, notice_type)

        if self.treatment == "I" or self.treatment == "Base":
            notice_text = notice_text.replace("[heart pay]", f'{self.parameterset.getHeartPay(p_number_used)/100:0.2f}')
            notice_text = notice_text.replace("[immune pay]", f'{self.parameterset.getImmunePay(p_number_used)/100:0.2f}')            
        else:
            notice_text = notice_text.replace("[heart pay]", f'{self.parameterset.getHeartPay(p_number_used):0.2f}')
            notice_text = notice_text.replace("[immune pay]", f'{self.parameterset.getImmunePay(p_number_used):0.2f}')

        notice_text = notice_text.replace("[fixed pay]", f'{self.parameterset.get_fixed_pay(p_number_used):0.2f}')
        notice_text = notice_text.replace("[fixed pay - 1]", f'{self.parameterset.get_fixed_pay(min(p_number_used - 1,1)):0.2f}')

        return notice_text
    
    def get_notice_title(self, p_number):
        '''
        get current notice title
        '''

        if not self.instruction_set:
            return ""

        if self.parameterset.getBlockChangeToday(p_number):
            notice_type = NoticeType.START
            time_block = self.get_current_block()
        elif self.parameterset.getBlockChangeInTwoDays(p_number):
            notice_type = NoticeType.ADVANCE
            time_block = self.get_next_block(p_number + 2)
        else:
            return ""

        return self.instruction_set.get_notice_title(time_block, notice_type)
    
    def get_block_pay_date(self, period_number):
        '''
        return the pay date given the specified period
        '''
        last_period = self.parameterset.get_block_last_period(period_number)

        last_period_date = self.session_days.get(period_number = last_period).date

        return last_period_date + timedelta(days=1)
    
    def get_block_pay_date_formatted(self, period_number):
        '''
        return the pay date given the specified period formatted
        '''

        return self.get_block_pay_date(period_number).strftime("%#m/%#d/%Y")

    #return json object of class
    def json(self):
        '''
        return json object of model
        '''
        email_list=""
        for s in self.session_subjects.filter(soft_delete=False):
            if email_list != "":
                email_list +=", "

            email_list += s.contact_email

        current_session_day = self.getCurrentSessionDay()
        yesterday_session_day = self.getYesterdaysSessionDay()

        return{
            "id" : self.id,
            "title" : self.title,
            "start_date" : self.getDateString(),
            "end_date" : self.getEndDateString(),
            "treatment" : self.treatment,
            "instruction_set" : self.instruction_set.json() if self.instruction_set else {},
            "treatment_label" : self.Treatment(self.treatment).label,
            "parameterset" : self.parameterset.json(),
            "editable" : self.editable(),
            "started" : self.started,
            "canceled" : self.canceled,
            "invitations_sent" : self.invitations_sent,
            "invitation_text" : self.invitation_text,
            "invitation_text_subject" : self.invitation_text_subject,
            "cancelation_text" : self.cancelation_text,
            "cancelation_text_subject":self.cancelation_text_subject,
            "email_list" : email_list,
            "current_period" : current_session_day.period_number if current_session_day else "---",
            "complete": self.complete(),
            "allow_delete" : self.allow_delete,
            "consent_required" : 1 if self.consent_required else 0,
            "questionnaire1_required" : 1 if self.questionnaire1_required else 0,
            "questionnaire2_required" : 1 if self.questionnaire2_required else 0,
            "payments_sent_yestery" : yesterday_session_day.payments_result_message if yesterday_session_day else "---",
            "auto_pay" : 1 if self.auto_pay else 0,
        }

#delete associated user model when profile is deleted
@receiver(post_delete, sender=Session)
def post_delete_parameterset(sender, instance, *args, **kwargs):
    if instance.parameterset: 
        instance.parameterset.delete()