
from datetime import datetime,timedelta

import logging
import json

from django.test import TestCase

from main.models import Session,Session_day_subject_actvity
from main.globals.todaysDate import todaysDate

from main.views.staff.staff_home import createSession
from main.views.staff.staff_session import updateSession,addSubject,startSession,sendCancelations
from main.views.subject.subject_home import payMe

#test past last day of experiment
class subjectCompleteTestCase(TestCase):
    fixtures = ['parameters.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()-timedelta(days=4)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}]}

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
class subjectLastDayTestCase(TestCase):
    fixtures = ['parameters.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()-timedelta(days=3)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}]}

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
class subjectAfterStartTestCase(TestCase):
    fixtures = ['parameters.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}]}

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
class subjectBeforeStartTestCase(TestCase):
    fixtures = ['parameters.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate() + timedelta(days=1)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date().strftime("%m/%d/%Y")}, {'name': 'treatment', 'value': 'I'}, {'name': 'consent_required', 'value': '1'}, {'name': 'questionnaire1_required', 'value': '1'}, {'name': 'questionnaire2_required', 'value': '1'}]}

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


