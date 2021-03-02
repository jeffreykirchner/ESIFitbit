from django import forms
from main.models import Consent_forms


class Consent_form_form(forms.ModelForm):


    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={"size":"125"}))

    body_text = forms.CharField(label='Text',
                                widget=forms.Textarea(attrs={"rows":"30", "cols":"125"}))


    class Meta:
        model=Consent_forms
        fields = ('__all__')