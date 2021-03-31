'''
parameter set pay level for treatment B and C
'''

from django.db import models

from main.models import Parameterset

class ParametersetPaylevel(models.Model):
    '''
    parameter set pay level for treatment B and C
    '''

    parameterset = models.ForeignKey(Parameterset, on_delete=models.CASCADE, related_name="paylevels")

    score = models.DecimalField(decimal_places=3, max_digits=5)          #if subject's score is less than or equal to this score pay value
    value = models.DecimalField(decimal_places=2, max_digits=5)          #value in dollars subject earns if score in this range
    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Parameterset pay level'
        verbose_name_plural = 'Parameterset pay levels'
        ordering = ['score']
    
    def json(self):
        return{
            "id" : self.id,
            "score" : self.score,
            "value" : self.value,
        }