'''
calculate activity levels and minutes
'''
import logging
from main.globals import round_half_away_from_zero

#calc activity
def calc_activity(active_time, a, b, c, activity_score, round_result): 
    '''
    calc activity minutes given number of active minutes
    '''
    logger = logging.getLogger(__name__)
    #immuneActivityTodayT-1 * (1 - (1 - immuneActivityTodayT-1) * (immune_parameter_1 / immune_parameter_2  - immuneTimeT-1 / (immuneTimeT-1 + immune_parameter_3))

    #logger.info(f'{active_time} {p1} {p2} {p3} {activityMinus1}')
    #v = float(activityMinus1) * (1 - (1 - float(activityMinus1)) * (float(p1) / float(p2)  - float(active_time) / (float(active_time) + float(p3))))

    a=float(a)
    b=float(b)
    c=float(c)

    active_time = float(active_time)
    activity_score = min(0.99, float(activity_score))

    #debug code
    #active_time=111

    v = a * activity_score + 0.5 * (1 + activity_score) * (1 - a * activity_score) * (active_time**b / (c + active_time**b))

    if v < 0:
        v = 0

    if round_result:
        v = round_half_away_from_zero(v, 2)

    return min(0.99, v)   

#calc minutes required to maintain target actvitity level
def calc_maintenance(a, b, c, y, z, n):
    '''
    calc maintenance minutes need to go from level y to level z
    '''
    logger = logging.getLogger(__name__)

    a = float(a)
    b = float(b)
    c = float(c)
    y = min(0.99,float(y))
    z = min(0.99,float(z))
    n = float(n)


    #v = 2**(1/b) * e * ((a * c * d - c * d)/(a**2 * d**2 - 2 * a * d + 2 * d - 1))**(1/b)
    # x = 2^(1/b) n ((a c y - c z)/(a y^2 - a y - y + 2 z - 1))^(1/b)

    #v = 2.0**(1 / float(b)) * float(e) * ((float(a) * float(c) * float(d) - float(c) * float(d))/((float(d) - 1.0) * (float(a) * float(d) + 1.0)))**(1.0/float(b))
    try:
        v = 2.0**(1/b) * n * ((a * c * y - c * z)/(a * y**2 - a * y - y + 2 * z - 1))**(1/b)
    except ZeroDivisionError:
        v = 0
        logger.warning(f"calc_maintenance divide by zero: a {a}, b {b}, c {c}, y {y}, z {z}, n {n}")

    v=abs(v)

    logger.info(f"calc_maintenance {v}, a {a}, b {b}, c {c}, y {y}, z {z}, n {n}")

    return v 