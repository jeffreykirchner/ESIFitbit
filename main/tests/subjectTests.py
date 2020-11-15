
from django.test import TestCase
import logging

from main.models import Session
from main.globals.todaysDate import todaysDate
from datetime import datetime,timedelta
import json

from main.views.staff.staff_home import createSession
from main.views.staff.staff_session import updateSession,addSubject
from main.views.subject.subject_home import payMe

class subjectBeforeStartTestCase(TestCase):
    fixtures = ['parameters.json']

    session = None      #test session

    def setUp(self):
        logger = logging.getLogger(__name__)

        createSession({})

        #set sessoin start to tomorrow
        session = Session.objects.first()

        start_date = todaysDate()+timedelta(days=1)

        data = {'action': 'updateSession', 'formData': [{'name': 'title', 'value': '*** New Session ***'}, {'name': 'start_date', 'value': start_date.date()}, {'name': 'treatment', 'value': 'I'}]}

        r = json.loads(updateSession(data,session.id).content.decode("UTF-8"))
        self.assertEqual(r['status'],"success")

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

        session = self.session

        #before start
        session_subject = self.session.session_subjects.all().first()
        session_day = self.session.session_days.all().first()

        r = json.loads(payMe({},session_subject,session_day).content.decode("UTF-8"))
        self.assertEqual(r['status'],"fail")


