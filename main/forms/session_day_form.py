'''
form for session model
'''
from django import forms
from main.models import Session_day

class SessionDayForm(forms.ModelForm):
    '''
    form for session day model
    '''
    survey_link = forms.CharField(label='Link',
                                  required=False,
                                  widget=forms.TextInput(attrs={"v-model" : "current_session_day.survey_link"}))

    survey_required = forms.ChoiceField(label='Enable Survey',
                                                choices=((1, 'Yes'), (0,'No')),
                                                widget=forms.Select(attrs={"v-model" : "current_session_day.survey_required"}))

    class Meta:
        model = Session_day
        fields = ('survey_link', 'survey_required')
    

    def clean_survey_link(self):
       
        
        try:
           survey_link = self.data.get('survey_link')
           survey_required = self.data.get('survey_required')

           if (survey_required == '1' or survey_required == 1) and not "http" in survey_link:
               raise forms.ValidationError('Invalid link')
            
        except ValueError:
            raise forms.ValidationError('Invalid Entry')

        return survey_link