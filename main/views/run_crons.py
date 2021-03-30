'''
when view is requested check for cron jobs
'''
from datetime import timedelta

import logging

from django.views.generic import View
from django.http import JsonResponse

from main.globals import todaysDate, do_ppms, todays_time
from main.views import Session_day
from main.models import Parameters

class RunCronsView(View):
    '''
    check and run crons
    '''

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        logger = logging.getLogger(__name__)

        response = []

        #do any A B C treatment calcs needed
        response.append(do_calc_a_b_c_treatments())

        #send payments
        response.append(do_paypal())
        
        logger.info(response)

        return JsonResponse({"response": response}, safe=False)


def do_paypal():
    '''
    check for Induvidual treatments that need to be paid and send paypal payment.
    '''

    target_time = todaysDate().replace(hour=0, minute=5).time()

    if todays_time() <= target_time:
        return {"Do Paypal Cron" : "Payment time not reached"}

    parm = Parameters.objects.first()

    #logger = logging.getLogger(__name__)

    yesterdays_date = todaysDate() - timedelta(days=1)

    yesterdays_sessions = Session_day.objects.filter(date=yesterdays_date.date()) \
                                             .filter(payments_sent = False) \
                                             .filter(session__soft_delete = False) \
                                             .prefetch_related("Session_day_subject_actvities_SD")

    #logger.info(yesterdays_sessions)

    # build ppms request
    #

    result_list = []

    for session_d in yesterdays_sessions:
        payments_list = []

        for subject_activity in session_d.Session_day_subject_actvities_SD.all() \
                                         .filter(session_subject__soft_delete = False) \
                                         .select_related("session_subject") :

            if subject_activity.payment_today > 0:

                payments_list.append({
                    "email" : subject_activity.session_subject.contact_email,
                    "amount" : subject_activity.payment_today,
                    "note" : f'{subject_activity.session_subject.name}, {parm.paypal_email_body}',
                    "memo" : f'SD_ID: {session_d.id}, U_ID: {subject_activity.session_subject.id}'
                })

        if len(payments_list) > 0:
            result = do_ppms(payments_list, session_d.id, parm.paypal_email_subject)
            session_d.payments_result_message = result["error_message"]
            session_d.save()

            result_list.append(result)

    yesterdays_sessions.update(payments_sent = True)

    return {"Do Paypal Cron": result_list}


def do_calc_a_b_c_treatments():
    '''
    check for A B C treatments for lumpsum payments.
    '''

    logger = logging.getLogger(__name__)

    yesterdays_date = todaysDate() - timedelta(days=1)

    #check for yesterday's sessions that fall on payday
    yesterdays_sessions = Session_day.objects.filter(date=yesterdays_date.date()) \
                                             .filter(payments_sent = False) \
                                             .filter(session__soft_delete = False) \
                                             .exclude(session__treatment = "I") \
                                             .exclude(session__treatment = "Base")
    
    payments_list = []

    logger.info(f'do_calc_a_b_c_treatments {yesterdays_sessions}')

    for session_d in yesterdays_sessions:
        payments_list.append(session_d.calc_a_b_c_block_payments())

    return {"A B C Lumpsum Calculations": payments_list}
