'''
parameter set model
'''
import math
import logging

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

    #heartEarnings $ = block_N_heart_pay * heartActivityToday
    block_1_heart_pay = models.DecimalField(decimal_places=2, default=0.00, max_digits=6)
    block_2_heart_pay = models.DecimalField(decimal_places=2, default=8.00, max_digits=6)
    block_3_heart_pay = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)

    #immuneEarnings $ = block_N_immune_pay * immuneActivityToday
    block_1_immune_pay = models.DecimalField(decimal_places=2, default=0.00, max_digits=6)
    block_2_immune_pay = models.DecimalField(decimal_places=2, default=8.00, max_digits=6)
    block_3_immune_pay = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)

    #fixed pay per day $
    block_1_fixed_pay_per_day = models.DecimalField(decimal_places=2, default=3.00, max_digits=6)
    block_2_fixed_pay_per_day = models.DecimalField(decimal_places=2, default=3.00, max_digits=6)
    block_3_fixed_pay_per_day = models.DecimalField(decimal_places=2, default=3.00, max_digits=6)

    minimum_wrist_minutes = models.IntegerField(default = 1080)

    #number of days for each time block
    block_1_day_count = models.IntegerField(default = 1)
    block_2_day_count = models.IntegerField(default = 1)
    block_3_day_count = models.IntegerField(default = 1)

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

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Study Parameter Set'
        verbose_name_plural = 'Study Parameter Sets'

    # def get_heart_activity(heart_activity, heart_actvity_minutes):
    #     return 0

    def setup_from_dict(self, data):
        '''
        setup up from a file
        '''
        message = "Parameters loaded successfully."

        try:

            self.consent_form = main.models.Consent_forms.objects.get(id=data.get("consent_form"))

            self.heart_activity_inital = data.get("heart_activity_inital")
            self.heart_parameter_1 = data.get("heart_parameter_1")
            self.heart_parameter_2 = data.get("heart_parameter_2")
            self.heart_parameter_3 = data.get("heart_parameter_3")

            self.immune_activity_inital = data.get("immune_activity_inital")
            self.immune_parameter_1 = data.get("immune_parameter_1")
            self.immune_parameter_2 = data.get("immune_parameter_2")
            self.immune_parameter_3 = data.get("immune_parameter_3")

            self.block_1_heart_pay = data.get("block_1_heart_pay")
            self.block_2_heart_pay = data.get("block_2_heart_pay")
            self.block_3_heart_pay = data.get("block_3_heart_pay")

            self.block_1_immune_pay = data.get("block_1_immune_pay")
            self.block_2_immune_pay = data.get("block_2_immune_pay")
            self.block_3_immune_pay = data.get("block_3_immune_pay")

            self.block_1_day_count = data.get("block_1_day_count")
            self.block_2_day_count = data.get("block_2_day_count")
            self.block_3_day_count = data.get("block_3_day_count")

            self.block_1_fixed_pay_per_day = data.get("block_1_fixed_pay_per_day")
            self.block_2_fixed_pay_per_day = data.get("block_2_fixed_pay_per_day")
            self.block_3_fixed_pay_per_day = data.get("block_3_fixed_pay_per_day")

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

            #remove any old pay levels
            self.paylevels.all().delete()

            paylevel_list = data.get("pay_levels", -1)

            if paylevel_list != -1:
                for paylevel in paylevel_list:
                    new_paylevel = main.models.ParametersetPaylevel()

                    new_paylevel.parameterset = self
                    new_paylevel.score = paylevel["score"]
                    new_paylevel.value = paylevel["value"]

                    new_paylevel.save()


            self.save()

        except IntegrityError as err:
            message = f"Failed to load parameter set: {err}"
            #logger.info(message)

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

        self.block_1_heart_pay = data.block_1_heart_pay
        self.block_2_heart_pay = data.block_2_heart_pay
        self.block_3_heart_pay = data.block_3_heart_pay

        self.block_1_immune_pay = data.block_1_immune_pay
        self.block_2_immune_pay = data.block_2_immune_pay
        self.block_3_immune_pay = data.block_3_immune_pay

        self.block_1_day_count = data.block_1_day_count
        self.block_2_day_count = data.block_2_day_count
        self.block_3_day_count = data.block_3_day_count

        self.block_1_fixed_pay_per_day = data.block_1_fixed_pay_per_day
        self.block_2_fixed_pay_per_day = data.block_2_fixed_pay_per_day
        self.block_3_fixed_pay_per_day = data.block_3_fixed_pay_per_day

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

        #remove any old pay levels
        self.paylevels.all().delete()

        for paylevel in data.paylevels.all():
            new_paylevel = main.models.ParametersetPaylevel()

            new_paylevel.parameterset = self
            new_paylevel.score = paylevel.score
            new_paylevel.value = paylevel.value

            new_paylevel.save()


        self.save()

    def getHeartPay(self, period):
        '''
        return the maximum heart payment given period
        '''

        if period<=self.block_1_day_count+1:
            return self.block_1_heart_pay
        elif period<=self.block_2_day_count+self.block_1_day_count+1:
            return self.block_2_heart_pay
        else:
            return self.block_3_heart_pay

    #return the current maximum payment for heart activty
    def getImmunePay(self, period):

        if not self.sleep_tracking:
            return 0

        if period <= self.block_1_day_count + 1:
            return self.block_1_immune_pay
        elif period <= self.block_2_day_count + self.block_1_day_count + 1:
            return self.block_2_immune_pay
        else:
            return self.block_3_immune_pay
    
    def get_fixed_pay(self, period):

        if period <= self.block_1_day_count + 1:
            return self.block_1_fixed_pay_per_day
        elif period <= self.block_2_day_count + self.block_1_day_count + 1:
            return self.block_2_fixed_pay_per_day
        else:
            return self.block_3_fixed_pay_per_day

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
    def getBlock(self,period):
        if period <= self.block_1_day_count + 1:
            return 1
        elif period <= self.block_2_day_count + self.block_1_day_count + 1:
            return 2
        else:
            return 3
    
    def get_block_day_count(self, period):
        '''
        get number of days in time block that period falls in
        '''
        if period <= self.block_1_day_count + 1:
            return self.block_1_day_count + 1
        elif period <= self.block_2_day_count + self.block_1_day_count + 1:
            return self.block_2_day_count
        else:
            return self.block_3_day_count
    
    def get_block_first_period(self, period):
        '''
        return the first period of block that given period falls in
        '''
        if period <= self.block_1_day_count + 1:
            return 1
        elif period <= self.block_2_day_count + self.block_1_day_count + 1:
            return self.block_1_day_count + 2
        else:
            return self.block_1_day_count + self.block_2_day_count + 2
    
    def get_block_last_period(self, period):
        '''
        return the last period of block that given period falls in
        '''
        if period <= self.block_1_day_count + 1:
            return self.block_1_day_count + 1
        elif period <= self.block_2_day_count + self.block_1_day_count + 1:
            return self.block_2_day_count + self.block_1_day_count + 1
        else:
            return self.block_1_day_count + self.block_2_day_count + self.block_3_day_count + 1

    #return true if block 2 or 3 starts today
    def getBlockChangeToday(self,period):

        #start of block 2
        if period == self.block_1_day_count + 1 + 1:
            return True

        #start of block 3
        if period == self.block_2_day_count + self.block_1_day_count + 1 + 1:
            return True
        
        return False

    #return true if time block changes in two days
    def getBlockChangeInTwoDays(self,period):
        
        #check that not last block
        if period + 2 > self.block_1_day_count + self.block_2_day_count + self.block_3_day_count + 1:
            return False

        #check block 2 start
        if period == self.block_1_day_count + 1 - 1:
            return True

        #check block 3 start
        if period == self.block_2_day_count + self.block_1_day_count + 1 - 1:
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
                          self.block_1_heart_pay,self.block_2_heart_pay,self.block_3_heart_pay,
                          self.block_1_immune_pay,self.block_2_immune_pay,self.block_3_immune_pay,
                          self.block_1_day_count,self.block_2_day_count,self.block_3_day_count,
                          self.block_1_fixed_pay_per_day,self.block_2_fixed_pay_per_day, self.block_3_fixed_pay_per_day,
                          self.minimum_wrist_minutes,
                          self.y_min_heart,self.y_max_heart,self.y_ticks_heart,self.x_min_heart,self.x_max_heart,self.x_ticks_heart,
                          self.y_min_immune,self.y_max_immune,self.y_ticks_immune,self.x_min_immune,self.x_max_immune,self.x_ticks_immune,
                          self.sleep_tracking, self.show_group])

    def get_csv_response_pay_level(self, writer):
        '''
        get csv version of pay levels
        '''
        start_score = 0
        for pay_level in self.paylevels.all():
            writer.writerow([start_score, pay_level.score,"$" + str(pay_level.value)])
            start_score = pay_level.score + Decimal("0.01")

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

            "block_1_heart_pay":self.block_1_heart_pay,
            "block_2_heart_pay":self.block_2_heart_pay,
            "block_3_heart_pay":self.block_3_heart_pay,

            "block_1_immune_pay":self.block_1_immune_pay,
            "block_2_immune_pay":self.block_2_immune_pay,
            "block_3_immune_pay":self.block_3_immune_pay,

            "block_1_fixed_pay_per_day":self.block_1_fixed_pay_per_day,
            "block_2_fixed_pay_per_day":self.block_2_fixed_pay_per_day,
            "block_3_fixed_pay_per_day":self.block_3_fixed_pay_per_day,

            "minimum_wrist_minutes":self.minimum_wrist_minutes,

            "block_1_day_count":self.block_1_day_count,
            "block_2_day_count":self.block_2_day_count,
            "block_3_day_count":self.block_3_day_count,

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

            "pay_levels" : [pl.json() for pl in self.paylevels.all()],
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