'''
instruction set form
'''
from django import forms
from main.models import InstructionSetNotice


class InstructionSetNoticeForm(forms.ModelForm):
    '''
    instruction set form
    '''

    text = forms.CharField(label='Page Text',
                           required=False, 
                           widget=forms.Textarea(attrs={"rows":"20", "cols":"200"}))

    class Meta:
        model=InstructionSetNotice
        fields=['title','text']