import logging
from main.models import Parameters
from datetime import datetime,timedelta
import pytz

#get todays, time zone adjusted date time object
def todaysDate():
    '''
        Get today's server time zone adjusted date time object with zeroed time
    '''
    logger = logging.getLogger(__name__)
    #logger.info("Get todays date object")

    p = Parameters.objects.first()
    tz = pytz.timezone(p.experimentTimeZone)

    d_today = datetime.now(tz)
    d_today = d_today.replace(hour=0,minute=0, second=0,microsecond=0)       
    
    return d_today