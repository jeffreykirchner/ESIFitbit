from django import forms
from main.models import Parameterset
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class Parameterset_form(forms.ModelForm):

    heart_activity_inital = forms.DecimalField(label='Heart Activity T1',
                            min_value=0.0001,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_activity_inital"}))

    heart_parameter_1 = forms.DecimalField(label='Heart Parameter 1',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_parameter_1"}))
    
    heart_parameter_2 = forms.DecimalField(label='Heart Parameter 2',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_parameter_2"}))
    
    heart_parameter_3 = forms.DecimalField(label='Heart Parameter 3',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_parameter_3"}))

    immune_activity_inital = forms.DecimalField(label='Immune Activity T1',
                            min_value=0.0001,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_activity_inital"}))

    immune_parameter_1 = forms.DecimalField(label='Immune Parameter 1',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_parameter_1"}))
    
    immune_parameter_2 = forms.DecimalField(label='Immune Parameter 2',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_parameter_2"}))
    
    immune_parameter_3 = forms.DecimalField(label='Immune Parameter 3',
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_parameter_3"}))
    
    treatment_pay_1 = forms.DecimalField(label='Treatment 1 Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_pay_1"}))
    
    treatment_pay_2 = forms.DecimalField(label='Treatment 2 Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_pay_2"}))

    treatment_pay_3 = forms.DecimalField(label='Treatment 3 Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_pay_3"}))

    treatment_1_day_count = forms.DecimalField(label='Treatment 1 Days',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_1_day_count"}))
    
    treatment_2_day_count = forms.DecimalField(label='Treatment 2 Days',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_2_day_count"}))

    treatment_3_day_count = forms.DecimalField(label='Treatment 3 Days',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_3_day_count"}))

    treatment_3_heart_bonus = forms.DecimalField(label='Heart Bonus ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_3_heart_bonus"}))

    treatment_3_immune_bonus = forms.DecimalField(label='Immune Bonus ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_3_immune_bonus"}))
    
    treatment_3_bonus_target_count = forms.IntegerField(label='Cutoff, better than Nth Subject / Total',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.treatment_3_bonus_target_count"}))

    class Meta:
        model=Parameterset
        fields = ('__all__')