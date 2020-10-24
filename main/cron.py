import logging
from django_cron import CronJobBase, Schedule
from datetime import datetime,timedelta
import pytz
from main.models import Session,Parameters

class checkStartNewDay(CronJobBase):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main.check_for_new_day'    # a unique code

    def do(self):
        logger = logging.getLogger(__name__)
        logger.info("Check if a new day has started for each session")

        sessions = Session.objects.filter(soft_delete=False)

        logger.info(sessions)

        for s in sessions:
            s.addNewSessionDays()

            
