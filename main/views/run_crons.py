'''
when view is requested check for cron jobs
'''
import logging

from django.views.generic import View
from django.http import JsonResponse

from main.globals import todaysDate
from main.views import Session_day
from datetime import timedelta

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

        response.append(self.do_paypal())
        response.append(self.do_calc_daily_payments())

        logger.info(response)

        return JsonResponse({"response" : response}, safe=False)


    def do_paypal(self):
        '''
        check for Induvidual treatments that need to be paid and send paypal payment.
        '''

        logger = logging.getLogger(__name__) 

        yesterdays_date = todaysDate() - timedelta(days=1)
        
        yesterdays_sessions = Session_day.objects.filter(date = yesterdays_date.date()) \
                                                 .filter(payments_sent = False) \
                                                 .filter(session__treatment = "I")

        result = {"Do Paypal Cron" : yesterdays_sessions}

        return result
    
    def do_calc_daily_payments(self):
        '''
        check for Induvidual Lumpsum treatments that need to have their payments calculated and fitbit data pulled.
        '''

        logger = logging.getLogger(__name__) 

        result = {"Do Daily Lumpsum Payments" : "result here"}

        return result

