from django.db import models
import logging
import traceback
from django.utils.timezone import now

#experiment session parameters
class Parameterset(models.Model):
    number_of_days = models.IntegerField(default = 1)  
    number_of_players = models.IntegerField(default = 1) 

    #heartActivityToday = heartActivityTodayT-1 * (1 - (1 - heartActivityTodayT-1) * (heart_parameter_1 / heart_parameter_2  - heartTimeT-1 / (heartTimeT-1 + heart_parameter_3))
    heart_activity_inital =  models.DecimalField(decimal_places=10, default=1, max_digits=20)
    heart_parameter_1 = models.DecimalField(decimal_places=10, default=1, max_digits=20) 
    heart_parameter_2 = models.DecimalField(decimal_places=10, default=3, max_digits=20)
    heart_parameter_3 = models.DecimalField(decimal_places=10, default=60, max_digits=20)

    #immuneActivityToday = immuneActivityTodayT-1 * (1 - (1 - immuneActivityTodayT-1) * (immune_parameter_1 / immune_parameter_2  - immuneTimeT-1 / (immuneTimeT-1 + immune_parameter_3))
    immune_activity_inital =  models.DecimalField(decimal_places=10, default=1, max_digits=20)
    immune_parameter_1 = models.DecimalField(decimal_places=10, default=1, max_digits=20) 
    immune_parameter_2 = models.DecimalField(decimal_places=10, default=3, max_digits=20)
    immune_parameter_3 = models.DecimalField(decimal_places=10, default=60, max_digits=20) 

    #todaysEarnings = treatmentPay * (heartActivityToday + immuneEarningsToday)
    treatment_pay_1 = models.DecimalField(decimal_places=2, default=4.00, max_digits=6)
    treatment_pay_2 = models.DecimalField(decimal_places=2, default=8.00, max_digits=6)
    treatment_pay_3 = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)

    #bonus paid to subjects when group target met
    treatment_3_heart_bonus = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)
    treatment_3_immune_bonus = models.DecimalField(decimal_places=2, default=16.00, max_digits=6)
    treatment_3_bonus_target_count = models.IntegerField(default = 1)

    #number of days for each treatment
    treatment_1_day_count = models.IntegerField(default = 1)
    treatment_2_day_count = models.IntegerField(default = 1)
    treatment_3_day_count = models.IntegerField(default = 1)

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Experiment Parameter Set'
        verbose_name_plural = 'Experiment Parameter Sets'

    def get_heart_activity(heart_activity,heart_actvity_minutes):
        return 

    #return json object of class
    def json(self):
        return{
            "id":self.id,
            "name":self.number_of_days,
            "name":self.start_date,
        }