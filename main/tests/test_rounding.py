'''
tests for rounding
'''
from django.test import TestCase

from main.globals import round_half_away_from_zero


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




            


