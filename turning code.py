'''
Have the wheels go opposite directions to turn the robot. We need to make it
a function so that the gyro can call it.
'''

from __future__ import print_function 
from __future__ import division

import brickpi3

BP = brickpi3.BrickPi3()

def turning(a, power): #we need gyro, direction input, power
    if a== 0: #this is supposed to go straight
        BP.set_motor_power(BP.PORT_A, power)
        BP.set_motor_power(BP.PORT_C, power)
    elif a == -1:
        BP.set_motor_power(BP.PORT_A, -power) #-c is for the motor to go opposite direction 
                                          # c is the variable that will dictate speed??
        BP.set_motor_power(BP.PORT_C, power)
    elif a == 1:
        BP.set_motor_power(BP.PORT_A, power) 
        BP.set_motor_power(BP.PORT_C, -power)
    else:
        print('error')
