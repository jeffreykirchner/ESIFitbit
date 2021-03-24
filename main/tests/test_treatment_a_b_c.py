'''
tests for treatment A B C
'''
from datetime import datetime,timedelta

import logging
import json

from django.test import TestCase

from main.models import Session, Session_day_subject_actvity
from main.globals import todaysDate, PageType, TimeBlock, NoticeType

from main.views.staff.staff_home import createSession
from main.views.staff.staff_session import updateSession, addSubject, startSession, sendCancelations
from main.views.subject.subject_home import payMe

#test past last day of experiment
class SessionBlockTests(TestCase):
    '''
    tests for subject screen
    '''
    fixtures = ['parameters.json', 'instruction_set.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 5

        session.parameterset.save()
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'A'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

        r = json.loads(updateSession(data,session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")

        session = Session.objects.first()
        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        addSubject({},session.id)
        addSubject({},session.id)
        addSubject({},session.id)
        addSubject({},session.id)
        addSubject({},session.id)
        addSubject({},session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")

        session = Session.objects.first()
        self.session = session

        Session_day_subject_actvity.objects.filter(session_day__session = session).update(fitbit_on_wrist_minutes = session.parameterset.minimum_wrist_minutes)
        
    def test_block_length(self):
        '''test block level counts '''

        session = self.session

        #check block length
        self.assertEqual(4, session.parameterset.get_block_day_count(1))
        self.assertEqual(4, session.parameterset.get_block_day_count(2))
        self.assertEqual(4, session.parameterset.get_block_day_count(4))  
        self.assertEqual(3, session.parameterset.get_block_day_count(5))
        self.assertEqual(3, session.parameterset.get_block_day_count(7))  
        self.assertEqual(5,session.parameterset.get_block_day_count(8))
        self.assertEqual(5,session.parameterset.get_block_day_count(12))

        #get first period
        self.assertEqual(1, session.parameterset.get_block_first_period(1))
        self.assertEqual(1, session.parameterset.get_block_first_period(2))
        self.assertEqual(1, session.parameterset.get_block_first_period(4))  
        self.assertEqual(5, session.parameterset.get_block_first_period(5))
        self.assertEqual(5, session.parameterset.get_block_first_period(7))  
        self.assertEqual(8,session.parameterset.get_block_first_period(8))
        self.assertEqual(8,session.parameterset.get_block_first_period(9))
        self.assertEqual(8,session.parameterset.get_block_first_period(12))

        #get last period
        self.assertEqual(4, session.parameterset.get_block_last_period(1))
        self.assertEqual(4, session.parameterset.get_block_last_period(2))
        self.assertEqual(4, session.parameterset.get_block_last_period(4))  
        self.assertEqual(7, session.parameterset.get_block_last_period(5))
        self.assertEqual(7, session.parameterset.get_block_last_period(7))  
        self.assertEqual(12,session.parameterset.get_block_last_period(8))
        self.assertEqual(12,session.parameterset.get_block_last_period(9))
        self.assertEqual(12,session.parameterset.get_block_last_period(12))

        #check pay date
        self.assertEqual(todaysDate().date() + timedelta(days=4), session.get_block_pay_date(2))
        self.assertEqual(todaysDate().date() + timedelta(days=4), session.get_block_pay_date(4))
        self.assertEqual(todaysDate().date() + timedelta(days=7), session.get_block_pay_date(5))
        self.assertEqual(todaysDate().date() + timedelta(days=7), session.get_block_pay_date(7))
        self.assertEqual(todaysDate().date() + timedelta(days=12), session.get_block_pay_date(8))
        self.assertEqual(todaysDate().date() + timedelta(days=12), session.get_block_pay_date(12))

        #check daily pay not heart pay
        self.assertEqual(session.parameterset.block_1_fixed_pay_per_day, session.get_daily_payment_A_B_C(1))
        self.assertEqual(session.parameterset.block_1_fixed_pay_per_day, session.get_daily_payment_A_B_C(4))


    def test_subject_averages(self):
        '''
        test subject's average calculations
        '''

        logger = logging.getLogger(__name__)

        session = self.session

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        session_subject = session.session_subjects.first()

        start_sleep = 0.2
        start_heart = 0.1
        for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
            activity.heart_activity = start_heart
            activity.immune_activity = start_sleep

            start_heart += 0.01
            start_sleep += 0.01

            activity.paypal_today = True
            activity.save()
        
        # for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
        #     logger.info(f'heart activity: {activity.heart_activity} sleep activity: {activity.immune_activity} paypal today: {activity.paypal_today} period: {activity.session_day.period_number}')

        #check averages of no heart missed days
        self.assertEqual(0.1, float(session_subject.get_average_heart_score(1)))
        self.assertEqual(0.1, float(session_subject.get_average_heart_score(2)))
        self.assertEqual(0.12,float(session_subject.get_average_heart_score(4)))
        self.assertEqual(0.14,float(session_subject.get_average_heart_score(5)))
        self.assertEqual(0.15,float(session_subject.get_average_heart_score(7)))  
        self.assertEqual(0.17,float(session_subject.get_average_heart_score(8)))
        self.assertEqual(0.18,float(session_subject.get_average_heart_score(9)))
        self.assertEqual(0.19,float(session_subject.get_average_heart_score(12)))

        #check averages of no heart missed days
        self.assertEqual(0.2, float(session_subject.get_average_sleep_score(1)))
        self.assertEqual(0.2, float(session_subject.get_average_sleep_score(2)))
        self.assertEqual(0.22,float(session_subject.get_average_sleep_score(4)))
        self.assertEqual(0.24,float(session_subject.get_average_sleep_score(5)))
        self.assertEqual(0.25,float(session_subject.get_average_sleep_score(7)))  
        self.assertEqual(0.27,float(session_subject.get_average_sleep_score(8)))
        self.assertEqual(0.28,float(session_subject.get_average_sleep_score(9)))
        self.assertEqual(0.29,float(session_subject.get_average_sleep_score(12)))

        #get missed checkins
        self.assertEqual(0, float(session_subject.get_missed_checkins(1)))
        self.assertEqual(0, float(session_subject.get_missed_checkins(2)))
        self.assertEqual(0,float(session_subject.get_missed_checkins(4)))
        self.assertEqual(0,float(session_subject.get_missed_checkins(5)))
        self.assertEqual(0,float(session_subject.get_missed_checkins(7)))  
        self.assertEqual(0,float(session_subject.get_missed_checkins(8)))
        self.assertEqual(0,float(session_subject.get_missed_checkins(9)))
        self.assertEqual(0,float(session_subject.get_missed_checkins(12)))

        #get earnings so far
        self.assertEqual(12, float(session_subject.get_earnings_in_block_so_far(1)))
        self.assertEqual(12, float(session_subject.get_earnings_in_block_so_far(2)))
        self.assertEqual(12,float(session_subject.get_earnings_in_block_so_far(4)))
        self.assertEqual(9,float(session_subject.get_earnings_in_block_so_far(5)))
        self.assertEqual(9,float(session_subject.get_earnings_in_block_so_far(7)))  
        self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(8)))
        self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(9)))
        self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(12)))

        #insert missed days
        session_subject.Session_day_subject_actvities.filter(session_day__period_number = 2).update(paypal_today=False)
        session_subject.Session_day_subject_actvities.filter(session_day__period_number = 5).update(paypal_today=False)
        session_subject.Session_day_subject_actvities.filter(session_day__period_number = 9).update(paypal_today=False)

        for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
            logger.info(f'heart activity: {activity.heart_activity} sleep activity: {activity.immune_activity} paypal today: {activity.paypal_today} period: {activity.session_day.period_number}')

        #heart scores
        self.assertEqual(0.1, float(session_subject.get_average_heart_score(1)))
        self.assertEqual(0.1, float(session_subject.get_average_heart_score(2)))
        self.assertEqual(0.12,float(session_subject.get_average_heart_score(4)))
        self.assertEqual(-1,float(session_subject.get_average_heart_score(5)))
        self.assertEqual(0.16,float(session_subject.get_average_heart_score(7)))  
        self.assertEqual(0.17,float(session_subject.get_average_heart_score(8)))
        self.assertEqual(0.17,float(session_subject.get_average_heart_score(9)))
        self.assertEqual(0.19,float(session_subject.get_average_heart_score(12)))

        #sleep scores
        self.assertEqual(0.20, float(session_subject.get_average_sleep_score(1)))
        self.assertEqual(0.20, float(session_subject.get_average_sleep_score(2)))
        self.assertEqual(0.22,float(session_subject.get_average_sleep_score(4)))
        self.assertEqual(-1,float(session_subject.get_average_sleep_score(5)))
        self.assertEqual(0.26,float(session_subject.get_average_sleep_score(7)))  
        self.assertEqual(0.27,float(session_subject.get_average_sleep_score(8)))
        self.assertEqual(0.27,float(session_subject.get_average_sleep_score(9)))
        self.assertEqual(0.29,float(session_subject.get_average_sleep_score(12)))

        #missed checkins
        self.assertEqual(0, float(session_subject.get_missed_checkins(1)))
        self.assertEqual(1, float(session_subject.get_missed_checkins(2)))
        self.assertEqual(1,float(session_subject.get_missed_checkins(4)))
        self.assertEqual(1,float(session_subject.get_missed_checkins(5)))
        self.assertEqual(1,float(session_subject.get_missed_checkins(7)))  
        self.assertEqual(0,float(session_subject.get_missed_checkins(8)))
        self.assertEqual(1,float(session_subject.get_missed_checkins(9)))
        self.assertEqual(1,float(session_subject.get_missed_checkins(12)))

        #get earnings so far
        self.assertEqual(12, float(session_subject.get_earnings_in_block_so_far(1)))
        self.assertEqual(9, float(session_subject.get_earnings_in_block_so_far(2)))
        self.assertEqual(9,float(session_subject.get_earnings_in_block_so_far(4)))
        self.assertEqual(6,float(session_subject.get_earnings_in_block_so_far(5)))
        self.assertEqual(6,float(session_subject.get_earnings_in_block_so_far(7)))  
        self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(8)))
        self.assertEqual(12,float(session_subject.get_earnings_in_block_so_far(9)))
        self.assertEqual(12,float(session_subject.get_earnings_in_block_so_far(12)))
            


