'''
parameter set paylevel form
'''
from django import forms
from main.models import ParametersetTimeBlock


class ParametersetTimeBlockForm(forms.ModelForm):
    '''
    parameter set paylevel form
    '''

    day_count = forms.IntegerField(label='Number of Days',
                               min_value=0,
                               widget=forms.NumberInput(attrs={"step":1,"min":0,"v-model":"current_time_block.day_count"}))

    heart_pay = forms.DecimalField(label='Heart Pay($)',
                                   min_value=0,
                                   widget=forms.NumberInput(attrs={"v-model":"current_time_block.heart_pay"}))

    immune_pay = forms.DecimalField(label='Sleep Pay($)',
                                    min_value=0,
                                    widget=forms.NumberInput(attrs={"v-model":"current_time_block.immune_pay"}))

    fixed_pay_per_day = forms.DecimalField(label='Fixed Pay($)',
                                           min_value=0,
                                           widget=forms.NumberInput(attrs={"v-model":"current_time_block.fixed_pay_per_day"}))

    class Meta:
        model=ParametersetTimeBlock
        fields = ('day_count', 'heart_pay', 'immune_pay', 'fixed_pay_per_day')