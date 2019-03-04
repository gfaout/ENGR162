from __future__ import print_function
from __future__ import division
import brickpi3
import time

import brickpi_functions as brick


BP = brickpi3.BrickPi3()
#EV3_GYRO = BP.PORT_2

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
EV3_GYRO = BP.PORT_2
time.sleep(4)
try:
    while (True):
        try:
            for i in range(4):
                angle = brick.get_curr_angle(EV3_GYRO)                
                print(angle)
                time.sleep(0.5)
            print("New Cycle")
        except brickpi3.SensorError as error:
            print(error)

except KeyboardInterrupt:
    print("Ending")
    time.sleep(0.5)
    print("Now Ending")
    BP.reset_all()
