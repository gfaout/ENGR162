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
        
def set_motor_limits(self, port, power = 0, dps = 0):
        """
        Set the motor speed limit
        Keyword arguments:
        port -- The motor port(s). PORT_A, PORT_B, PORT_C, and/or PORT_D.
        power -- The power limit in percent (0 to 100), with 0 being no limit (100)
        dps -- The speed limit in degrees per second, with 0 being no limit
        """
       
        dps = int(dps)
        outArray = [self.SPI_Address, self.BPSPI_MESSAGE_TYPE.SET_MOTOR_LIMITS, int(port), int(power), ((dps >> 8) & 0xFF), (dps & 0xFF)]
        self.spi_transfer_array(outArray)