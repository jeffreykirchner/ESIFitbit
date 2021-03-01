from django import forms
from main.models import Session


class SessionFormAdmin(forms.ModelForm):


    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={"size":"125"}))
    
    allow_delete = forms.BooleanField(label='Allow Delete', required=False)

    canceled = forms.BooleanField(label='Canceled', required=False)
 
    soft_delete = forms.BooleanField(label='Deleted', required=False)


    class Meta:
        model=Session
        fields = ('title','allow_delete','canceled','soft_delete')