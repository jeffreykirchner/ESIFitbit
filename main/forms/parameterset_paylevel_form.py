'''
parameter set paylevel form
'''
from django import forms
from main.models import ParametersetPaylevel


class ParametersetPaylevelForm(forms.ModelForm):
    '''
    parameter set paylevel form
    '''

    score = forms.DecimalField(label='Activity score from 0-1',
                               min_value=0,
                               widget=forms.NumberInput(attrs={"v-model":"current_paylevel.score"}))

    value = forms.DecimalField(label='$ value for level',
                               min_value=0,
                               widget=forms.NumberInput(attrs={"v-model":"current_paylevel.value"}))

    class Meta:
        model=ParametersetPaylevel
        fields = ('__all__')