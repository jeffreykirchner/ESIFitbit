from django import forms
from main.models import Session_subject
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class Subject_form(forms.ModelForm):
    name = forms.CharField(label='Full Name',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.name"})) 
    
    contact_email = forms.CharField(label='Contact Email',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.contact_email"}))
    
    student_id = forms.CharField(label='Student ID',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.student_id"}))

    gmail_address = forms.CharField(label='Gmail Address (FitBit)',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.gmail_address"}))
    
    gmail_password = forms.CharField(label='Gmail Password (FitBit)',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.gmail_password"}))

    display_color = forms.CharField(label='Display Color',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.display_color"}))
    

    class Meta:
        model=Session_subject
        exclude=['login_key','session','fitBitAccessToken','fitBitRefreshToken','fitBitUserId',
                 'soft_delete','consent_required','questionnaire1_required','questionnaire2_required',
                 'consent_signature','id_number','fitBitLastSynced','fitBitTimeZone']