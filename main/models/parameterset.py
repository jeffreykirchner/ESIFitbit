from django.db import models
import logging
import traceback
from django.utils.timezone import now

from django.core import serializers

#experiment session parameters
class Parameterset(models.Model):

    #heartActivityToday = heartActivityTodayT-1 * (1 - (1 - heartActivityTodayT-1) * (heart_parameter_1 / heart_parameter_2  - heartTimeT-1 / (heartTimeT-1 + heart_parameter_3))
    heart_activity_inital =  models.DecimalField(decimal_places=10, default=0.6, max_digits=20)
    heart_parameter_1 = models.DecimalField(decimal_places=10, default=0.5, max_digits=20) 
    heart_parameter_2 = models.DecimalField(decimal_places=10, default=3.0, max_digits=20)
    heart_parameter_3 = models.DecimalField(decimal_places=10, default=6.0, max_digits=20)

    #immuneActivityToday = immuneActivityTodayT-1 * (1 - (1 - immuneActivityTodayT-1) * (immune_parameter_1 / immune_parameter_2  - immuneTimeT-1 / (immuneTimeT-1 + immune_parameter_3))
    immune_activity_inital =  models.DecimalField(decimal_places=10, default=0.6, max_digits=20)
    immune_parameter_1 = models.DecimalField(decimal_places=10, default=0.2, max_digits=20) 
    immune_parameter_2 = models.DecimalField(decimal_places=10, default=4.0, max_digits=20)
    immune_parameter_3 = models.DecimalField(decimal_places=10, default=4.0, max_digits=20) 

    #heartEarnings $ = block_N_heart_pay * heartActivityToday
    block_1_heart_pay = models.DecimalField(decimal_places=2, default=0.00, max_digits=6)
    block_2_heart_pay = models.DecimalField(decimal_places=2, default=8.00, max_digits=6)
    block_3_heart_pay = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)

    #immuneEarnings $ = block_N_immune_pay * immuneActivityToday
    block_1_immune_pay = models.DecimalField(decimal_places=2, default=0.00, max_digits=6)
    block_2_immune_pay = models.DecimalField(decimal_places=2, default=8.00, max_digits=6)
    block_3_immune_pay = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)

    #fixed pay per day $
    fixed_pay_per_day = models.DecimalField(decimal_places=2, default=4.00, max_digits=6)

    #number of days for each time block
    block_1_day_count = models.IntegerField(default = 1)
    block_2_day_count = models.IntegerField(default = 1)
    block_3_day_count = models.IntegerField(default = 1)

    #bonus paid to subjects when group target met
    treatment_3_heart_bonus = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)
    treatment_3_immune_bonus = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)
    treatment_3_bonus_target_count = models.IntegerField(default = 1)

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

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = 'Experiment Parameter Set'
        verbose_name_plural = 'Experiment Parameter Sets'

    def get_heart_activity(heart_activity,heart_actvity_minutes):
        return 0
    
    #copy another parameter set into this one
    def setup(self,ps):
        self.save()

        self.heart_activity_inital = ps.heart_activity_inital
        self.heart_parameter_1 = ps.heart_parameter_1
        self.heart_parameter_2 = ps.heart_parameter_2
        self.heart_parameter_3 = ps.heart_parameter_3
        
        self.immune_activity_inital = ps.immune_activity_inital
        self.immune_parameter_1 = ps.immune_parameter_1
        self.immune_parameter_2 = ps.immune_parameter_2
        self.immune_parameter_3 = ps.immune_parameter_3

        self.block_1_heart_pay = ps.block_1_heart_pay
        self.block_2_heart_pay = ps.block_2_heart_pay
        self.block_3_heart_pay = ps.block_3_heart_pay

        self.block_1_immune_pay = ps.block_1_immune_pay
        self.block_2_immune_pay = ps.block_2_immune_pay
        self.block_3_immune_pay = ps.block_3_immune_pay

        self.block_1_day_count = ps.block_1_day_count
        self.block_2_day_count = ps.block_2_day_count
        self.block_3_day_count = ps.block_3_day_count

        self.fixed_pay_per_day = p.fixed_pay_per_day

        self.treatment_3_heart_bonus = ps.treatment_3_heart_bonus
        self.treatment_3_immune_bonus = ps.treatment_3_immune_bonus
        self.treatment_3_bonus_target_count = ps.treatment_3_bonus_target_count

        self.y_min_heart = ps.y_min_heart
        self.y_max_heart = ps.y_max_heart
        self.y_ticks_heart = ps.y_ticks_heart
        self.x_min_heart = ps.x_min_heart
        self.x_max_heart = ps.x_max_heart
        self.x_ticks_heart = ps.x_ticks_heart

        self.y_min_immune = ps.y_min_immune
        self.y_max_immune = ps.y_max_immune
        self.y_ticks_immune = ps.y_ticks_immune
        self.x_min_immune = ps.x_min_immune
        self.x_max_immune = ps.x_max_immune
        self.x_ticks_immune = ps.x_ticks_immune
        
        self.save()

    #return the current maximum payment for heart activty
    def getHeartPay(self,period):

        if period<=self.block_1_day_count:            
            return self.block_1_heart_pay
        elif period<=self.block_2_day_count:
            return self.block_2_heart_pay
        else:
            return self.block_3_heart_pay        

    #return the current maximum payment for heart activty
    def getImmunePay(self,period):
        
        if period<=self.block_1_day_count:            
            return self.block_1_immune_pay
        elif period<=self.block_2_day_count:
            return self.block_2_immune_pay
        else:
            return self.block_3_immune_pay

    #return json object of class
    def json(self):
        return{
            
            "id":self.id,

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

            "fixed_pay_per_day":self.fixed_pay_per_day,

            "treatment_3_heart_bonus":self.treatment_3_heart_bonus,
            "treatment_3_immune_bonus":self.treatment_3_immune_bonus,
            "treatment_3_bonus_target_count":self.treatment_3_bonus_target_count,

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