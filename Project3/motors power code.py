'''
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

try:
    try:
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder B
    except IOError as error:
        print(error)
    
    while True:
        # The following BP.get_motor_encoder function returns the encoder value (what we want to use to control motor C's power).
        try:
            power = BP.get_motor_encoder(BP.PORT_B) / 10
            if power > 100:
                power = 100
            elif power < -100:
                power = -100
        except IOError as error:
            print(error)
            power = 0
        BP.set_motor_power(BP.PORT_C, power)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all() 
'''



from __future__ import print_function 
from __future__ import division

import time 
import brickpi3

BP = brickpi3.BrickPi3()
try:
    try:
         BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) #this might need to be changed to PORT_A
    except IOError as error:
        print(error)
                
    while True:
            try:
                power = BP.get_motor_encoder(BP.PORT_B) / 10 #don't know why we are dividing by 10
                                                             #might need to change to PORT_A
                if power > 100:
                    power = 100
                elif power < -100:
                    power = -100
            except IOError as error:
                print(error)
                power = 0
                    
            BP.set_motor_power(BP.PORT_C, power) #is the PORT_ corresponding to the motor controlled? PORT_A for motor A?
            time.sleep(0.02)    
            
except KeyboardInterrupt:
    BP.reset_all()
    
#change the PORT_ to where we are plugging in 

