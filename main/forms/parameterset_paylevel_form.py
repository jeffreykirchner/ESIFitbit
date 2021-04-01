'''
parameter set paylevel form
'''
from django import forms
from main.models import ParametersetPaylevel


class ParametersetPaylevelForm(forms.ModelForm):
    '''
    parameter set paylevel form
    '''

    score = forms.DecimalField(label='Activity score (0-1)',
                               min_value=0.0,
                               max_value=1.0,
                               widget=forms.NumberInput(attrs={"v-model":"current_paylevel.score", "step":"0.1"}))

    value = forms.DecimalField(label='Value for level ($)',
                               min_value=0,
                               widget=forms.NumberInput(attrs={"v-model":"current_paylevel.value"}))

    class Meta:
        model=ParametersetPaylevel
        fields = ('score','value')