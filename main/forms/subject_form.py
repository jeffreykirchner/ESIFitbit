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

    # gmail_address = forms.CharField(label='Gmail Address (FitBit)',
    #                         required=False,
    #                         widget=forms.TextInput(attrs={"v-model":"currentSubject.gmail_address"}))
    
    # gmail_password = forms.CharField(label='Gmail Password (FitBit)',
    #                         required=False,
    #                         widget=forms.TextInput(attrs={"v-model":"currentSubject.gmail_password"}))

    display_color = forms.CharField(label='Display Color',
                            widget=forms.TextInput(attrs={"v-model":"currentSubject.display_color"}))
    
    group_number = forms.IntegerField(label='Group Number',
                                      min_value=0,
                                      widget=forms.NumberInput(attrs={"value":"","step":1,"min":0, "v-model":"currentSubject.group_number"}))
    

    class Meta:
        model=Session_subject
        fields=('name', 'contact_email', 'student_id', 'display_color', 'group_number')