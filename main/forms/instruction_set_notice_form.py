'''
instruction set form
'''
from tinymce.widgets import TinyMCE

from django import forms
from main.models import InstructionSetNotice


class InstructionSetNoticeForm(forms.ModelForm):
    '''
    instruction set form
    '''

    text = forms.CharField(label='Page Text',
                           required=False, 
                           widget=TinyMCE(attrs={"rows":"15", 
                                                      "plugins": "link image code",
                                                      "cols":"125"}))

    class Meta:
        model=InstructionSetNotice
        fields=['title','text']