from django import forms
from main.models import Parameters
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class Parameters_form(forms.ModelForm):
    contactEmail = forms.CharField(label='Contact Email Address',
                                         widget=forms.TextInput(attrs={"size":"125"})) 
    
    maxDailyEarnings = forms.CharField(label='Max Daily Earnings ($)',
                                       widget=forms.NumberInput(attrs={}))
    
    siteURL = forms.CharField(label='Site URL',
                                         widget=forms.TextInput(attrs={"size":"125"}))

    testEmailAccount = forms.CharField(label='Test Email Account',
                                         widget=forms.TextInput(attrs={"size":"125"}))

    invitationTextSubject = forms.CharField(label='Welcome Email, Subject',
                                         widget=forms.TextInput(attrs={"size":"125"}))

    invitationText = forms.CharField(label='Welcome Email, Text',
                                     widget=forms.Textarea(attrs={"rows":"15", "cols":"125"}))


    cancelationTextSubject = forms.CharField(label='Cancelation Email, Subject',
                                        widget=forms.TextInput(attrs={"size":"125"}))

    cancelationText = forms.CharField(label='Cancelation Email, Text',
                                     widget=forms.Textarea(attrs={"rows":"15", "cols":"125"}))
    
    consentFormRequired = forms.ChoiceField(label='Consent Form Required',
                                        choices=((True, 'Yes'), (False,'No' )),                 
                                        widget=forms.Select)

    questionnaire1Required = forms.ChoiceField(label='Pre-Study Questionnaire',
                                        choices=((True, 'Yes'), (False,'No' )),                 
                                        widget=forms.Select)

    questionnaire2Required = forms.ChoiceField(label='Post-Study Questionnaire',
                                        choices=((True, 'Yes'), (False,'No' )),                 
                                        widget=forms.Select)

    experimentTimeZone = forms.ChoiceField(label="Study Timezone",
                                        choices=[(tz, tz) for tz in pytz.all_timezones])
    
    trackerDataOnly = forms.ChoiceField(label='Only Fitness Tracker Data',
                                        choices=((True, 'Yes'), (False,'No' )),                 
                                        widget=forms.Select)

    heartHelpText = forms.CharField(label='Heart Help Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))

    immuneHelpText = forms.CharField(label='Immune Help Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))

    paymentHelpText = forms.CharField(label='Non-Basline Payment Help Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))

    paymentHelpTextBaseline = forms.CharField(label='Basline Payment Help Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"})) 

    manualHelpText = forms.CharField(label='Session Help Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))

    staffHomeHelpText = forms.CharField(label='Session List Help Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))  

    blockChangeText = forms.CharField(label='Time Block Change Text',
                                     widget=forms.Textarea(attrs={"rows":"25", "cols":"125"}))                                                              

    class Meta:
        model=Parameters
        fields = ('__all__')