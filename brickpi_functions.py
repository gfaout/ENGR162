import brickpi3
import time
BP = brickpi3.BrickPi3()
gyro_iterations = 5
   


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


