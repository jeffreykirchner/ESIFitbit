from django import forms
from main.models import Session_subject_questionnaire2
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz
from main.globals.likertScales import Yes_No, Likert_change, SexAtBirth, GenderIdentity
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
    
    holiday_break_explaination = forms.CharField(label=mark_safe('How did you spend your spring break?'),
                                                 required=True,
                                                 widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    sex_at_birth = forms.TypedChoiceField(label='What was your sex at birth?', 
                                          required=True,
                                          choices=SexAtBirth.choices,    
                                          initial=SexAtBirth.DEFAULT,         
                                          widget=forms.Select(attrs={}))
    
    gender_identity = forms.TypedChoiceField(label='To which gender identity do you most identify?', 
                                             required=True,  
                                             choices=GenderIdentity.choices,    
                                             initial=GenderIdentity.DEFAULT,         
                                             widget=forms.Select(attrs={}))

    gender_identity_fillin = forms.CharField(label="",
                                             required=False,
                                             widget=forms.TextInput(attrs={"size":"125",
                                                                           "placeholder":"Self describe your gender identity"}))



    class Meta:
        model=Session_subject_questionnaire2
        fields=('sleep_changed', 'sleep_changed_explaination', 'exercise_changed', 'exercise_changed_explaination', 
                'health_concern', 'health_concern_explaination', 'holiday_break_explaination' , 'sex_at_birth', 'gender_identity',
                'gender_identity_fillin')

    
    def clean_gender_identity_fillin(self):
        gender_identity_fillin = self.data['gender_identity_fillin']

        if self.data['gender_identity'] == 'Describe':
            if gender_identity_fillin == '':
                 raise forms.ValidationError('Field Required')

        return gender_identity_fillin