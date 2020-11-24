from django.db import models
import logging
import traceback
from django.utils.timezone import now
from . import Parameterset

from django.dispatch import receiver
from django.db.models.signals import post_delete
import main
import pytz

from main.globals import todaysDate

from main.models import Parameters

from django.http import HttpResponse
import csv

from datetime import datetime,timedelta

from enum import Enum
from django.utils.translation import gettext_lazy as _
   
#experiment sessoin
class Session(models.Model):

    class Treatment(models.TextChoices):
        FOUR = "B", _('Baseline')
        ONE = 'I', _('Individual')
        TWO = "IwC", _('Individual with chat')
        THREE = "IwCpB", _('Individual with chat and bonus')        

    parameterset = models.ForeignKey(Parameterset,on_delete=models.CASCADE)

    title = models.CharField(max_length = 300,default="*** New Session ***")    #title of session
    start_date = models.DateField(default=now)                                  #date of session start
    end_date = models.DateField(default=now)                                    #date of session end

    started =  models.BooleanField(default=False)                               #starts session and filll in session 

    canceled = models.BooleanField(default=False)                               #true if session needs to be canceled
    cancelation_text =  models.CharField(max_length = 10000,default = "")       #text sent to subjects if experiment is canceled
    cancelation_text_subject = models.CharField(max_length = 1000,default = "") #email subject text for experiment cancelation

    invitations_sent = models.BooleanField(default=False)                       #true once invititations have been sent to subjects
    invitation_text =  models.CharField(max_length = 10000,default = "")        #text sent to subjects in experiment invititation
    invitation_text_subject = models.CharField(max_length = 1000,default = "")  #email subject text for experiment invititation

    treatment = models.CharField( max_length=100, choices=Treatment.choices,default=Treatment.ONE)    

    soft_delete =  models.BooleanField(default=False)                            #hide session if true

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Experiment Session'
        verbose_name_plural = 'Experiment Sessions'

    #get the current session day
    def getCurrentSessionDay(self):
        logger = logging.getLogger(__name__)

        d_today = todaysDate()

        #logger.info(f"getCurrentSessionDay {d_today}")

        return self.session_days.filter(date = d_today).first()
    
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
        return self.parameterset.block_1_day_count+self.parameterset.block_2_day_count+self.parameterset.block_3_day_count
    
    #calc and store end date
    def calcEndDate(self):

        d_end = todaysDate()
        d_end = d_end.replace(day=self.start_date.day,month=self.start_date.month, year=self.start_date.year)

        d_end += timedelta(days=self.numberOfDays())

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

        return main.globals.sendMassInvitations(self.session_subjects.all(),self.invitation_text_subject,text)

    #send email canceling session
    def sendCancelation(self):
        p = Parameters.objects.first()
        text = self.cancelation_text

        text = text.replace("[contact email]", p.contactEmail)

        return main.globals.sendMassInvitations(self.session_subjects.all(),self.cancelation_text_subject,text)

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
        writer.writerow(["Session","Period","Block","Date","Subject ID", "Subject Code","Heart Activity Minutes",
                         "Immune Activity Minutes","Heart Activity Score","Immune Activity Score",
                         "Check In Today", "Paid Today","Fixed Payment","Heart Payment","Immune Payment","Total Payment Today"])

        sd_list = self.session_days.all().order_by('period_number')

        for sd in sd_list:
            sd.getCSVResponse(writer)

        writer.writerow([])
        writer.writerow(["Pre Questionnaire"])

        writer.writerow(['Session','Subject ID','Subject Code','Sleep Hours','Sleep Likert','Sleep Explanation','Exercise Minutes',
                         'Exercise Likert','Exercise Explanation','Health Importance Likert',
                         'Health Importance Explanation','Health Importance Actions','Health Satisfaction Likert',
                         'Sleep Variation Likert','Sleep Variation Explanation',
                         'Exercise Variation Likert','Exercise Variation Explanation'])

        ss_list = self.session_subjects.all().order_by('id_number')
        
        for ss in ss_list:
            if ss.Session_subject_questionnaire1.all():
                ss.Session_subject_questionnaire1.first().getCSVResponse(writer)

        writer.writerow([])
        writer.writerow(["Post Questionnaire"])

        writer.writerow(['Session','Subject ID','Subject Code',
                         'Sleep Change Post','Sleep Change Post Explanation',
                         'Exercise Change Post','Exercise Changed Post Explanation',
                         'Health Concern Post','Health Concern Post Explanation'])

        ss_list = self.session_subjects.all().order_by('id_number')
        
        for ss in ss_list:
            if ss.Session_subject_questionnaire2.all():
                ss.Session_subject_questionnaire2.first().getCSVResponse(writer)

        #parameters
        writer.writerow([])
        writer.writerow(["Parameters"])
        writer.writerow(['Session',
                          'Heart activity inital','Heart parameter 1','Heart parameter 2','Heart parameter 3',
                          'Immune activity inital','Immune parameter 1','Immune parameter 2','Immune parameter 3',
                          'Block 1 heart pay','Block 2 heart pay','Block 3 heart pay', 
                          'Block 1 immune pay','Block 2 immune pay','Block 3 immune pay',
                          'Block 1 day count','Block 2 day count','Block 3 day count', 
                          'Fixed pay per day',
                          'Treatment 3 heart bonus','Treatment 3 immune bonus','Treatment 3 bonus target count',  
                          'Y min heart','Y max heart','Y ticks heart','X min heart','X max heart','X ticks heart',  
                          'Y min immune','Y max immune','Y ticks immune','X min immune','X max immune','X ticks immune'])

        self.parameterset.getCSVResponse(writer,self.title)

        return csv_response

    #get earnings in csv file for specified date
    def getCSVEarnings(self,date):
        logger = logging.getLogger(__name__)

        csv_response = HttpResponse(content_type='text/csv')
        csv_response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(csv_response)

        date = datetime.strptime(date,"%Y-%m-%d").date()

        logger.info(f'getCSVEarnings date {date}')

        sdsa_list = main.models.Session_day_subject_actvity.objects.filter(session_day__session=self,session_day__date = date)

        logger.info(sdsa_list)

        for sdsa in sdsa_list:
            if sdsa.paypal_today:
                writer.writerow([sdsa.session_subject.student_id,f'${sdsa.getTodaysTotalEarnings():0.2f}'])
            else:
                writer.writerow([sdsa.session_subject.student_id,'$0.00'])

        return csv_response


    #return json object of class
    def json(self):

        email_list=""
        for s in self.session_subjects.all():
            if email_list != "":
                email_list +=", "

            email_list += s.contact_email

        return{
            "id":self.id,
            "title":self.title,
            "start_date":self.getDateString(),
            "end_date":self.getEndDateString(),
            "treatment":self.treatment,
            "treatment_label":self.Treatment(self.treatment).label,
            "parameterset":self.parameterset.json(),
            "editable":self.editable(),
            "started":self.started,
            "canceled":self.canceled,
            "invitations_sent":self.invitations_sent,
            "invitation_text":self.invitation_text,
            "invitation_text_subject":self.invitation_text_subject,
            "cancelation_text":self.cancelation_text,
            "cancelation_text_subject":self.cancelation_text_subject,
            "email_list":email_list,
        }

#delete associated user model when profile is deleted
@receiver(post_delete, sender=Session)
def post_delete_parameterset(sender, instance, *args, **kwargs):
    if instance.parameterset: 
        instance.parameterset.delete()