'''
parameter set model
'''
import math
import logging
import re

from django.db import models
from django.db.utils import IntegrityError
from decimal import Decimal

import main

#experiment session parameters
class Parameterset(models.Model):
    '''
    parameter set model
    '''
    consent_form = models.ForeignKey('main.Consent_forms',on_delete=models.CASCADE,null=True,blank=True)

    #heartActivityToday = heartActivityTodayT-1 * (1 - (1 - heartActivityTodayT-1) * (heart_parameter_1 / heart_parameter_2  - heartTimeT-1 / (heartTimeT-1 + heart_parameter_3))
    heart_activity_inital =  models.DecimalField(decimal_places=5, default=0.6, max_digits=20)
    heart_parameter_1 = models.DecimalField(decimal_places=5, default=0.5, max_digits=20)
    heart_parameter_2 = models.DecimalField(decimal_places=5, default=3.0, max_digits=20)
    heart_parameter_3 = models.DecimalField(decimal_places=5, default=6.0, max_digits=20)

    #immuneActivityToday = immuneActivityTodayT-1 * (1 - (1 - immuneActivityTodayT-1) * (immune_parameter_1 / immune_parameter_2  - immuneTimeT-1 / (immuneTimeT-1 + immune_parameter_3))
    immune_activity_inital =  models.DecimalField(decimal_places=5, default=0.6, max_digits=20)
    immune_parameter_1 = models.DecimalField(decimal_places=5, default=0.2, max_digits=20)
    immune_parameter_2 = models.DecimalField(decimal_places=5, default=4.0, max_digits=20)
    immune_parameter_3 = models.DecimalField(decimal_places=5, default=4.0, max_digits=20)

    minimum_wrist_minutes = models.IntegerField(default = 1080)

    #heart graph self
    y_min_heart = models.IntegerField(default=0)
    y_max_heart = models.IntegerField(default=100)
    y_ticks_heart = models.IntegerField(default = 10)
    x_min_heart = models.IntegerField(default = 0)
    x_max_heart = models.IntegerField(default = 90)
    x_ticks_heart = models.IntegerField(default = 3)

    #immune graph self
    y_min_immune = models.IntegerField(default=0)
    y_max_immune = models.IntegerField(default=100)
    y_ticks_immune = models.IntegerField(default = 10)
    x_min_immune = models.IntegerField(default = 0)
    x_max_immune = models.IntegerField(default = 12)
    x_ticks_immune = models.IntegerField(default = 6)

    sleep_tracking = models.BooleanField(default=True)  #enable sleep tracking
    show_group = models.BooleanField(default=False)     #show group information
    show_chat = models.BooleanField(default=False)      #show tab information

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Study Parameter Set'
        verbose_name_plural = 'Study Parameter Sets'

    def setup_from_dict(self, data):
        '''
        setup up from a file
        '''
        message = "Parameters loaded successfully."

        # try:

        self.consent_form = main.models.Consent_forms.objects.get(id=data.get("consent_form"))

        self.heart_activity_inital = data.get("heart_activity_inital")
        self.heart_parameter_1 = data.get("heart_parameter_1")
        self.heart_parameter_2 = data.get("heart_parameter_2")
        self.heart_parameter_3 = data.get("heart_parameter_3")

        self.immune_activity_inital = data.get("immune_activity_inital")
        self.immune_parameter_1 = data.get("immune_parameter_1")
        self.immune_parameter_2 = data.get("immune_parameter_2")
        self.immune_parameter_3 = data.get("immune_parameter_3")

        self.minimum_wrist_minutes = data.get("minimum_wrist_minutes")

        self.y_min_heart = data.get("y_min_heart")
        self.y_max_heart = data.get("y_max_heart")
        self.y_ticks_heart = data.get("y_ticks_heart")
        self.x_min_heart = data.get("x_min_heart")
        self.x_max_heart = data.get("x_max_heart")
        self.x_ticks_heart = data.get("x_ticks_heart")

        self.y_min_immune = data.get("y_min_immune")
        self.y_max_immune = data.get("y_max_immune")
        self.y_ticks_immune = data.get("y_ticks_immune")
        self.x_min_immune = data.get("x_min_immune")
        self.x_max_immune = data.get("x_max_immune")
        self.x_ticks_immune = data.get("x_ticks_immune")

        self.sleep_tracking =  data.get("sleep_tracking")
        self.show_group = data.get("show_group")
        self.show_chat = data.get("show_chat")

        # pay levels
        self.paylevels.all().delete()

        paylevel_list = data.get("pay_levels", -1)

        if paylevel_list != -1:
            for paylevel in paylevel_list:
                new_paylevel = main.models.ParametersetPaylevel()

                new_paylevel.parameterset = self
                new_paylevel.score = paylevel["score"]
                new_paylevel.value = paylevel["value"]

                new_paylevel.save()
        
        #time blocks
        self.time_blocks.all().delete()
        time_block_list = data.get("time_blocks", -1)
        if time_block_list != -1:
            for time_block in time_block_list:
                new_time_block = main.models.ParametersetTimeBlock()

                new_time_block.parameterset = self
                new_time_block.setup_from_dict(time_block)

        self.save()

        # except IntegrityError as err:
        #     message = f"Failed to load parameter set: {err}"
        #     #logger.info(message)

        return message

    def setup(self, data):
        '''
        copy another parameterset into this one
        '''
        self.save()

        self.consent_form = data.consent_form

        self.heart_activity_inital = data.heart_activity_inital
        self.heart_parameter_1 = data.heart_parameter_1
        self.heart_parameter_2 = data.heart_parameter_2
        self.heart_parameter_3 = data.heart_parameter_3

        self.immune_activity_inital = data.immune_activity_inital
        self.immune_parameter_1 = data.immune_parameter_1
        self.immune_parameter_2 = data.immune_parameter_2
        self.immune_parameter_3 = data.immune_parameter_3

        self.minimum_wrist_minutes = data.minimum_wrist_minutes

        self.y_min_heart = data.y_min_heart
        self.y_max_heart = data.y_max_heart
        self.y_ticks_heart = data.y_ticks_heart
        self.x_min_heart = data.x_min_heart
        self.x_max_heart = data.x_max_heart
        self.x_ticks_heart = data.x_ticks_heart

        self.y_min_immune = data.y_min_immune
        self.y_max_immune = data.y_max_immune
        self.y_ticks_immune = data.y_ticks_immune
        self.x_min_immune = data.x_min_immune
        self.x_max_immune = data.x_max_immune
        self.x_ticks_immune = data.x_ticks_immune

        self.sleep_tracking = data.sleep_tracking
        self.show_group = data.show_group
        self.show_chat = data.show_chat

        #pay levels
        self.paylevels.all().delete()

        for paylevel in data.paylevels.all():
            new_paylevel = main.models.ParametersetPaylevel()

            new_paylevel.parameterset = self
            new_paylevel.score = paylevel.score
            new_paylevel.value = paylevel.value

            new_paylevel.save()
        
        #time blocks
        self.time_blocks.all().delete()
        for time_block in data.time_blocks.all():
            new_time_block = main.models.ParametersetTimeBlock()

            new_time_block.parameterset = self
            new_time_block.setup(time_block)

        self.save()

    def getHeartPay(self, period):
        '''
        return the maximum heart payment given period
        '''

        b = self.getBlock(period)

        return b.heart_pay if b else None

    def get_total_number_of_periods(self):
        '''
        return the total number of periods
        '''
        if self.time_blocks.all().count() == 0:
            return 0
        
        period_count = 1

        for b in self.time_blocks.all():
            period_count += b.day_count

        return period_count

    #return the current maximum payment for heart activty
    def getImmunePay(self, period):

        if not self.sleep_tracking:
            return 0

        b = self.getBlock(period)

        return b.immune_pay if b else None
    
    def get_fixed_pay(self, period):

        b = self.getBlock(period)

        return b.fixed_pay_per_day if b else None

    def get_treatment_b_c_paylevel(self, score):
        '''
        return the dollar payment
        '''

        if self.paylevels.all().count() == 0:
            return 0

        #check for score out of range
        if score >= 1:
            return self.paylevels.all().last().value
        
        if score <= 0:
            return self.paylevels.all().first().value

        for pay_level in self.paylevels.all():
            if score <= pay_level.score:
                return pay_level.value
        
        return 0

    #get period's time block
    def getBlock(self, period):

        logger = logging.getLogger(__name__)
        #logger.info(f'Get Block for period: {period}')

        period_counter = 1
        block_number = 1

        for b in self.time_blocks.all():
            #logger.info(b)
            if period <= period_counter + b.day_count:
               #logger.info(f'Get Block found: {b}')
               return b
            else:
                period_counter += b.day_count
        
        return None
    
    def get_block_day_count(self, period):
        '''
        get number of days in time block that period falls in
        '''
        b = self.getBlock(period)

        if not b:
            return None
        
        if b.block_number==1:
            return b.day_count+1

        return b.day_count
    
    def get_block_first_period(self, period):
        '''
        return the first period of block that given period falls in
        '''

        b = self.getBlock(period)

        if not b:
            return None

        period_counter = 1
        
        if b.block_number==1:
            return period_counter

        block_list = self.time_blocks.filter(block_number__lt=b.block_number)

        for b in block_list:
            period_counter += b.day_count

        return period_counter + 1
    
    def get_block_last_period(self, period):
        '''
        return the last period of block that given period falls in
        '''
        b = self.getBlock(period)

        if not b:
            return None

        period_counter = 1
        
        block_list = self.time_blocks.filter(block_number__lte=b.block_number)

        for b in block_list:
            period_counter += b.day_count
        
        return period_counter
        
    #return true if block greater 1 starts today
    def getBlockChangeToday(self, period):

        b = self.getBlock(period)

        if not b:
            return None
        
        if b.block_number == 1:
            return 

        if self.get_block_first_period(period) == period:
           return True
        
        return False

    #return true if time block changes in two days
    def getBlockChangeInTwoDays(self, period):

        if self.getBlock(period) == self.time_blocks.all().last():
            return

        if self.get_block_first_period(period+2) == period+2:
           return True
        
        return False

    #return string formated wrist minutes
    def getFormatedWristMinutes(self) -> str:
        v = f'{math.floor(self.minimum_wrist_minutes/60)}hrs'

        if self.minimum_wrist_minutes%60 != 0 :
            v += f' {self.minimum_wrist_minutes%60}mins'

        return v

    #get csv reponse for data file
    def getCSVResponse(self,writer,title,treatment):

        writer.writerow([title,treatment,
                          self.heart_activity_inital,self.heart_parameter_1,self.heart_parameter_2,self.heart_parameter_3,
                          self.immune_activity_inital,self.immune_parameter_1,self.immune_parameter_2,self.immune_parameter_3,
                          self.minimum_wrist_minutes,
                          self.y_min_heart,self.y_max_heart,self.y_ticks_heart,self.x_min_heart,self.x_max_heart,self.x_ticks_heart,
                          self.y_min_immune,self.y_max_immune,self.y_ticks_immune,self.x_min_immune,self.x_max_immune,self.x_ticks_immune,
                          self.sleep_tracking, self.show_group])
    
    def get_csv_response_time_blocks(self, writer):
        '''
        get cvs version fo time blocks
        '''
        for time_block in self.time_blocks.all():
            time_block.get_csv_response(writer)

    def get_csv_response_pay_level(self, writer):
        '''
        get csv version of pay levels
        '''
        start_score = 0
        for pay_level in self.paylevels.all():
            writer.writerow([start_score, pay_level.score,"$" + str(pay_level.value)])
            start_score = pay_level.score + Decimal("0.01")

    def add_time_block(self):
        '''
        add new time block to parameter set
        '''

        time_block = main.models.ParametersetTimeBlock()

        time_block.parameterset = self
        time_block.block_number = self.time_blocks.all().last().block_number + 1 if self.time_blocks.all().last() else 1

        time_block.save()
    
    def remove_time_block(self):
        '''
        remove last time block
        '''

        if self.time_blocks.all().count() <= 1:
            return
        
        self.time_blocks.all().last().delete()

    #return json object of class
    def json(self):
        return{

            "id":self.id,

            "consent_form" : self.consent_form.id if self.consent_form else None,

            "heart_activity_inital":self.heart_activity_inital,
            "heart_parameter_1":self.heart_parameter_1,
            "heart_parameter_2":self.heart_parameter_2,
            "heart_parameter_3":self.heart_parameter_3,

            "immune_activity_inital":self.immune_activity_inital,
            "immune_parameter_1":self.immune_parameter_1,
            "immune_parameter_2":self.immune_parameter_2,
            "immune_parameter_3":self.immune_parameter_3,

            "minimum_wrist_minutes":self.minimum_wrist_minutes,

            "y_min_heart":self.y_min_heart,
            "y_max_heart":self.y_max_heart,
            "y_ticks_heart":self.y_ticks_heart,
            "x_min_heart":self.x_min_heart,
            "x_max_heart":self.x_max_heart,
            "x_ticks_heart":self.x_ticks_heart,

            "y_min_immune":self.y_min_immune,
            "y_max_immune":self.y_max_immune,
            "y_ticks_immune":self.y_ticks_immune,
            "x_min_immune":self.x_min_immune,
            "x_max_immune":self.x_max_immune,
            "x_ticks_immune":self.x_ticks_immune,

            "sleep_tracking":1 if  self.sleep_tracking else 0,
            "show_group":1 if  self.show_group else 0,
            "show_chat":1 if self.show_chat else 0,

            "pay_levels" : [pl.json() for pl in self.paylevels.all()],

            "time_blocks" : [tb.json() for tb in self.time_blocks.all()],
        }

    def json_graph(self):
        return{
            "y_min_heart":float(self.y_min_heart),
            "y_max_heart":float(self.y_max_heart),
            "y_ticks_heart":self.y_ticks_heart,
            "x_min_heart":self.x_min_heart,
            "x_max_heart":self.x_max_heart,
            "x_ticks_heart":self.x_ticks_heart,

            "y_min_immune":float(self.y_min_immune),
            "y_max_immune":float(self.y_max_immune),
            "y_ticks_immune":self.y_ticks_immune,
            "x_min_immune":self.x_min_immune,
            "x_max_immune":self.x_max_immune,
            "x_ticks_immune":self.x_ticks_immune,
        }