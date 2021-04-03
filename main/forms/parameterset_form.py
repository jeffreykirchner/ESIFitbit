from django import forms
from main.models import Parameterset,Consent_forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
import pytz

class Parameterset_form(forms.ModelForm):

    consent_form = forms.ModelChoiceField(label="Consent Form",
                                            empty_label=None,
                                            queryset=Consent_forms.objects.all(),
                                            widget=forms.Select(attrs={"v-model":"session.parameterset.consent_form"}))

    heart_activity_inital = forms.DecimalField(label='Heart Activity T1',
                            min_value=0.0001,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_activity_inital"}))

    heart_parameter_1 = forms.DecimalField(label='Heart P1',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_parameter_1"}))
    
    heart_parameter_2 = forms.DecimalField(label='Heart P2',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_parameter_2"}))
    
    heart_parameter_3 = forms.DecimalField(label='Heart P3',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.heart_parameter_3"}))

    immune_activity_inital = forms.DecimalField(label='Sleep Activity T1',
                            min_value=0.0001,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_activity_inital"}))

    immune_parameter_1 = forms.DecimalField(label='Sleep P1',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_parameter_1"}))
    
    immune_parameter_2 = forms.DecimalField(label='Sleep P2',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_parameter_2"}))
    
    immune_parameter_3 = forms.DecimalField(label='Sleep P3',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.immune_parameter_3"}))

    block_1_fixed_pay_per_day = forms.DecimalField(label='Block 1 Fixed Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_1_fixed_pay_per_day"}))
    
    block_2_fixed_pay_per_day = forms.DecimalField(label='Block 2 Fixed Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_2_fixed_pay_per_day"}))

    block_3_fixed_pay_per_day = forms.DecimalField(label='Block 3 Fixed Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_3_fixed_pay_per_day"}))
    
    minimum_wrist_minutes = forms.DecimalField(label='Minimum Wrist Minutes',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.minimum_wrist_minutes"}))
    
    block_1_heart_pay = forms.DecimalField(label='Block 1 Heart Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_1_heart_pay",
                                                            "v-bind:disabled" :"session.treatment === 'B'"}))
    
    block_2_heart_pay = forms.DecimalField(label='Block 2 Heart Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_2_heart_pay",
                                                            "v-bind:disabled" :"session.treatment === 'B'"}))

    block_3_heart_pay = forms.DecimalField(label='Block 3 Heart Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_3_heart_pay",
                                                            "v-bind:disabled" :"session.treatment === 'B'"}))
    
    block_1_immune_pay = forms.DecimalField(label='Block 1 Sleep Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_1_immune_pay",
                                                            "v-bind:disabled" :"session.treatment === 'B'"}))
    
    block_2_immune_pay = forms.DecimalField(label='Block 2 Sleep Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_2_immune_pay",
                                                            "v-bind:disabled" :"session.treatment === 'B'"}))

    block_3_immune_pay = forms.DecimalField(label='Block 3 Sleep Pay ($)',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_3_immune_pay",
                                                            "v-bind:disabled" :"session.treatment === 'B'"}))

    block_1_day_count = forms.DecimalField(label='Block 1 Days',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_1_day_count",
                                                            "v-bind:disabled" :"session.editable === false"}))
    
    block_2_day_count = forms.DecimalField(label='Block 2 Days',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_2_day_count",
                                                            "v-bind:disabled" :"session.editable === false"}))

    block_3_day_count = forms.DecimalField(label='Block 3 Days',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.block_3_day_count",
                                                            "v-bind:disabled" :"session.editable === false"}))

    y_min_heart = forms.DecimalField(label='Heart Y Minimum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.y_min_heart"}))
    
    y_max_heart = forms.DecimalField(label='Heart Y Maximum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.y_max_heart"}))
    
    y_ticks_heart = forms.DecimalField(label='Heart Y Ticks',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.y_ticks_heart"}))
    
    x_min_heart = forms.DecimalField(label='Heart X Minimum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.x_min_heart"}))
    
    x_max_heart = forms.DecimalField(label='Heart X Maximum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.x_max_heart"}))
    
    x_ticks_heart = forms.DecimalField(label='Heart X Ticks',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.x_ticks_heart"}))
    
    y_min_immune = forms.DecimalField(label='Sleep Y Minimum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.y_min_immune"}))
    
    y_max_immune = forms.DecimalField(label='Sleep Y Maximum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.y_max_immune"}))
    
    y_ticks_immune = forms.DecimalField(label='Sleep Y Ticks',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.y_ticks_immune"}))
    
    x_min_immune = forms.DecimalField(label='Sleep X Minimum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.x_min_immune"}))
    
    x_max_immune = forms.DecimalField(label='Sleep X Maximum',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.x_max_immune"}))
    
    x_ticks_immune = forms.DecimalField(label='Sleep X Ticks',
                            min_value=0,
                            widget=forms.NumberInput(attrs={"v-model":"session.parameterset.x_ticks_immune"}))

    class Meta:
        model=Parameterset
        fields = ('__all__')