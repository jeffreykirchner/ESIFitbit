from django import forms
from main.models import Session
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class Session_form(forms.ModelForm):
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={"v-model" : "session.title"})) 
    
    start_date = forms.DateField(label="Start Date",
                                 input_formats=['%m/%d/%Y'],
                                 error_messages={'invalid' : 'Format: M/D/YYYY'},                                                                                                           
                                 widget=forms.DateTimeInput(attrs={"v-model" : "session.start_date",
                                                                   "v-bind:disabled" : "session.editable === false"}))
    
    treatment = forms.TypedChoiceField(label='Treatment', 
                                       choices=Session.Treatment.choices,                   
                                       widget=forms.Select(attrs={"v-model" : "session.treatment"}))
    
    consent_required = forms.ChoiceField(label='Enable Consent Form',
                                         choices=((1, 'Yes'), (0,'No')),
                                         widget=forms.Select(attrs={"v-model" : "session.consent_required",
                                                                    "v-bind:disabled" : "session.editable === false"}))

    questionnaire1_required = forms.ChoiceField(label='Enable Pre-Questionnaire',
                                                choices=((1, 'Yes'), (0,'No')),
                                                widget=forms.Select(attrs={"v-model" : "session.questionnaire1_required",
                                                                           "v-bind:disabled" : "session.editable === false"}))

    questionnaire2_required = forms.ChoiceField(label='Enable Post-Questionnaire',
                                                choices=((1, 'Yes'), (0,'No')),
                                                widget=forms.Select(attrs={"v-model" : "session.questionnaire2_required",
                                                                           "v-bind:disabled" : "session.editable === false"}))                                     
    

    class Meta:
        model = Session
        fields = ('title', 'start_date', 'treatment','consent_required','questionnaire1_required','questionnaire2_required')