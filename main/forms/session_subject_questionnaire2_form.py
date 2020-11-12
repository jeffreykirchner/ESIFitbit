from django import forms
from main.models import Session_subject_questionnaire2
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz
from main.globals.likertScales import Yes_No,Likert_change
from django.utils.safestring import mark_safe

class Session_subject_questionnaire2_form(forms.ModelForm):
        
    sleep_changed = forms.TypedChoiceField(label='As a result of participating in this study, I slept _________________ while I was participating, then before the study.', 
                                         choices=Likert_change.choices,    
                                         initial=Likert_change.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    sleep_changed_explaination = forms.CharField(label='How else did your sleep habits change? (Optional)',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    exercise_changed = forms.TypedChoiceField(label='As a result of participating in this study, I exercised _________________ while I was participating, then before the study.', 
                                         choices=Likert_change.choices,    
                                         initial=Likert_change.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    exercise_changed_explaination = forms.CharField(label='How else did your exercise habits change? (Optional)',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    health_concern = forms.TypedChoiceField(label='As a result of participating in this study, I will act with ____________________ concern for my health in the future. ', 
                                         choices=Likert_change.choices,    
                                         initial=Likert_change.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    health_concern_explaination = forms.CharField(label=mark_safe('If you anticipate a change: how will you change?<br>If do NOT anticipate a change: why won’t you change?'),
                                        required=True,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    class Meta:
        model=Session_subject_questionnaire2
        exclude=['session_subject']