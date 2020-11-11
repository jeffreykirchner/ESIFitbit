from django import forms
from main.models import Session_subject_questionnaire1
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz
from main.globals.likertScales import Yes_No

class Session_subject_questionnaire1_form(forms.ModelForm):
        
    sleep_changed = forms.TypedChoiceField(label='Did participating in this study change your sleep habits while you were participating?', 
                                         choices=Yes_No.choices,    
                                         initial=Yes_No.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    sleep_changed_explaination = forms.CharField(label='If you did change, how did you change?',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    exercise_changed = forms.TypedChoiceField(label='Did participating in this study change your exercise habits while you were participating?', 
                                         choices=Yes_No.choices,    
                                         initial=Yes_No.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    exercise_changed_explaination = forms.CharField(label='If you did change, how did you change?',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    health_concern = forms.TypedChoiceField(label='Did participating in this study change the way you will act concerning your health in the future? ', 
                                         choices=Yes_No.choices,    
                                         initial=Yes_No.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    health_concern_explaination = forms.CharField(label='If YES: how will you change? If NO: why won’t you change?',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    class Meta:
        model=Session_subject_questionnaire1
        exclude=['session_subject']