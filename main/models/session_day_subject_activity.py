'''
subject's daily activity
'''
from datetime import datetime, timedelta

import pytz
import uuid
import main
import math
import logging
import traceback
from enum import Enum

from django.db import models
from django.utils.timezone import now

from . import Session_day,Session_subject,Parameters

from main.globals import round_half_away_from_zero, calc_maintenance, calc_activity

class Session_day_subject_actvity(models.Model):
    '''
    subject's daily activity
    '''
    session_day = models.ForeignKey(Session_day, on_delete=models.CASCADE, related_name="Session_day_subject_actvities_SD")
    session_subject = models.ForeignKey(Session_subject, on_delete=models.CASCADE, related_name="Session_day_subject_actvities")

    heart_activity_minutes = models.IntegerField(default=0)       #todays heart activity minutes
    immune_activity_minutes = models.IntegerField(default=0)      #todays immune activity minutes

    heart_activity = models.DecimalField(decimal_places=2, default=0, max_digits=10)               #todays heart activity calculation
    immune_activity = models.DecimalField(decimal_places=2, default=0, max_digits=10)              #todays immune activity calculation
    
    check_in_today = models.BooleanField(default=False)                                             #true if the user checked in today
    paypal_today = models.BooleanField(default=False)                                               #true if the user collected their payment today

    payment_today =  models.DecimalField(decimal_places=2, default=0, max_digits=6)                 #amount of money paid to subject today

    #fitbit metrics
    fitbit_minutes_sedentary = models.IntegerField(default=0)         #todays tracker sedentary minutes
    fitbit_minutes_lightly_active = models.IntegerField(default=0)    #todays tracker lightly active minutes
    fitbit_minutes_fairly_active = models.IntegerField(default=0)     #todays tracker fairly active minutes
    fitbit_minutes_very_active = models.IntegerField(default=0)       #todays tracker very active minutes
    fitbit_steps = models.IntegerField(default=0)                     #todays tracker steps
    fitbit_calories = models.IntegerField(default=0)                  #todays tracker calories
    fitbit_minutes_heart_out_of_range = models.IntegerField(default=0)         #todays heart rate out of range
    fitbit_minutes_heart_fat_burn = models.IntegerField(default=0)             #todays heart rate lightly fat burn
    fitbit_minutes_heart_cardio = models.IntegerField(default=0)               #todays heart rate cardio
    fitbit_minutes_heart_peak = models.IntegerField(default=0)                 #todays heart rate peak
    fitbit_heart_time_series =  models.CharField(max_length = 100000, default = '')  #today's heart rate time series
    fitbit_immune_time_series =  models.CharField(max_length = 100000, default = '')  #today's sleep time series

    fitbit_on_wrist_minutes = models.IntegerField(default=0)         #minutes fit bit was one wrist (sum of heart time series) 
    fitbit_min_heart_rate_zone_bpm = models.IntegerField(default=0)  #minimum bmp a subject must have to register active zone minutes

    last_login = models.DateTimeField(null=True,blank=True)          #first time the subject logged in this day 

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return "Period " + str(self.session_day.period_number) + " Subject " + self.session_subject.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session_day', 'session_subject'], name='unique_SDSA')
        ]
        verbose_name = 'Session Day'
        verbose_name_plural = 'Session Days'

    #calc heart activity
    def calcHeartActivity(self,heart_time,activity_score,round_result):
        logger = logging.getLogger(__name__)

        p_set = self.session_day.session.parameterset

        return calc_activity(heart_time/15,
                            p_set.heart_parameter_1,
                            p_set.heart_parameter_2,
                            p_set.heart_parameter_3,
                            activity_score,
                            round_result)

    #save heart activity    
    def saveHeartActivity(self,heart_time,heartActivityMinus1):
        self.heart_activity = self.calcHeartActivity(heart_time,heartActivityMinus1,True)
        self.save()

    #calc immune activity
    def calcImmuneActivity(self,immune_time,activity_score,round_result):
        p_set = self.session_day.session.parameterset

        return calc_activity(immune_time/240,
                            p_set.immune_parameter_1,
                            p_set.immune_parameter_2,
                            p_set.immune_parameter_3,
                            activity_score,
                            round_result)

    #save immune activity    
    def saveImmuneActivity(self,immune_time,immuneActivityMinus1):
        self.immune_activity = self.calcImmuneActivity(immune_time,immuneActivityMinus1,True)
        self.save()
    
    #get number of minutes for heart maintenance
    def getHeartMaintenance(self):
        logger = logging.getLogger(__name__)

        p_set = self.session_day.session.parameterset

        return calc_maintenance(p_set.heart_parameter_1,
                               p_set.heart_parameter_2,
                               p_set.heart_parameter_3,
                               self.heart_activity,
                               self.heart_activity,
                               15)

    #get number of minutes for heart maintenance
    def getImmuneMaintenance(self):
        logger = logging.getLogger(__name__) 

        p_set = self.session_day.session.parameterset

        return calc_maintenance(p_set.immune_parameter_1,
                               p_set.immune_parameter_2,
                               p_set.immune_parameter_3,
                               self.immune_activity,
                               self.immune_activity,
                               240)

    def heart_activity_formatted(self):
        '''
        format heart score according to treamtnet
        '''
        if self.session_day.session.treatment == "I":
            v = int(self.heart_activity * 100)
            return f'{v}'
        
        return f'{self.heart_activity:0.2f}'

    def immune_activity_formatted(self):
        '''
        format sleep score according to treatment
        '''
        if self.session_day.session.treatment == "I":
            v = int(self.immune_activity * 100)
            return f'{v}'
    
        return f'{self.immune_activity:0.2f}'

    #return the activity day before this one
    def getPreviousActivityDay(self):
        logger = logging.getLogger(__name__)

        if self.session_day.period_number == 1:
            return None
        
        try:
            return main.models.Session_day_subject_actvity.objects.get(session_subject = self.session_subject,
                                                                       session_day__period_number = self.session_day.period_number-1)
        except Exception  as e: 
            logger.warning(e)
            return None
    
    def getHeartActivityFutureRange(self):
        '''
        return range of possible scores for subject's heart graph
        '''
        logger = logging.getLogger(__name__)
        v = []

        ps = self.session_day.session.parameterset

        value_step = (ps.x_max_heart - ps.x_min_heart) / 100
        current_value = ps.x_min_heart

        logger.info(f'getHeartActivityFutureRange {self.heart_activity} {self.id} {self.session_day.period_number}')

        multiplier = 1

        if self.session_day.session.treatment == "I":
            multiplier = 100

        for i in range(99):
            v.append({"x":current_value, "y": self.calcHeartActivity(current_value,self.heart_activity,False) * multiplier})
            current_value += value_step

        return v

    def getImmuneActivityFutureRange(self):
        '''
        return the range of possible scores for subject's sleep graph
        '''
        v = []

        ps = self.session_day.session.parameterset

        value_step = (ps.x_max_immune * 60 - ps.x_min_immune * 60) / 100
        current_value = ps.x_min_immune * 60

        multiplier = 1

        if self.session_day.session.treatment == "I":
            multiplier = 100

        for i in range(99):
            v.append({"x":current_value, "y": self.calcImmuneActivity(current_value,self.immune_activity,False) * multiplier})
            current_value += value_step

        return v

    #get heart payment for today
    def getTodaysHeartEarnings(self):
        return self.heart_activity * self.session_day.getCurrentHeartPay()
    
    #get immune payment for today
    def getTodaysImmuneEarnings(self):
        return self.immune_activity * self.session_day.getCurrentImmunePay()
    
    #get today's total earnings
    def getTodaysTotalEarnings(self):
        return self.session_day.session.parameterset.get_fixed_pay(self.session_day.period_number) + \
               self.getTodaysHeartEarnings() + \
               self.getTodaysImmuneEarnings()

    #save today's total earnings
    def storeTodaysTotalEarnings(self):
        self.payment_today = self.getTodaysTotalEarnings()
        self.save()

    def calc_a_b_c_block_payments(self):
        '''
        calc block payment for treatments A B C
        '''

        logger = logging.getLogger(__name__)
        
        period_number = self.session_day.period_number

        start_period = self.session_day.session.parameterset.get_block_first_period(period_number)
        end_period = self.session_day.session.parameterset.get_block_last_period(period_number)
        block_length = self.session_day.session.parameterset.get_block_day_count(period_number)
        
        session_day = self.session_day

        #check if today is last period
        if period_number != end_period:
            logger.warning(f'calc_a_b_c_block_payments not last period {self}, end period {end_period}')
            return 0

        missed_days = self.session_subject.get_missed_checkins(period_number)
        daily_payment = self.session_subject.get_daily_payment_A_B_C(period_number)
        self.payment_today = round_half_away_from_zero((block_length - missed_days) * daily_payment, 2)
        self.save() 

        logger.info(f'calc_a_b_c_block_payments payment {self.payment_today}, block length {block_length}, missed days {missed_days}, daily payment {daily_payment}')

        return float(self.payment_today)

    #get health improvment minutes
    def getTodaysHeartImprovmentMinutes(self):
        logger = logging.getLogger(__name__)

        #check that not maxed out
        if self.heart_activity >= 1.0 :
            logger.info('getTodaysHeartImprovmentMinutes already at max')
            return {"target_activity": '--',"target_minutes": '--',"target_bpm":'--'}

        p_set = self.session_day.session.parameterset

        max_activity = self.calcHeartActivity(1440, self.heart_activity, True)

        target_activity = (float(self.heart_activity) + max_activity) / 2

        target_activity = round_half_away_from_zero(target_activity, 2)

        target_minutes = calc_maintenance(p_set.heart_parameter_1,
                                         p_set.heart_parameter_2,
                                         p_set.heart_parameter_3,
                                         self.heart_activity,
                                         target_activity,                                   
                                         15)

        logger.info(f'getTodaysHeartImprovmentMinutes heart_activity {self.heart_activity} max_activity {max_activity} target_activity {target_activity} target_minutes {target_minutes}')

        target_minutes = math.ceil(target_minutes)

        if self.session_day.session.treatment == "I":
            target_activity = int(target_activity*100)
        else:
            target_activity = f'{target_activity:0.2f}'
        
        return {"target_activity": f'{target_activity}',"target_minutes":f' {target_minutes}mins',"target_bpm":f'{self.fitbit_min_heart_rate_zone_bpm}bpm'}

    #get immune improvment minutes
    def getTodaysImmuneImprovmentHours(self):
        logger = logging.getLogger(__name__)
        p_set = self.session_day.session.parameterset

        #check that not maxed out
        if self.immune_activity >= 1.0:
            logger.info('getTodaysHeartImprovmentMinutes already at max')
            return {"target_activity": '--',"target_hours": '--'}

        max_activity = self.calcImmuneActivity(1440,self.immune_activity,True)

        target_activity = (float(self.immune_activity) + max_activity)/2

        target_activity = round_half_away_from_zero(target_activity, 2)

        target_minutes = calc_maintenance(p_set.immune_parameter_1,
                                         p_set.immune_parameter_2,
                                         p_set.immune_parameter_3,
                                         self.immune_activity,
                                         target_activity,
                                         240)

        logger.info(f'getTodaysimmuneImprovmentMinutes immune_activity {self.immune_activity} max_activity {max_activity} target_activity {target_activity} target_minutes {target_minutes}')

        target_minutes = math.ceil(target_minutes)

        if self.session_day.session.treatment == "I":
            target_activity = int(target_activity*100)
        else:
            target_activity = f'{target_activity:0.2f}'

        return {"target_activity": f'{target_activity}',"target_hours":f'{math.floor(target_minutes/60)}hrs {target_minutes%60}mins'}

    #pull heart rate data
    def pullFibitBitHeartRate(self,calc_active_minutes):
        logger = logging.getLogger(__name__)
        fitbitError = False

        #heart rate
        try:
            heart_full = self.session_subject.getFitbitHeartRate(self.session_day.date) 
            #logger.info(f'pullFitbitActvities {temp_h}')    ]
        
            heart_summary = heart_full['activities-heart'][0]['value']['heartRateZones']

            #store heart rate ranges
            for i in range(4):
            
                minutes = heart_summary[i].get("minutes",0)
                name =  heart_summary[i].get("name","not found")

                logger.info(f'pullFibitBitHeartRate {name} {minutes}')

                if name == 'Out of Range':
                    self.fitbit_minutes_heart_out_of_range = minutes
                elif name == 'Fat Burn':
                    self.fitbit_minutes_heart_fat_burn = minutes
                    self.fitbit_min_heart_rate_zone_bpm =  heart_summary[i].get("min",0)
                elif name == 'Cardio':
                    self.fitbit_minutes_heart_cardio = minutes
                elif name == 'Peak':
                    self.fitbit_minutes_heart_peak = minutes

            self.fitbit_heart_time_series = heart_full
            self.save()

            #store minutes on wrist
            #v = eval(str(heart_full))
            v = heart_full.get("activities-heart-intraday",-1)

            if v == -1:
                self.fitbit_on_wrist_minutes = 0
            
            v = v.get('dataset',-1)
            if v==-1:
                self.fitbit_on_wrist_minutes = 0
            else:
                self.fitbit_on_wrist_minutes = len(v)

                #active zone minutes, new calculation
                if calc_active_minutes:
                    self.heart_activity_minutes = self.fitbit_minutes_heart_cardio * 2 + \
                                                  self.fitbit_minutes_heart_peak * 2 + \
                                                  self.fitbit_minutes_heart_fat_burn

            self.save()
       
        except Exception  as e:
            logger.warning(f'Error pullFibitBitHeartRate {e}')
            fitbitError = True

        return fitbitError

    #pull actvities from fitbit and store
    def pullFitbitActvities(self):
        logger = logging.getLogger(__name__)

        fitbitError = False

        self.fitbit_immune_time_series = self.session_subject.getFitbitSleep(self.session_day.date)
        immune_activity_minutes = self.session_subject.getFibitImmuneMinutes(self.session_day.date)

        if immune_activity_minutes !=-1:
            #activites
            self.fitbit_minutes_sedentary = self.session_subject.getFibitActivityMinutes(self.session_day.date,"minutesSedentary")
            self.fitbit_minutes_lightly_active = self.session_subject.getFibitActivityMinutes(self.session_day.date,"minutesLightlyActive")
            self.fitbit_minutes_fairly_active = self.session_subject.getFibitActivityMinutes(self.session_day.date,"minutesFairlyActive")
            self.fitbit_minutes_very_active = self.session_subject.getFibitActivityMinutes(self.session_day.date,"minutesVeryActive")
            self.fitbit_steps = self.session_subject.getFibitActivityMinutes(self.session_day.date,"steps")
            self.fitbit_calories = self.session_subject.getFibitActivityMinutes(self.session_day.date,"calories")

        self.save()

        #old active minutes calculation
        heart_activity_minutes =  self.fitbit_minutes_fairly_active +  self.fitbit_minutes_very_active

        if immune_activity_minutes >= 0:
            self.immune_activity_minutes = immune_activity_minutes
        else:
            logger.warning(f"immune_activity_minutes not found: session subject {self.session_subject} session day {self.session_day}")
            fitbitError=True
        
        #old calculation
        #self.heart_activity_minutes = heart_activity_minutes

        if heart_activity_minutes < 0:
            logger.warning(f"heart_activity_minutes not found: session subject {self.session_subject} session day {self.session_day}")
            fitbitError=True

        self.save()

        return fitbitError

    #update the last login time
    def updateLast_login(self):
        if not self.last_login:

            self.last_login = datetime.now(pytz.UTC)
            self.save()

    #return string formated wrist minutes
    def getFormatedWristMinutes(self) -> str:
        m = self.fitbit_on_wrist_minutes

        v = f'{math.floor(m/60)}hrs'

        if m % 60 != 0 :
            v += f' {m%60}mins'

        return v
    
    #return CSV response for data download
    def getCSVResponse(self,writer):
        p = Parameters.objects.first()
        tz = pytz.timezone(p.experimentTimeZone)
        last_login_str = "No login" if not self.last_login else self.last_login.astimezone(tz).strftime("%#m/%#d/%Y %H:%M:%S %Z")
        # ["Session","Period","Block","Date","Subject ID", "Subject Code","Heart Activity Minutes",
        #                  "Immune Activity Minutes","Heart Activity Score","Immune Activity Score",
        #                  "Check In Today", "Paid Today","Fixed Payment","Heart Payment","Immune Payment","Total Payment Today"]
        
        heart_earnings = self.getTodaysHeartEarnings()
        sleep_earnings = self.getTodaysImmuneEarnings()

        writer.writerow([f'{self.session_day.session.title}', self.session_day.period_number, self.session_day.session.parameterset.getBlock(self.session_day.period_number),
                         self.session_day.getDateStr(),self.session_subject.id_number, self.session_subject.contact_email, self.heart_activity_minutes,
                         self.immune_activity_minutes,self.heart_activity, self.immune_activity, self.check_in_today,
                         self.paypal_today, self.session_day.session.parameterset.get_fixed_pay(self.session_day.period_number), heart_earnings,
                         sleep_earnings, self.payment_today, self.fitbit_minutes_sedentary, self.fitbit_minutes_lightly_active,
                         self.fitbit_minutes_fairly_active, self.fitbit_minutes_very_active, self.fitbit_steps, self.fitbit_calories,
                         self.fitbit_minutes_heart_out_of_range, self.fitbit_minutes_heart_fat_burn, self.fitbit_minutes_heart_cardio,
                         self.fitbit_minutes_heart_peak, self.fitbit_min_heart_rate_zone_bpm, self.fitbit_on_wrist_minutes, last_login_str])
    
    def getCSVResponseABC(self,writer):
        p = Parameters.objects.first()
        tz = pytz.timezone(p.experimentTimeZone)
        last_login_str = "No login" if not self.last_login else self.last_login.astimezone(tz).strftime("%#m/%#d/%Y %H:%M:%S %Z")
        # ["Session","Period","Block","Date","Subject ID", "Subject Code","Heart Activity Minutes",
        #                  "Immune Activity Minutes","Heart Activity Score","Immune Activity Score",
        #                  "Check In Today", "Paid Today","Fixed Payment","Heart Payment","Immune Payment","Total Payment Today"]
        
        period_number = self.session_day.period_number
        treatment =  self.session_subject.session.treatment

        missed_days = self.session_subject.get_missed_checkins(period_number)

        heart_average = self.session_subject.get_average_heart_score(period_number)

        if treatment == "A":
            heart_paylevel = self.session_subject.session.parameterset.getHeartPay(period_number)
        else:
            heart_paylevel = self.session_subject.session.parameterset.get_treatment_b_c_paylevel(heart_average)
        
        sleep_average = self.session_subject.get_average_sleep_score(period_number)

        if treatment == "A":
            sleep_paylevel = self.session_subject.session.parameterset.getImmunePay(period_number)
        else:
            sleep_paylevel = self.session_subject.session.parameterset.get_treatment_b_c_paylevel(sleep_average)

        writer.writerow([f'{self.session_day.session.title}',period_number , self.session_day.session.parameterset.getBlock(period_number),
                         self.session_day.getDateStr(),self.session_subject.id_number, self.session_subject.contact_email, self.heart_activity_minutes,
                         self.immune_activity_minutes,self.heart_activity, self.immune_activity, self.check_in_today,
                         self.paypal_today, missed_days, self.session_day.session.parameterset.get_fixed_pay(period_number), heart_average, heart_paylevel,
                         sleep_average, sleep_paylevel, self.payment_today, self.fitbit_minutes_sedentary, self.fitbit_minutes_lightly_active,
                         self.fitbit_minutes_fairly_active, self.fitbit_minutes_very_active, self.fitbit_steps, self.fitbit_calories,
                         self.fitbit_minutes_heart_out_of_range, self.fitbit_minutes_heart_fat_burn, self.fitbit_minutes_heart_cardio,
                         self.fitbit_minutes_heart_peak, self.fitbit_min_heart_rate_zone_bpm, self.fitbit_on_wrist_minutes, last_login_str])

    #return json object of class
    def json(self):
        immune_activity_minutes=int(self.immune_activity_minutes)
        immune_activity_hours = f'{math.floor(immune_activity_minutes/60)}hrs {immune_activity_minutes%60}mins'

        immune_maintenance_minutes = math.ceil(self.getImmuneMaintenance())
        immune_maintenance_hours = f'{math.floor(immune_maintenance_minutes/60)}hrs {immune_maintenance_minutes%60}mins'

        return{
            "id":self.id,             
            "heart_activity":self.heart_activity_formatted(),     
            "immune_activity":self.immune_activity_formatted(),
            "heart_activity_minutes":f'{int(self.heart_activity_minutes)}mins',     
            "immune_activity_hours":immune_activity_hours,
            "check_in_today":self.check_in_today,     
            "paypal_today":self.paypal_today,
            "heart_activity_future":self.getHeartActivityFutureRange(),
            "immune_activity_future":self.getImmuneActivityFutureRange(),
            "current_heart_pay":f'{self.session_day.get_current_heart_pay_display():0.2f}',
            "current_immune_pay":f'{self.session_day.get_current_immune_pay_display():0.2f}',
            "current_heart_earnings":f'{self.getTodaysHeartEarnings():0.2f}',
            "current_immune_earnings":f'{self.getTodaysImmuneEarnings():0.2f}',
            "current_total_earnings":f'{self.getTodaysTotalEarnings():0.2f}',
            "fixed_pay_per_day" : f'{self.session_day.session.parameterset.get_fixed_pay(self.session_day.period_number):0.2f}',
            "heart_maintenance_minutes" : f'{math.ceil(self.getHeartMaintenance())}mins',
            "immune_maintenance_hours" : immune_maintenance_hours,
            "heart_improvment_minutes" : self.getTodaysHeartImprovmentMinutes(),
            "immune_improvment_hours":self.getTodaysImmuneImprovmentHours(),
            "time_on_wrist":self.getFormatedWristMinutes(),
        }