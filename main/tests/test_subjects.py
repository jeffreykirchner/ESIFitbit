'''
tests for subject screen
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
class SubjectCompleteTestCase(TestCase):
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

        start_date = todaysDate()-timedelta(days=4)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

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
        
    def testPayMe(self):
        '''after Start PayMe '''

        session = self.session

        #before start
        session_subject = self.session.session_subjects.all().first()
        session_day = self.session.getCurrentSessionDay()
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 4)
        session_day_subject_actvity.fitbit_on_wrist_minutes = self.session.parameterset

        session_subject.consent_required = False
        session_subject.questionnaire1_required = False
        session_subject.questionnaire2_required = False

        session_subject.save()

        #check session complete
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))    
        self.assertIn("Session day not found",r['message'])    
        # session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 4).first()
        # self.assertFalse(session_day_subject_actvity.paypal_today)   

#test last day of experiment
class SubjectLastDayTestCase(TestCase):
    fixtures = ['parameters.json', 'instruction_set.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()-timedelta(days=3)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

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
        
    def testPayMe(self):
        '''after Start PayMe '''

        session = self.session

        #before start
        session_subject = self.session.session_subjects.all().first()
        session_day = self.session.session_days.get(period_number = 4)
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.get(session_day__period_number = 4)

        session_subject.consent_required = False
        session_subject.questionnaire1_required = False

        session_subject.save()

        #check for questionnaire 2
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))    
        self.assertIn("Questionnaire 2 required",r['message'])    
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 4).first()
        self.assertFalse(session_day_subject_actvity.paypal_today)   

        session_subject.questionnaire2_required = False  
        session_subject.save()  

        #questionnaire 2 done
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))    
        self.assertEquals("",r['message'])    
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 4).first()
        self.assertTrue(session_day_subject_actvity.paypal_today) 

#test subject after experiment has started
class SubjectAfterStartTestCase(TestCase):
    fixtures = ['parameters.json' , 'instruction_set.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

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
        
    def testPayMe(self):
        '''after Start PayMe '''

        session = self.session

        #before start
        session_subject = self.session.session_subjects.all().first()
        session_day = self.session.session_days.all().first()
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()

        session_subject.consent_required = False
        session_subject.questionnaire1_required = False

        session_subject.save()

        #pay subject
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))    
        self.assertEquals("",r['message'])    
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()
        self.assertTrue(session_day_subject_actvity.paypal_today)        

        #check double pay
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))     
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()   
        self.assertIn("Double payment attempt",r['message'])

        #cancel and reload 
        r = json.loads(sendCancelations({'action': 'sendCancelations', 'cancelation_text_subject': 'ESI Fitbit study canceled.', 'cancelation_text': '[subject name],\r\n\r\nUnfortunately we had to cancel the online Fitbit study you have been participating in.\r\n\r\nNo further action is required on your part.\r\n\r\nIf you have any questions, do not reply to this email, please contact:\r\n[contact email]\r\n\r\nThank you for your understanding.'},session.id).content.decode("UTF-8"))
        self.assertTrue(r['success'])
        session = Session.objects.get(id = session.id)

        session_subject = session.session_subjects.all().first()
        session_day = session.session_days.all().first()
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()

        #check cancelation 
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))     
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()   
        self.assertIn("Session is canceled",r['message'])
    
    #test low and high wrist time
    def testWristTime(self):
        session = self.session

        #before start
        session_subject = self.session.session_subjects.all().first()


        session_day = self.session.session_days.get(period_number = 1)
        session_day.date = todaysDate() - timedelta(days=1)
        session_day.save()

        session_day = self.session.session_days.get(period_number = 2)
        session_day.date = todaysDate().date()
        session_day.save()
        session_day_subject_actvity = Session_day_subject_actvity.objects.get(session_day = session_day,session_subject = session_subject)

        session_subject.consent_required = False
        session_subject.questionnaire1_required = False

        session_subject.save()

        #minutes too low
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))    
        self.assertEquals("Pay Error: Wrist time too low.",r['message'])    
        session_day_subject_actvity = Session_day_subject_actvity.objects.get(session_day = session_day,session_subject = session_subject)
        self.assertFalse(session_day_subject_actvity.paypal_today)

        #minutes high enough
        session_day_m1 = self.session.session_days.get(period_number = 1)
        session_day_subject_actvity = Session_day_subject_actvity.objects.get(session_day = session_day_m1,session_subject = session_subject)
        session_day_subject_actvity.fitbit_on_wrist_minutes = self.session.parameterset.minimum_wrist_minutes
        session_day_subject_actvity.save()

        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))    
        self.assertEquals("",r['message'])    
        session_day_subject_actvity = Session_day_subject_actvity.objects.get(session_day = session_day,session_subject = session_subject)
        self.assertTrue(session_day_subject_actvity.paypal_today)

#test subject before experiment starts
class SubjectBeforeStartTestCase(TestCase):
    fixtures = ['parameters.json', 'instruction_set.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate() + timedelta(days=1)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'},{'name': 'instruction_set', 'value': '1'}]}

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

        self.session = session
        
    def testPayMe(self):
        '''Before Start PayMe '''
        logger = logging.getLogger(__name__)  

        session = self.session

        #before start
        session_subject = session.session_subjects.all().first()
        session_day = session.session_days.all().first()
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()

        #check session started
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))
        self.assertIn("Session not started",r['message'])
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()
        self.assertFalse(session_day_subject_actvity.paypal_today)

        #start and reload 
        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        session_subject = session.session_subjects.all().first()
        session_day = session.session_days.all().first()
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()

        #check for consent
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))
        self.assertIn("Consent required", r['message'])
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()
        self.assertFalse(session_day_subject_actvity.paypal_today)

        session_subject.consent_required = False

        #check questionnaire 1
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))
        self.assertIn("Questionnaire 1 required",r['message'])
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()
        self.assertFalse(session_day_subject_actvity.paypal_today)

        session_subject.questionnaire1_required = False

        #check that before start
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))
        self.assertIn("Session_day.date does not match today's date",r['message'])
        session_day_subject_actvity = session_subject.Session_day_subject_actvities.filter(session_day__period_number = 1).first()
        self.assertFalse(session_day_subject_actvity.paypal_today)

        #check that session_day_subject_actvity exits
        session_day_subject_actvity.delete()
        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))
        self.assertIn("Could not find session_day_subject_actvity",r['message'])

class SubjectInstructions(TestCase):
    '''
    test correct instructions and notices are shown
    '''
    fixtures = ['parameters.json', 'instruction_set.json']

    session = None

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        self.session = Session.objects.first()

        start_date = todaysDate()

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)

        self.session = Session.objects.get(id = self.session.id)
    
    def test_three_x_three_one(self):
        '''
        test experiment with a 3 x 3 x 3 time block one
        '''
        logger = logging.getLogger(__name__)

        session = self.session
        instruction_set = session.instruction_set

        #logger.info(self.session.instruction_set)

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3

        session.parameterset.save()
        session.calcEndDate()

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        #block one instructions
        heart_help_text = session.get_instruction_text(PageType.HEART)
        immune_help_text = session.get_instruction_text(PageType.SLEEP)
        payment_help_text = session.get_instruction_text(PageType.PAY)

        self.assertEqual(heart_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.HEART))
        self.assertEqual(immune_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.SLEEP))
        self.assertEqual(payment_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.PAY))

        #check for payment change notice
        p_number = session.getCurrentSessionDay().period_number

        notification_title = session.get_notice_title(p_number)
        notification_text = session.get_notice_text(p_number)

        self.assertEqual(notification_title, "")
        self.assertEqual(notification_text, "")

    def test_three_x_three_two(self):
        '''
        test experiment with a 3 x 3 x 3 time block two
        '''
        logger = logging.getLogger(__name__)

        session = self.session
        instruction_set = session.instruction_set

        #logger.info(self.session.instruction_set)

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3

        session.parameterset.save()

        start_date = todaysDate() - timedelta(4)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        heart_help_text = session.get_instruction_text(PageType.HEART)
        immune_help_text = session.get_instruction_text(PageType.SLEEP)
        payment_help_text = session.get_instruction_text(PageType.PAY)

        self.assertEqual(heart_help_text, instruction_set.get_page_text(TimeBlock.TWO, PageType.HEART))
        self.assertEqual(immune_help_text, instruction_set.get_page_text(TimeBlock.TWO, PageType.SLEEP))
        self.assertEqual(payment_help_text, instruction_set.get_page_text(TimeBlock.TWO, PageType.PAY))

        #check for payment change notice
        p_number = session.getCurrentSessionDay().period_number

        notification_title = session.get_notice_title(p_number)
        notification_text = session.get_notice_text(p_number)

        self.assertEqual(notification_title, instruction_set.get_notice_title(TimeBlock.TWO, NoticeType.START))
        self.assertEqual(notification_text, instruction_set.get_notice_text(TimeBlock.TWO, NoticeType.START))
   
    def test_three_x_three_three(self):
        '''
        test experiment with a 3 x 3 x 3 time block three
        '''
        logger = logging.getLogger(__name__)

        session = self.session
        instruction_set = session.instruction_set

        #logger.info(self.session.instruction_set)

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3

        session.parameterset.save()

        start_date = todaysDate() - timedelta(7)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        heart_help_text = session.get_instruction_text(PageType.HEART)
        immune_help_text = session.get_instruction_text(PageType.SLEEP)
        payment_help_text = session.get_instruction_text(PageType.PAY)

        self.assertEqual(heart_help_text, instruction_set.get_page_text(TimeBlock.THREE, PageType.HEART))
        self.assertEqual(immune_help_text, instruction_set.get_page_text(TimeBlock.THREE, PageType.SLEEP))
        self.assertEqual(payment_help_text, instruction_set.get_page_text(TimeBlock.THREE, PageType.PAY))

        #check for payment change notice
        p_number = session.getCurrentSessionDay().period_number

        notification_title = session.get_notice_title(p_number)
        notification_text = session.get_notice_text(p_number)

        self.assertEqual(notification_title, instruction_set.get_notice_title(TimeBlock.THREE, NoticeType.START))
        self.assertEqual(notification_text, instruction_set.get_notice_text(TimeBlock.THREE, NoticeType.START))

    def test_three_x_three_one_advance(self):
        '''
        test experiment with a 3 x 3 x 3 time block two advanced notice
        '''
        logger = logging.getLogger(__name__)

        session = self.session
        instruction_set = session.instruction_set

        #logger.info(self.session.instruction_set)

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3

        session.parameterset.save()

        start_date = todaysDate() - timedelta(2)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        heart_help_text = session.get_instruction_text(PageType.HEART)
        immune_help_text = session.get_instruction_text(PageType.SLEEP)
        payment_help_text = session.get_instruction_text(PageType.PAY)

        self.assertEqual(heart_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.HEART))
        self.assertEqual(immune_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.SLEEP))
        self.assertEqual(payment_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.PAY))

        #check for payment change notice
        p_number = session.getCurrentSessionDay().period_number

        notification_title = session.get_notice_title(p_number)
        notification_text = session.get_notice_text(p_number)

        self.assertEqual(notification_title, instruction_set.get_notice_title(TimeBlock.TWO, NoticeType.ADVANCE))
        self.assertEqual(notification_text, instruction_set.get_notice_text(TimeBlock.TWO, NoticeType.ADVANCE))

    def test_three_x_three_two_advance(self):
        '''
        test experiment with a 3 x 3 x 3 time block three advanced notice
        '''
        logger = logging.getLogger(__name__)

        session = self.session
        instruction_set = session.instruction_set

        #logger.info(self.session.instruction_set)

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3

        session.parameterset.save()

        start_date = todaysDate() - timedelta(5)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        heart_help_text = session.get_instruction_text(PageType.HEART)
        immune_help_text = session.get_instruction_text(PageType.SLEEP)
        payment_help_text = session.get_instruction_text(PageType.PAY)

        self.assertEqual(heart_help_text, instruction_set.get_page_text(TimeBlock.TWO, PageType.HEART))
        self.assertEqual(immune_help_text, instruction_set.get_page_text(TimeBlock.TWO, PageType.SLEEP))
        self.assertEqual(payment_help_text, instruction_set.get_page_text(TimeBlock.TWO, PageType.PAY))

        #check for payment change notice
        p_number = session.getCurrentSessionDay().period_number

        notification_title = session.get_notice_title(p_number)
        notification_text = session.get_notice_text(p_number)

        self.assertEqual(notification_title, instruction_set.get_notice_title(TimeBlock.THREE, NoticeType.ADVANCE))
        self.assertEqual(notification_text, instruction_set.get_notice_text(TimeBlock.THREE, NoticeType.ADVANCE))

    def test_fourteen_x_zero_advance(self):
        '''
        test experiment with a 14 x 0 x 0 time block one advanced notice
        '''
        logger = logging.getLogger(__name__)

        session = self.session
        instruction_set = session.instruction_set

        #logger.info(self.session.instruction_set)

        session.parameterset.block_1_day_count = 14
        session.parameterset.block_2_day_count = 0
        session.parameterset.block_3_day_count = 0

        session.parameterset.save()

        start_date = todaysDate() - timedelta(13)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        heart_help_text = session.get_instruction_text(PageType.HEART)
        immune_help_text = session.get_instruction_text(PageType.SLEEP)
        payment_help_text = session.get_instruction_text(PageType.PAY)

        self.assertEqual(heart_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.HEART))
        self.assertEqual(immune_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.SLEEP))
        self.assertEqual(payment_help_text, instruction_set.get_page_text(TimeBlock.ONE, PageType.PAY))

        #check for payment change notice
        p_number = session.getCurrentSessionDay().period_number

        notification_title = session.get_notice_title(p_number)
        notification_text = session.get_notice_text(p_number)

        self.assertEqual(notification_title, "")
        self.assertEqual(notification_text, "")

class SubjectPayments(TestCase):
    '''
    check that correct payments are being used during each time block
    '''
    fixtures = ['parameters.json', 'instruction_set.json']

    session = None

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        self.session = Session.objects.first()

        start_date = todaysDate()

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)
        addSubject({},self.session.id)

        self.session = Session.objects.get(id = self.session.id)
        self.session.parameterset.block_1_fixed_pay_per_day = 3
        self.session.parameterset.block_2_fixed_pay_per_day = 4
        self.session.parameterset.block_3_fixed_pay_per_day = 5
        self.session.parameterset.save()

    
    def test_three_x_three_one(self):
        '''
        test experiment with a 3 x 3 x 3 time block one
        '''
        logger = logging.getLogger(__name__)

        session = self.session

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3

        session.parameterset.save()
        session.calcEndDate()

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        #check for correct base payments block 1
        self.assertEqual(session.parameterset.get_fixed_pay(session.getCurrentSessionDay().period_number), session.parameterset.block_1_fixed_pay_per_day)
        self.assertEqual(session.parameterset.getHeartPay(session.getCurrentSessionDay().period_number), session.parameterset.block_1_heart_pay)
        self.assertEqual(session.parameterset.getImmunePay(session.getCurrentSessionDay().period_number), session.parameterset.block_1_immune_pay)
    
    def test_three_x_three_two(self):
        '''
        test experiment with a 3 x 3 x 3 time block one
        '''
        logger = logging.getLogger(__name__)

        session = self.session

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3
        session.parameterset.save()

        start_date = todaysDate() - timedelta(4)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        session.calcEndDate()

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        #check for correct base payments block 2
        self.assertEqual(session.parameterset.get_fixed_pay(session.getCurrentSessionDay().period_number), session.parameterset.block_2_fixed_pay_per_day)
        self.assertEqual(session.parameterset.getHeartPay(session.getCurrentSessionDay().period_number), session.parameterset.block_2_heart_pay)
        self.assertEqual(session.parameterset.getImmunePay(session.getCurrentSessionDay().period_number), session.parameterset.block_2_immune_pay)

    def test_three_x_three_three(self):
        '''
        test experiment with a 3 x 3 x 3 time block one
        '''
        logger = logging.getLogger(__name__)

        session = self.session

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3
        session.parameterset.save()

        start_date = todaysDate() - timedelta(7)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        session.calcEndDate()

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        #check for correct base payments block 3
        self.assertEqual(session.parameterset.get_fixed_pay(session.getCurrentSessionDay().period_number), session.parameterset.block_3_fixed_pay_per_day)
        self.assertEqual(session.parameterset.getHeartPay(session.getCurrentSessionDay().period_number), session.parameterset.block_3_heart_pay)
        self.assertEqual(session.parameterset.getImmunePay(session.getCurrentSessionDay().period_number), session.parameterset.block_3_immune_pay)

    def test_three_x_three_total_payment(self):
        '''
        test experiment with a 3 x 3 x 3 time block one
        '''
        logger = logging.getLogger(__name__)

        session = self.session

        session.parameterset.block_1_day_count = 3
        session.parameterset.block_2_day_count = 3
        session.parameterset.block_3_day_count = 3
        session.parameterset.save()

        parameterset = session.parameterset

        start_date = todaysDate() - timedelta(7)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'instruction_set', 'value': '2'}]}

        result = json.loads(updateSession(data, self.session.id).content.decode("UTF-8"))
        self.assertEqual(result['status'],"success")

        session = Session.objects.get(id = session.id)
        session.calcEndDate()
        session = Session.objects.get(id = session.id)

        session.calcEndDate()

        r = json.loads(startSession({},session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")
        session = Session.objects.get(id = session.id)

        logger.info(f"Session start date {session.start_date} end date {session.end_date}")

        #check for correct base payments
        session_subject = session.session_subjects.first()
        session_day_2day = session.getCurrentSessionDay()
        session_day_yda = session.getYesterdaysSessionDay()
        period_number = session.getCurrentSessionDay().period_number

        session_subject_activity_yda = session_day_yda.Session_day_subject_actvities_SD.get(session_subject=session_subject)

        session_subject_activity_yda.heart_activity_minutes = 20
        session_subject_activity_yda.immune_activity_minutes = 480

        session_subject_activity_yda.heart_activity = 0.6
        session_subject_activity_yda.immune_activity = 0.6

        session_subject_activity_yda.save()

        session_subject.calcTodaysActivity(period_number)
        session_subject_activity_2day = session_day_2day.Session_day_subject_actvities_SD.get(session_subject=session_subject)

        #wolfram alpha
        #solve x  = a * m + 0.5 * (1 + m) * (1 - a * m) * (f^b / (c +f^b)), a = 0.5, b = 3.0, c = 6, m = 0.6, f = 20 /15
        #solve x  = a * m + 0.5 * (1 + m) * (1 - a * m) * (f^b / (c +f^b)), a = 0.2, b = 4, c = 4, m = 0.6, f = 480 /240

        self.assertEqual(float(session_subject_activity_2day.heart_activity),round(0.458584,2))
        self.assertEqual(float(session_subject_activity_2day.immune_activity),round(0.6832,2))

        self.assertEqual(round(float(session_subject_activity_2day.getTodaysTotalEarnings()),2),
                          round(float(parameterset.block_3_fixed_pay_per_day + 
                                parameterset.block_3_heart_pay * session_subject_activity_2day.heart_activity +
                                parameterset.block_3_immune_pay * session_subject_activity_2day.immune_activity)
                               ,2))



