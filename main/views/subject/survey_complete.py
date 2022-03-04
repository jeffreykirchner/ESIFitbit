'''
subject view
'''

import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from main.models import Session_day_subject_actvity



def Survey_Complete(request, activity_key):
    '''
    survey complete view
    '''

    if request.method == 'POST':

       pass

    else:
        logger = logging.getLogger(__name__) 
        logger.info(f"Suvey Complete {activity_key}")

        return_link = ""
        error = False

        try:
            session_day_subject_activity = Session_day_subject_actvity.objects.get(activity_key=activity_key)
            session_day_subject_activity.survey_complete = True
            session_day_subject_activity.save()

            return_link = session_day_subject_activity.session_subject.login_key
            logger.info(return_link)
        except ObjectDoesNotExist:
            logger.warning(f"Suvey Complete, not found: {activity_key}")
            error = True
        
        return render(request,'subject/survey_complete.html',{"error":error, "return_link" : return_link})



