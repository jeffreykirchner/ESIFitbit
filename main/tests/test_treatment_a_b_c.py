'''
tests for treatment A B C
'''
from datetime import datetime, timedelta
from decimal import Decimal

import logging
import json

from django.test import TestCase

from main.models import Session, Session_day_subject_actvity, ParametersetPaylevel
from main.globals import todaysDate, PageType, TimeBlock, NoticeType, round_half_away_from_zero

from main.views.staff.staff_home import createSession
from main.views.staff.staff_session import updateSession, addSubject, startSession, sendCancelations
from main.views import do_calc_a_b_c_treatments

#test past last day of experiment
class SessionBlockTests(TestCase):
    '''
    tests that block stats are correct
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

        #check on block 1 daily payments
        session_subject = session.session_subjects.first()
        self.assertEqual(session.parameterset.block_1_fixed_pay_per_day, session_subject.get_daily_payment_A_B_C(1))
        self.assertEqual(session.parameterset.block_1_fixed_pay_per_day, session_subject.get_daily_payment_A_B_C(4))


    def test_subject_averages(self):
        '''
        test subject's average calculations
        '''

        logger = logging.getLogger(__name__)

        session = self.session

        # r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        # self.assertEqual(r['status'],"success")
        # session = Session.objects.get(id = session.id)

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
        
        for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
            logger.info(f'heart activity: {activity.heart_activity} sleep activity: {activity.immune_activity} paypal today: {activity.paypal_today} period: {activity.session_day.period_number}')

        #check averages of no heart missed days
        self.assertEqual(0.1, float(session_subject.get_average_heart_score(1)))
        self.assertEqual(0.11, float(session_subject.get_average_heart_score(2)))
        self.assertEqual(0.12,float(session_subject.get_average_heart_score(4)))
        self.assertEqual(0.14,float(session_subject.get_average_heart_score(5)))
        self.assertEqual(0.15,float(session_subject.get_average_heart_score(7)))  
        self.assertEqual(0.17,float(session_subject.get_average_heart_score(8)))
        self.assertEqual(0.18,float(session_subject.get_average_heart_score(9)))
        self.assertEqual(0.19,float(session_subject.get_average_heart_score(12)))

        #check averages of no heart missed days
        self.assertEqual(0.2, float(session_subject.get_average_sleep_score(1)))
        self.assertEqual(0.21, float(session_subject.get_average_sleep_score(2)))
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
        # self.assertEqual(12, float(session_subject.get_earnings_in_block_so_far(1)))
        # self.assertEqual(12, float(session_subject.get_earnings_in_block_so_far(2)))
        # self.assertEqual(12,float(session_subject.get_earnings_in_block_so_far(4)))
        # self.assertEqual(9,float(session_subject.get_earnings_in_block_so_far(5)))
        # self.assertEqual(9,float(session_subject.get_earnings_in_block_so_far(7)))  
        # self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(8)))
        # self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(9)))
        # self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(12)))

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
        # self.assertEqual(12, float(session_subject.get_earnings_in_block_so_far(1)))
        # self.assertEqual(9, float(session_subject.get_earnings_in_block_so_far(2)))
        # self.assertEqual(9,float(session_subject.get_earnings_in_block_so_far(4)))
        # self.assertEqual(6,float(session_subject.get_earnings_in_block_so_far(5)))
        # self.assertEqual(6,float(session_subject.get_earnings_in_block_so_far(7)))  
        # self.assertEqual(15,float(session_subject.get_earnings_in_block_so_far(8)))
        # self.assertEqual(12,float(session_subject.get_earnings_in_block_so_far(9)))
        # self.assertEqual(12,float(session_subject.get_earnings_in_block_so_far(12)))

class SessionABCPayments(TestCase):
    '''
    tests treatment a b c payments
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
        session.save()

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'A'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

        r = json.loads(updateSession(data,session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")

        session = Session.objects.first()
        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        addSubject({},session.id)
        addSubject({},session.id)

        session = Session.objects.first()
        self.session = session

        #add in paylevels
        start_value = 1.00
        start_score = .14
        for i in range(8):
            ParametersetPaylevel.objects.create(parameterset=self.session.parameterset, value=start_value, score=start_score)
            start_value += 0.5
            start_score += 0.1
        
        ParametersetPaylevel.objects.create(parameterset=self.session.parameterset, value=5, score=0.99)

        for paylevel in ParametersetPaylevel.objects.all():
            logger.info(f'Paylevels {paylevel.score} {paylevel.value}')


    def test_block_1_payments_day_1(self):
        '''
        test that block 1 payments are calculated correctly
        ''' 

        #logger = logging.getLogger(__name__)

        session = self.session

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                start_heart += 0.01
                start_sleep += 0.01

                activity.paypal_today = True
                activity.save()

        results = do_calc_a_b_c_treatments()

        for result in results["A B C Lumpsum Calculations"]:
            self.assertEqual(result['payments'],[])
        
        #check for none payment everywhere else
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all():
                self.assertEqual(activity.payment_today, 0)

    def test_block_1_payments_day_4(self):
        '''
        test that block 1 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=3)

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                start_heart += 0.01
                start_sleep += 0.01

                activity.paypal_today = True
                activity.save()

        results = do_calc_a_b_c_treatments()

        #logger.info(results)

        for result in results["A B C Lumpsum Calculations"]:
            self.assertEqual(result['payments'],[])
        
        #check for none payment everywhere else
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all():
                self.assertEqual(activity.payment_today, 0)
    
    def test_block_1_payments_day_5(self):
        '''
        test that block 1 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=4)
        logger.info(f'test_block_1_payments_day_5 start date {session.start_date}')

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                start_heart += 0.01
                start_sleep += 0.01

                activity.paypal_today = True
                activity.save()

        results = do_calc_a_b_c_treatments()

        for result in results["A B C Lumpsum Calculations"]:
            for payment in result['payments']:
                self.assertEqual(payment['payment'], 12)
        
        #check for correct payment on last block
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 4)
            self.assertEqual(activity.payment_today, 12)
        
        #check for none payment everywhere else
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.exclude(session_day__period_number = 4):
                self.assertEqual(activity.payment_today, 0)
    
    def test_block_1_payments_day_5_missed_day(self):
        '''
        test that block 1 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=4)
        logger.info(f'test_block_1_payments_day_5 start date {session.start_date}')

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                start_heart += 0.01
                start_sleep += 0.01

                activity.paypal_today = True
                activity.save()
        
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 2)
            activity.paypal_today = False
            activity.save()

        results = do_calc_a_b_c_treatments()

        for result in results["A B C Lumpsum Calculations"]:
            for payment in result['payments']:
                self.assertEqual(payment['payment'], 9)
        
        #check for correct payment on last block
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 4)
            self.assertEqual(activity.payment_today, 9)
        
        #check for none payment everywhere else
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.exclude(session_day__period_number = 4):
                self.assertEqual(activity.payment_today, 0)
    
    def test_block_1_payments_day_6(self):
        '''
        test that block 2 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=5)

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                start_heart += 0.01
                start_sleep += 0.01

                activity.paypal_today = True
                activity.save()

        results = do_calc_a_b_c_treatments()

        #logger.info(results)

        for result in results["A B C Lumpsum Calculations"]:
            self.assertEqual(result['payments'],[])
        
        #check for none payment everywhere else
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all():
                self.assertEqual(activity.payment_today, 0)
    
    def test_block_1_payments_day_8(self):
        '''
        test that block 2 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=7)

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                activity.paypal_today = True
                activity.save()

                start_heart += 0.01
                start_sleep += 0.01            
            
            start_sleep = 0.2
            start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                logger.info(f"period {activity.session_day.period_number}, subject {activity.session_subject.id}, heart score {activity.heart_activity}, sleep score {activity.immune_activity}, pay pal today {activity.paypal_today}")

        results = do_calc_a_b_c_treatments()

        #logger.info(results)
        for result in results["A B C Lumpsum Calculations"]:
            for payment in result['payments']:
                self.assertEqual(payment['payment'], round_half_away_from_zero(3 * (3 + 8 * .15 + 8 * .25), 2))
        
        #check for none payment everywhere else
        #check for correct payment on last block
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 7)
            self.assertEqual(float(activity.payment_today), round_half_away_from_zero(3 * (3 + 8 * .15 + 8 * .25), 2))
    
    def test_block_1_payments_day_8_missed_day(self):
        '''
        test that block 2 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=7)

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                activity.paypal_today = True
                activity.save()

                start_heart += 0.01
                start_sleep += 0.01            
            
            start_sleep = 0.2
            start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 5)
            activity.paypal_today = False
            activity.save()

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                logger.info(f"period {activity.session_day.period_number}, subject {activity.session_subject.id}, heart score {activity.heart_activity}, sleep score {activity.immune_activity}, pay pal today {activity.paypal_today}")

        results = do_calc_a_b_c_treatments()

        #logger.info(results)
        for result in results["A B C Lumpsum Calculations"]:
            for payment in result['payments']:
                self.assertEqual(payment['payment'], round_half_away_from_zero(2 * (3 + 8 * .16 + 8 * .26), 2))
        
        #check for none payment everywhere else
        #check for correct payment on last block
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 7)
            self.assertEqual(float(activity.payment_today), round_half_away_from_zero(2 * (3 + 8 * .16 + 8 * .26), 2))
        
        #check for zeros
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.exclude(session_day__period_number = 7):
                self.assertEqual(activity.payment_today, 0)
    
    def test_block_1_payments_day_13_missed_day(self):
        '''
        test that block 3 payments are calculated correctly
        ''' 

        logger = logging.getLogger(__name__)

        session = self.session

        session.start_date = todaysDate() - timedelta(days=12)

        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                activity.paypal_today = True
                activity.save()

                start_heart += 0.01
                start_sleep += 0.01            
            
            start_sleep = 0.2
            start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 9)
            activity.paypal_today = False
            activity.save()

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                logger.info(f"period {activity.session_day.period_number}, subject {activity.session_subject.id}, heart score {activity.heart_activity}, sleep score {activity.immune_activity}, pay pal today {activity.paypal_today}")

        results = do_calc_a_b_c_treatments()

        #logger.info(results)
        for result in results["A B C Lumpsum Calculations"]:
            for payment in result['payments']:
                self.assertEqual(payment['payment'], round_half_away_from_zero(4 * (3 + 16 * .19 + 16 * .29), 2))
        
        #check for none payment everywhere else
        #check for correct payment on last block
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 12)
            self.assertEqual(float(activity.payment_today), round_half_away_from_zero(4 * (3 + 16 * .19 + 16 * .29), 2))
        
        #check for zeros
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.exclude(session_day__period_number = 12):
                self.assertEqual(activity.payment_today, 0)

    def test_b_c_paylevels(self):
        '''
        check that correct paylevel is return given a score level
        '''

        parmeter_set = self.session.parameterset

        self.assertEqual(1.00, parmeter_set.get_treatment_b_c_paylevel(Decimal('0')))
        self.assertEqual(1.00, parmeter_set.get_treatment_b_c_paylevel(Decimal('-1')))
        self.assertEqual(5.00, parmeter_set.get_treatment_b_c_paylevel(Decimal('1')))
        self.assertEqual(3.50, parmeter_set.get_treatment_b_c_paylevel(Decimal('0.64')))
        self.assertEqual(4.00, parmeter_set.get_treatment_b_c_paylevel(Decimal('0.65')))
    
    def test_b_payments_8_missed_day(self):
        '''
        test treatment b payments
        '''

        logger = logging.getLogger(__name__)

        session = self.session

        start_date = todaysDate() - timedelta(days=7)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'B'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

        r = json.loads(updateSession(data, session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        start_sleep = 0.2
        start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                activity.heart_activity = start_heart
                activity.immune_activity = start_sleep

                activity.paypal_today = True
                activity.save()

                start_heart += 0.01
                start_sleep += 0.01            
            
            start_sleep = 0.2
            start_heart = 0.1

        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 5)
            activity.paypal_today = False
            activity.save()

        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.all().order_by('session_day__period_number'):
                logger.info(f"period {activity.session_day.period_number}, subject {activity.session_subject.id}, heart score {activity.heart_activity}, sleep score {activity.immune_activity}, pay pal today {activity.paypal_today}")

        results = do_calc_a_b_c_treatments()

        #logger.info(results)
        for result in results["A B C Lumpsum Calculations"]:
            for payment in result['payments']:
                self.assertEqual(payment['payment'], round_half_away_from_zero(2 * (3 + 1.5 * .16 + 2 * .26), 2))
        
        #check for none payment everywhere else
        #check for correct payment on last block
        for session_subject in self.session.session_subjects.all():
            activity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 7)
            self.assertEqual(float(activity.payment_today), round_half_away_from_zero(2 * (3 + 1.5 * .16 + 2 * .26), 2))
        
        #check for zeros
        for session_subject in self.session.session_subjects.all():
            for activity in session_subject.Session_day_subject_actvities.exclude(session_day__period_number = 7):
                self.assertEqual(activity.payment_today, 0)

