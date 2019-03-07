from __future__ import print_function
from __future__ import division

import brickpi3
import time
BP = brickpi3.BrickPi3()
gyro_iterations = 5
delay = 0.01
A = BP.PORT_A


def get_curr_angle(EV3_GYRO):
    angle = [0 , 0]
    for i in range(gyro_iterations):
        sensor_data = BP.get_sensor(EV3_GYRO)
        angle[0] = angle[0] + sensor_data[0]
        angle[1] = angle[1] + sensor_data[1]       
        time.sleep(0.02)
    for j in range(len(angle)):
        angle[j] = angle[j] / gyro_iterations
    angle[0] = angle[0] % 360
    return angle

def changePos(target):
    try:
        BP.offset_motor_encoder(A, BP.get_motor_encoder(A))
    except IOError as error:
        print(error)
    current_pos = BP.get_motor_encoder(A)
    while (current_pos != target):
        direction = (target - current_pos) / abs(target - current_pos)
        print(direction, target - current_pos)
        if (abs(target - current_pos) < 5):
            BP.set_motor_dps(A, -15*direction)
            time.sleep(delay)
        else:
            BP.set_motor_dps(A,100*direction)
            time.sleep(delay)
        current_pos = BP.get_motor_encoder(A)
    print("finished")
    BP.set_motor_dps(A,0)
    
def checkThreeDirections():
    changePos(90)
    time.sleep(delay)
    changePos(-90)
    time.sleep(delay)
    changePos(-90)
    time.sleep(delay)
    changePos(90)
    time.sleep(0.02)


