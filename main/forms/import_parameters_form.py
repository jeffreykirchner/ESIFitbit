from django import forms
from django.contrib.auth.models import User
from main.models import Session

import logging
import re

#form
class Import_parameters_form(forms.Form):
    
    session =  forms.ModelChoiceField(label="Select session to copy.",
                                     queryset=Session.objects.filter(soft_delete=False),
                                     empty_label=None,
                                     widget=forms.Select(attrs={}))


    