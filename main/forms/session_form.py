from django import forms
from main.models import Session
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class Session_form(forms.ModelForm):
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={"v-model":"experiment.title",
                                                          "v-on:keyup":"mainFormChange1"})) 
    
    date = forms.DateTimeField(label="Start Date",
                               localize=True,
                               input_formats=['%m/%d/%Y'],
                               error_messages={'invalid': 'Format: M/D/YYYY H:MM am/pm ZZ'},                                                                                                           
                               widget = forms.DateTimeInput(attrs={"v-model":"currentSessionDay.date",                                                                 
                                                                   "v-on:change":"mainFormChange2"}))
    

    class Meta:
        model=Session
        fields = ('__all__')