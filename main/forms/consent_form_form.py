from xml.sax.xmlreader import AttributesNSImpl
from tinymce.widgets import TinyMCE

from django import forms
from main.models import Consent_forms


class Consent_form_form(forms.ModelForm):
    '''
    consent form form
    '''

    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={"size":"125"}))

    body_text = forms.CharField(label='Text',
                                widget=TinyMCE(attrs={"rows":"15","cols":"125"},
                                               mce_attrs ={
                                                      "height" : 600,
                                                      "theme": "silver",
                                                      "plugins": "directionality,paste,searchreplace,code,link",
                                                      "toolbar": "undo redo | styleselect | forecolor | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | link | code",
                                                      }))

    class Meta:
        model=Consent_forms
        fields = ('__all__')