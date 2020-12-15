from django import forms
from main.models import Session_subject_questionnaire1
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz
from main.globals.likertScales import Likert_importance,Likert_satisfaction,Likert_variation,Likert_variation2
from django.utils.safestring import mark_safe

class Session_subject_questionnaire1_form(forms.ModelForm):

    #sleep
    sleep_hours = forms.DecimalField(label='How many hours do you sleep in a typical night?',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"value":"","step":"0.1","min":0,"max":24}))
    
    sleep_importance = forms.TypedChoiceField(label='How important is it to you to get a good night’s sleep?', 
                                         choices=Likert_importance.choices,    
                                         initial=Likert_importance.DEFAULT,         
                                         widget=forms.Select(attrs={}))
    
    sleep_explanation = forms.CharField(label='Why? (Optional)',
                                        required=False,
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    #exercise
    exercise_minutes = forms.IntegerField(label='How many minutes do you exercise in a typical day?',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"value":"","step":1,"min":0,"max":24}))
    
    exercise_importance = forms.TypedChoiceField(label='How important is it to you to exercise?', 
                                         choices=Likert_importance.choices,
                                         initial=Likert_importance.DEFAULT,                   
                                         widget=forms.Select(attrs={}))
    
    exercise_explanation = forms.CharField(label='Why? (Optional)',
                                           required=False, 
                                           widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    #health importance
    health_importance = forms.TypedChoiceField(label='For you personally, how important is it to maintain your overall health? ', 
                                         choices=Likert_importance.choices,
                                         initial=Likert_importance.DEFAULT,                   
                                         widget=forms.Select(attrs={}))
    
    health_importance_explanation = forms.CharField(label='Why? (Optional)',
                                                    required=False,
                                                    widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))
    
    health_importance_actions = forms.CharField(label='For you personally, what does maintaining your health include? ',
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))
    
    health_satisfaction = forms.TypedChoiceField(label='How satisfied are you with your current efforts to maintain your health?', 
                                         choices=Likert_satisfaction.choices,
                                         initial=Likert_satisfaction.DEFAULT,                   
                                         widget=forms.Select(attrs={}))

    sleep_variation = forms.TypedChoiceField(label='How much day to day variation is there in the amount of time you spend sleeping?', 
                                         choices=Likert_variation.choices,
                                         initial=Likert_variation.DEFAULT,                   
                                         widget=forms.Select(attrs={}))

    sleep_variation_explanation = forms.CharField(label='For you personally, what are the typical reasons that you might not get a good night’s sleep?',
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    exercise_variation = forms.TypedChoiceField(label='How much day to day variation is there in the amount of time you spend exercising?', 
                                         choices=Likert_variation2.choices,
                                         initial=Likert_variation2.DEFAULT,                   
                                         widget=forms.Select(attrs={}))

    exercise_variation_explanation = forms.CharField(label='For you personally, what are the typical reasons that you might not exercise daily?',
                                        widget=forms.Textarea(attrs={"rows":"5", "cols":"75"}))

    #address
    address_full_name = forms.CharField(label=mark_safe('Mailing Address<br>Full Name'),
                                         widget=forms.TextInput(attrs={}))

    address_line_1 = forms.CharField(label=mark_safe('Address Line 1'),
                                         widget=forms.TextInput(attrs={"placeholder":"Street Address",}))

    address_line_2 = forms.CharField(label=mark_safe('Address Line 2'),
                                         required=False,
                                         widget=forms.TextInput(attrs={"placeholder":"Apartment, suite, unit, building, floor, etc.",}))

    address_city = forms.CharField(label=mark_safe('City'),
                                         widget=forms.TextInput(attrs={}))

    address_state = forms.CharField(label=mark_safe('State'),
                                         widget=forms.TextInput(attrs={}))

    address_zip_code = forms.CharField(label=mark_safe('Zip Code'),
                                         widget=forms.TextInput(attrs={}))

    class Meta:
        model=Session_subject_questionnaire1
        exclude=['session_subject']