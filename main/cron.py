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

        p = Parameters.objects.first()
        tz = pytz.timezone(p.experimentTimeZone)
        d_today = datetime.now(tz)
        d_today = d_today.replace(hour=0,minute=0, second=0)

        sessions = Session.objects.filter(start_date__lt = d_today,soft_delete=False)

        for s in sessions:
            s.addNewSessionDays(d_today)

        logger.info(sessions)    
