'''
Have the wheels go opposite directions to turn the robot. We need to make it
a function so that the gyro can call it.
RIGHT MOTOR: PORT C
LEFT MOTOR: PORT B
'''

from __future__ import print_function 
from __future__ import division

import brickpi3

BP = brickpi3.BrickPi3()

# a = direction input from left/right turning decision module (from ultrasonic code)
# power = set speed

def turning(a, power): #we need gyro, direction input, power
    if a== 0: #this is supposed to go straight
        BP.set_motor_power(BP.PORT_C, power) #right motor
        BP.set_motor_power(BP.PORT_B, power) #left motor
    elif a == -1: #turn left
        BP.set_motor_power(BP.PORT_C, power) 
        BP.set_motor_power(BP.PORT_B, -power)
    elif a == 1: #turn right
        BP.set_motor_power(BP.PORT_C, -power) 
        BP.set_motor_power(BP.PORT_B, power)
    else:
        print('error')
