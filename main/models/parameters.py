'''
site wide paramters
'''

from django.db import models


class Parameters(models.Model):
    '''
    site wide paramters
    '''
    contactEmail = models.CharField(max_length=1000, default="JohnSmith@abc.edu")  # primary contact for subjects
    experimentTimeZone = models.CharField(max_length=1000, default="US/Pacific")  # time zone the experiment is in
    maxDailyEarnings = models.DecimalField(decimal_places=2, max_digits=5, default=20)  # max money that can be paid to a subject per year
    siteURL = models.CharField(max_length=200, default="https://www.google.com/")  # site URL used for display in emails
    testEmailAccount = models.CharField(max_length=1000, default="")  # email account used for debug mode emails

    invitationTextSubject = models.CharField(max_length=1000, default="")  # email subject text for the single day invitation
    invitationText = models.CharField(max_length=10000, default="")  # email text for the single day invitation

    cancelationTextSubject = models.CharField(max_length=1000, default="")  # email subject text when an experiment is canceled
    cancelationText = models.CharField(max_length=10000, default="")  # email text when an experiment is canceled

    paypal_email_subject = models.CharField(max_length=200, default="You have a payment from <your_org>.")  # subject of paypal payment emails
    paypal_email_body = models.CharField(max_length=200, default="thanks for your participation!")  # body of paypal payment email

    consentFormRequired = models.BooleanField(default=True)  # true if subject must agree to special consent form before doing experiment

    questionnaire1Required = models.BooleanField(default=True)  # enable pre experiment questionnaire
    questionnaire2Required = models.BooleanField(default=True)  # enable post experiment questionnaire

    trackerDataOnly = models.BooleanField(default=True)  # only use data collected from fitness tracker

    manualHelpText = models.CharField(max_length=5000, default="")                      # help text shown to staff
    staffHomeHelpText = models.CharField(max_length=5000, default="")                   # help text shown to staff home page

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Parameters"

    class Meta:
        verbose_name = 'Parameters'
        verbose_name_plural = 'Parameters'

    def json(self):
        '''
        return json version of class
        '''

        return{
            "contactEmail": self.contactEmail,
        }
