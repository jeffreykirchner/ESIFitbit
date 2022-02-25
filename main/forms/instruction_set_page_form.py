'''
instruction set form
'''
from tinymce.widgets import TinyMCE

from django import forms
from main.models import InstructionSetPage


class InstructionSetPageForm(forms.ModelForm):
    '''
    instruction set form
    '''

    text = forms.CharField(label='PageText',
                           required=False, 
                           widget=TinyMCE(attrs={"rows":"15", 
                                                      "plugins": "link image code",
                                                      "cols":"125"}))

    class Meta:
        model=InstructionSetPage
        fields=['text']