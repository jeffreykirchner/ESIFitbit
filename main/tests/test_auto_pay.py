'''
test automatic payments
'''
from datetime import datetime, timedelta

import json
import logging

from django.test import TestCase

from main.models import Session, Session_day_subject_actvity
from main.globals import todaysDate
from main.views.staff.staff_home import createSession
from main.views import do_paypal
from main.views.staff.staff_session import updateSession, addSubject, startSession

class TestAutoPay(TestCase):
    '''
    test automatic payments
    '''
    fixtures = ['parameters.json', 'instruction_set.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        self.session = Session.objects.first()

        start_date = todaysDate() - timedelta(days=1)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}, {'name':'auto_pay','value':'1'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        addSubject({},self.session.id)
        addSubject({},self.session.id)

        self.session = Session.objects.get(id = self.session.id)
        self.session.parameterset.block_1_fixed_pay_per_day = 3
        self.session.parameterset.block_2_fixed_pay_per_day = 4
        self.session.parameterset.block_3_fixed_pay_per_day = 5
        self.session.parameterset.save()

        r = json.loads(startSession({}, self.session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")

        self.session = Session.objects.first()
        logger.info(f"Session start date {self.session.start_date} end date {self.session.end_date}")

        #store synced today
        for subject in self.session.session_subjects.all():
            subject.fitBitLastSynced = todaysDate()
            subject.save()
    
    def test_auto_pay(self):
        '''
        test auto pay feature
        '''
        logger = logging.getLogger(__name__) 

        yesterday = todaysDate() - timedelta(days=1)

        session = Session.objects.first()
        session_day = session.session_days.get(date = yesterday.date())

        logger.info(session_day)
       
        #test no payments
        session_day.payments_sent=False
        session_day.save()
        session.auto_pay = True
        session.save()

        r = do_paypal()
        self.assertEqual([],r['Do Paypal Cron'])                                                          

        #test payments
        pay = 1.00
        for activity in session_day.Session_day_subject_actvities_SD.all().order_by("id"):
            activity.paypal_today = True
            activity.payment_today = pay
            activity.save()
            pay += 1

        session = Session.objects.first()
        session_day = session.session_days.get(date = yesterday.date())
        session_day.payments_sent=False
        session_day.save()

        session.auto_pay = True
        session.save()

        r = do_paypal()
        self.assertNotEqual(2, len(r['Do Paypal Cron']))

        #check no double sending
        r = do_paypal()
        self.assertEqual(0, len(r['Do Paypal Cron']))

        #check auto pay off
        session = Session.objects.first()
        session_day = session.session_days.get(date = yesterday.date())
        session_day.payments_sent=False
        session_day.save()

        session.auto_pay = False
        session.save()

        r = do_paypal()
        logger.info(r)
        self.assertEqual(0, len(r['Do Paypal Cron']))

        








