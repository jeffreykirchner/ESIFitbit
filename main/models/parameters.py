from django.db import models
import logging
import traceback
from django.contrib.auth.models import User

#gloabal parameters for site
class Parameters(models.Model):
    contactEmail =  models.CharField(max_length = 1000,default = "JohnSmith@abc.edu")      #primary contact for subjects
    experimentTimeZone = models.CharField(max_length = 1000,default = "US/Pacific")        #time zone the experiment is in
    maxDailyEarnings = models.DecimalField(decimal_places=2, max_digits=5,default = 20)   #max money that can be paid to a subject per year  
    siteURL = models.CharField(max_length = 200,default = "https://www.google.com/")       #site URL used for display in emails

    invitationTextSubject = models.CharField(max_length = 1000,default = "")               #email subject text for the single day invitation
    invitationText = models.CharField(max_length = 10000,default = "")                     #email text for the single day invitation
    
    cancelationTextSubject = models.CharField(max_length = 1000,default = "")              #email subject text when an experiment is canceled
    cancelationText = models.CharField(max_length = 10000,default = "")                    #email text when an experiment is canceled

    consentForm = models.CharField(max_length = 50000, default ="")                        #consent for subject must agree to before participation 
    consentFormRequired = models.BooleanField(default=True)                                #true if subject must agree to special consent form before doing experiment

    questionnaire1Required = models.BooleanField(default=True)                             #enable pre experiment questionnaire
    questionnaire2Required = models.BooleanField(default=True)                             #enable post experiment questionnaire

    trackerDataOnly = models.BooleanField(default=True)                                    #only use data collected from fitness tracker

    heartHelpText = models.CharField(max_length = 5000,default = "")                       #heart help text shown to subjects
    immuneHelpText = models.CharField(max_length = 5000,default = "")                      #immune help text shown to subjects
    paymentHelpText = models.CharField(max_length = 5000,default = "")                     #payment help text shown to subjects for none baseline
    paymentHelpTextBaseline = models.CharField(max_length = 5000,default = "")             #payment help text shown to subjects for basline treatments

    manualHelpText = models.CharField(max_length = 5000,default = "")                      # help text shown to staff
    staffHomeHelpText = models.CharField(max_length = 5000,default = "")                   # help text shown to staff home page

    blockChangeText = models.CharField(max_length = 5000,default = "")                     # help text shown when time block changes

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return "Site Parameters"

    class Meta:
        verbose_name = 'Parameters'
        verbose_name_plural = 'Parameters'
    
    def json(self):
        return{
            "labManager":self.labManager.last_name + ", " + self.labManager.first_name,
            "subjectTimeZone":self.subjectTimeZone,
            "defaultShowUpFee":str(self.defaultShowUpFee),
            "invitationText":self.invitationText,
            "consentForm":self.consentForm,
            "heartHelpText":self.heartHelpText,
            "immuneHelpText":self.immuneHelpText,
            "paymentHelpText":self.paymentHelpText,
        }