'''
tests for rounding
'''
from django.test import TestCase

from main.globals import round_half_away_from_zero, calc_activity, calc_maintenance


#test past last day of experiment
class TestRounding(TestCase):
    '''
    tests for rounding
    '''

    def setUp(self):
       pass

    def test_rounding(self):
        '''test round away from zero '''

        self.assertEqual(1.6, round_half_away_from_zero(1.55,1))
        self.assertEqual(1.7, round_half_away_from_zero(1.66,1))
        self.assertEqual(1.7, round_half_away_from_zero(1.650,1))
        self.assertEqual(1.6, round_half_away_from_zero(1.61,1))

        self.assertEqual(1.61, round_half_away_from_zero(1.611,2))
        self.assertEqual(1.67, round_half_away_from_zero(1.665,2))
        self.assertEqual(1.65, round_half_away_from_zero(1.651,2))
        self.assertEqual(1.67, round_half_away_from_zero(1.666,2))

        self.assertEqual(21.67, round_half_away_from_zero(21.666,2))
        self.assertEqual(22.00, round_half_away_from_zero(21.995,2))

class TestCalcMaintenance(TestCase):
    '''
    test maintainence minutes calculations
    '''
    def setUp(self):
       pass
    
    def test_calc_maintenance(self):
        '''
        test the maintainence calculations
        '''
        #wolfram alpha
        #solve y = a * x + 0.5 * (1 + x) * (1 - a * x) * ((z/n)^b / (c + (z/n)^b)), a=0.6, b=3, c=6, x=0.6, z=30, n=15

        self.assertEqual(0.65, calc_activity(30/15, 0.6, 3, 6, 0.6, True))
        self.assertEqual(0.99, calc_activity(300/15, 0.6, 3, 6, 1, True))
        self.assertEqual(0.5, calc_activity(0/15, 0.5, 3, 6, 0.99, True))

        self.assertEqual(0.89, calc_activity(480/240, 0.2, 4, 2.5, 1, True))
        self.assertEqual(0.73, calc_activity(480/240, 0.2, 4, 2.5, 0.6, True))

        



            


