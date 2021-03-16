'''
instruction set form
'''
from django import forms
from main.models import InstructionSetPage


class InstructionSetPageForm(forms.ModelForm):
    '''
    instruction set form
    '''

    text = forms.CharField(label='PageText',
                                widget=forms.Textarea(attrs={"rows":"20", "cols":"200"}))

    class Meta:
        model=InstructionSetPage
        fields=['text']