from __future__ import print_function
from __future__ import division
import brickpi3
import grovepi
import time

BP = brickpi3.BrickPi3()
A = BP.PORT_A
B = BP.PORT_B
C = BP.PORT_C
delay_gyro = 4
delay = 0.01
gyro_iterations = 5
sonic_iterations = 5
ultrasonic = 1
grovepi.pinMode(ultrasonic, "INPUT")
directions_free = [0, 0, 0]
distance_ahead = 0

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

EV3_GYRO = BP.PORT_2

def curr_distance():
    sonic_distance = 0
    try:
        for i in range(sonic_iterations):
            sonic_distance = sonic_distance + grovepi.ultrasonicRead(ultrasonic)
            time.sleep(0.02)
        sonic_distance = sonic_distance / sonic_iterations
    except TypeError:
        print("Error")
    except IOError:
        print("Error")
    return sonic_distance


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
    
def checkThreeDirections(directions_free):
    changePos(90)
    directions_free[0] = curr_distance()
    time.sleep(delay)
    changePos(-90)
    directions_free[1] = curr_distance()
    time.sleep(delay)
    changePos(-90)
    directions_free[2] = curr_distance()
    time.sleep(delay)
    changePos(90)
    time.sleep(0.02)
    return(directions_free)


##___MAIN CODE____##
time.sleep(delay_gyro)

try:
    while True:
        while (distance_ahead > 15):
            #Go straight a little
            #Check ultrasonic and do distance_ahead again
        directions_free = [0, 0, 0]
        directions_free = checkThreeDirections(directions_free)
        if (directions_free[0] > 15):
        
        


        #value = get_curr_angle(EV3_GYRO)
        #print(value)
        time.sleep(delay)

except KeyboardInterrupt:
    print("Keyboard Interrupt")
    BP.reset_all()
