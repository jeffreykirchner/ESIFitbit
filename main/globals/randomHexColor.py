import random

#get a random color in hex format
def getRandomHexColor():
   
    return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    