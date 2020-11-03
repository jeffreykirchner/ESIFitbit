from django import forms
from main.models import Session
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class Session_form(forms.ModelForm):
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={"v-model":"session.title"})) 
    
    start_date = forms.DateField(label="Start Date",
                               input_formats=['%m/%d/%Y'],
                               error_messages={'invalid': 'Format: M/D/YYYY'},                                                                                                           
                               widget = forms.DateTimeInput(attrs={"v-model":"session.start_date",
                                                                   "v-bind:disabled" :"session.editable === false"}))
    
    treatment = forms.TypedChoiceField(label='Treatment', 
                                         choices=Session.Treatment.choices,                   
                                         widget=forms.Select(attrs={"v-model":"session.treatment"}))
    

    class Meta:
        model=Session
        exclude=['soft_delete','parameterset','started','end_date','invitations_sent','invitation_text','invitation_text_subject']