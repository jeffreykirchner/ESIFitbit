'''
parameter set model
'''
import math
import logging

from django.db import models
from django.db.utils import IntegrityError
from decimal import Decimal

from main.models import Parameterset
from main.globals import TimeBlock 

import main

#experiment session parameters
class ParametersetTimeBlock(models.Model):
    '''
    parameter set model
    '''

    parameterset = models.ForeignKey(Parameterset, on_delete=models.CASCADE, related_name="time_blocks")

    heart_pay = models.DecimalField(decimal_places=2, default=0.00, max_digits=6)            #heartEarnings $ = block_N_heart_pay * heartActivityToday
    immune_pay = models.DecimalField(decimal_places=2, default=0.00, max_digits=6)           #immuneEarnings $ = block_N_immune_pay * immuneActivityToday
    fixed_pay_per_day = models.DecimalField(decimal_places=2, default=3.00, max_digits=6)    #fixed pay per day $
    day_count = models.IntegerField(default = 1)                                             #number of days for each time block 
    block_number = models.IntegerField(default = 1)                                          #which block from 1 - N this is

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'id:{self.id}, parameterset: {self.parameterset}, block number: {self.block_number}'

    class Meta:
        verbose_name = 'Study Parameter Set Time Block'
        verbose_name_plural = 'Study Parameter Set Time Blocks'

        ordering = ['block_number']

        constraints = [
            models.UniqueConstraint(fields=['block_number', 'parameterset'], name='unique_time_block')
        ]


    def setup_from_dict(self, data):
        '''
        setup up from a file
        '''
        message = "Parameters loaded successfully."

        try:

            self.heart_pay = data.get("heart_pay")
            self.immune_pay = data.get("immune_pay")
            self.day_count = data.get("day_count")
            self.fixed_pay_per_day = data.get("fixed_pay_per_day")
            self.block_number = data.get("block_number")

            self.save()

        except IntegrityError as err:
            message = f"Failed to load parameter set: {err}"
            #logger.info(message)

        return message

    def setup(self, data):
        '''
        copy another parameterset into this one
        '''

        self.heart_pay = data.heart_pay
        self.immune_pay = data.immune_pay
        self.day_count = data.day_count
        self.fixed_pay_per_day = data.fixed_pay_per_day
        self.block_number = data.block_number

        self.save()
    
    def get_time_block_global(self):
        '''
        return the time block global
        '''
        logger = logging.getLogger(__name__)

        logger.info(f"get_time_block_global: {self.block_number}")
        
        if self.block_number == 1:
            return TimeBlock.ONE
        elif self.block_number == 2:
            return TimeBlock.TWO
        elif self.block_number == 3:
            return TimeBlock.THREE
        elif self.block_number == 4:
            return TimeBlock.FOUR
        elif self.block_number == 5:
            return TimeBlock.FIVE
        elif self.block_number == 6:
            return TimeBlock.SIX
        
        return None

    def get_csv_response(self, writer):
        '''
        return csv version
        '''
        writer.writerow([self.block_number, self.heart_pay, self.immune_pay, self.fixed_pay_per_day, self.day_count])


    #return json object of class
    def json(self):
        
        return{

            "id":self.id,

            "heart_pay" : self.heart_pay,
            "immune_pay" : self.immune_pay,
            "day_count" : self.day_count,
            "fixed_pay_per_day" : self.fixed_pay_per_day,
            "block_number" : self.block_number,
        }

