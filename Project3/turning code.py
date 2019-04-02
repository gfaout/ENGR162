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

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
speed=200				#initial speed
cmd='x'		
rightMotor=PORT_C	# right motor is on PORT_C
leftMotor=PORT_B	# left motor is on PORT_		#last used command (used when increasing or decreasing speed)

#Move Forward
def fwd():
	BrickPi.MotorSpeed[rightMotor] = speed  
	BrickPi.MotorSpeed[leftMotor] = speed  
#Move Left
def left():
	BrickPi.MotorSpeed[rightMotor] = speed  
	BrickPi.MotorSpeed[leftMotor] = -speed
#Move Right
def right():
	BrickPi.MotorSpeed[rightMotor] = -speed  
	BrickPi.MotorSpeed[leftMotor] = speed
#Move backward
def back():
	BrickPi.MotorSpeed[rightMotor] = -speed  
	BrickPi.MotorSpeed[leftMotor] = -speed
#Stop
def stop():
	BrickPi.MotorSpeed[rightMotor] = 0  
	BrickPi.MotorSpeed[leftMotor] = 0


# a = direction input from left/right turning decision module (from ultrasonic code)
# power = set speed

def turning(a, power): #we need gyro, direction input, power
    if a== 0: #this is supposed to go straight
        #call fwd() function
        BP.set_motor_power(BP.PORT_C, power) #right motor
        BP.set_motor_power(BP.PORT_B, power) #left motor
    elif a == -1: #turn left
        #call left() function
        BP.set_motor_power(BP.PORT_C, power) 
        BP.set_motor_power(BP.PORT_B, -power)
    elif a == 1: #turn right
        #call right() function
        BP.set_motor_power(BP.PORT_C, -power) 
        BP.set_motor_power(BP.PORT_B, power)
    else:
        print('error')
        
        
def set_motor_dps(self, port, dps):
        """
        Set the motor target speed in degrees per second
        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        dps -- The target speed in degrees per second
        """
   
        dps = int(dps)
        outArray = [self.SPI_Address, self.BPSPI_MESSAGE_TYPE.SET_MOTOR_DPS, int(port), ((dps >> 8) & 0xFF), (dps & 0xFF)]
        self.spi_transfer_array(outArray)
