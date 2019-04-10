from __future__ import print_function
from __future__ import division
import brickpi3
import grovepi
import time

#### Import statements, constants settings, and grovepi setup ####
BP = brickpi3.BrickPi3()
A = BP.PORT_A
B = BP.PORT_B  # Left wheel   # positive moves wheel backward & negative forward
C = BP.PORT_C  # Right wheel
EV3_GYRO = BP.PORT_2
EV3_Ultra = BP.PORT_3
delay_brickpi = 4
delay = 0.03
gyro_iterations = 5
sonic_iterations = 5
ultrasonic_left = 1
ultrasonic_right = 2
grovepi.pinMode(ultrasonic_left, "INPUT")
grovepi.pinMode(ultrasonic_right, "INPUT")
all_direction_distance = [0, 0, 0]
map = [[5]] #1 indicates path, 0 indicates not part of path, 5 is start, 2 is heat, 3 is magnet, 4 is end

####_________________________________________________________####

#### Brickpi Sensor Setup ####
BP.set_sensor_type(EV3_GYRO, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
BP.set_sensor_type(EV3_Ultra, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM) 
####________#####

"""
 while (angle <  abs(degree_to_reach)):
        if (degree_to_reach > 0):
            BP.set_motor_dps(B, 30)
            BP.set_motor_dps(C, -30)
            time.delay(delay)
            BP.set_motor_dps(B, 0)
            BP.set_motor_dps(C, 0)
        else:
            BP.set_motor_dps(B, -30)
            BP.set_motor_dps(C, 30)
            time.delay(delay)
            BP.set_motor_dps(B, 0)
            BP.set_motor_dps(C, 0)
        angle = getCurrAngle(EV3_GYRO)
"""
def turn(degrees_to_turn):  # positive is to the right, negative is to the left
    #Assume degrees_to_turn is below 361 and above -361
    start_angle = getCurrAngle(EV3_GYRO)[0]
    angle = start_angle
    target_angle = (degrees_to_turn + start_angle)
    print("Start angle: ",start_angle, " / ","Target Angle", target_angle)
    if ((degrees_to_turn >= 0 and degrees_to_turn <= 180) or (degrees_to_turn >= -360 and degrees_to_turn < -180) ):
        direction = 1 # Turn clockwise
    else:
        direction = -1 # Turn counterclockwise.
    while (direction * (angle - target_angle) < 0):   # Test
        print("Current_angle and Target_Angle:    \n",angle, target_angle)
        print("big")
        BP.set_motor_dps(B, -direction * 100)  #initial turning 
        BP.set_motor_dps(C, direction * 100) #opposite sign to create turning  
        # Constant iterations and stops                
        """elif ((abs(target_angle - angle) > 3) or (abs(target_angle - angle) > 3 and abs(target_angle - angle) < 357)):
            print("smol")
            BP.set_motor_dps(B, 0)   #this is to stop the turning before the next check 
            BP.set_motor_dps(C, 0)
            BP.set_motor_dps(B, direction * 15)
            BP.set_motor_dps(C, -direction * 15)
        else:
            BP.set_motor_dps(B, 0)
            BP.set_motor_dps(C, 0)

            if (direction == 1):
                BP.set_motor_dps(B, 5)
                BP.set_motor_dps(C, -5)
            elif (direction == -1):
                BP.set_motor_dps(B, -5)
                BP.set_motor_dps(C, 5)"""
        angle = getCurrAngle(EV3_GYRO)[0]
    BP.set_motor_power(B, 0)
    BP.set_motor_power(C, 0)      
    print("overshot\n")
    while (angle != target_angle):
        P = 0 # Proportional Feedback Value
        I = 0 # Integral Feedback Value
        KP = 2.5 # Proportional Gain value
        KI = 3 # Integral Gain value
        dT = 0.1 # Time step
        error =  direction * (angle - target_angle) # Error Value

        P = -KP * error   # Not sure if this should be positive or negative
        I +=  -KI * error * dT / 2   # Not sure if this should be positive or negative

        powerIn = (P + I) * 0.75
        BP.set_motor_power(B, powerIn)
        BP.set_motor_power(C, -powerIn)
        time.delay(dT)
        BP.set_motor_power(B, 0)
        BP.set_motor_power(C, 0) # Unsure if this will cover set_motor_dps to 0
        angle = getCurrAngle(EV3_GYRO)[0]
    print("finished")
    BP.set_motor_power(B, 0)
    BP.set_motor_power(C, 0)
        
def goStraight(offset = 0):
    BP.set_motor_dps(B, -200 - offset)
    BP.set_motor_dps(C, -200 + offset)
    time.sleep(delay)
    """BP.set_motor_dps(B, 0)
    BP.set_motor_dps(C, 0)"""

def stop():
    BP.set_motor_dps(B, 0)
    BP.set_motor_dps(C, 0)

#The following function is an attempt at a realignment function
"""
def checkAlignment(sonic_distance)
    if (sonic_distance[0] < 80 && sonic_distance[2] < 80) #checks to make sure it's between walls.  
        if (sonic_distance[0] - sonic_distance[2] < -6):
           print("Too far to the right ")
        elif(sonic_distance[0] - sonic_distance[2] > 6):
            print("Too far to the left ")
        else:
            print("Just fine")
    return
"""
def currDistance(ultrasonic_port, BP_Ultra):
    sonic_distance = 0
    if (ultrasonic_port != 0):
        try:
            for i in range(sonic_iterations):
                sonic_distance = sonic_distance + grovepi.ultrasonicRead(ultrasonic_port)
                time.sleep(0.02)
            sonic_distance = sonic_distance / sonic_iterations
        except TypeError:
            print("Error")
        except IOError:
            print("Error")
    elif (BP_Ultra != 0):
        try:
            for i in range(sonic_iterations):
                sonic_distance = sonic_distance + BP.get_sensor(BP_Ultra)
                time.sleep(0.02)
            sonic_distance = sonic_distance / sonic_iterations
        except TypeError:
            print("Error")
        except IOError:
            print("Error")
    return sonic_distance


def getCurrAngle(EV3_GYRO)
    angle = [0 , 0]
    for i in range(gyro_iterations):
        sensor_data = BP.get_sensor(EV3_GYRO)
        angle[0] = angle[0] + sensor_data[0]
        angle[1] = angle[1] + sensor_data[1]       
        time.sleep(0.02)
    for j in range(len(angle)):
        angle[j] = angle[j] / gyro_iterations
    return angle

# Returns absolute position from 0 to 360, angular velocity
def getStandardAngle(EV3_GYRO):
    angle = getCurrAngle(EV3_GYRO)
    angle[0] = angle[0] % 360
    return angle


#This function likely isn't needed now that we aren't using a motor to control the direction of the top ultrasonic.  
'''
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
'''

#This code creates a list of 3 elements, where the first element 
#is the left ultrasonic distance, the second element is the forward ultrasonic distance, 
#and the third element is the right ultrasonic distance
def checkUltrasonic(all_direction_distance):
    all_direction_distance[0] = currDistance(ultrasonic_left, 0)
    all_direction_distance[1] = currDistance(0, EV3_Ultra)
    all_direction_distance[2] = currDistance(ultrasonic_right, 0)
    return(all_direction_distance)

def openPaths(all_direction_distance):
    all_direction_distance = checkUltrasonic(all_direction_distance)
    paths_free = [False, False, False]
    if (all_direction_distance[1] > 10):
        print("Straight")
        paths_free[1] = True
    for i in [0, 2]:
        if (all_direction_distance[i] > 20):
            paths_free[i] = True
    return paths_free

def mapDirection(standard_angle, curr_loc): #curr_loc as a 1x2 array with the coordinates of the location the GEARS is at
    pos_shift = [0, 0]
    if (standard_angle - 360 > -45 and standard_angle < 45):
        curr_loc[1] += 1
        pos_shift = [0, 1]
    elif (standard_angle > 45 and standard_angle < 135): 
        curr_loc[0] -= 1
        pos_shift = [-1, 0]
    elif (standard_angle > 135 and standard_angle < 225):
        curr_loc[1] -= 1
        pos_shift = [0, -1]
    else:
        curr_loc[0] += 1
        pos_shift = [1, 0]
    return

def updateMap(mapFinal, curr_loc, pos_shift):
    if (pos_shift[0] == -1):
        for j in range(0, len(mapFinal)):
            row = mapFinal[j]
            row.insert(0, 0)
        curr_loc[0] += 1
    elif (pos_shift[1] == -1):
        mapFinal.append([0])
        for i in range(0, len(mapFinal[0]) - 1):
            mapFinal[len(mapFinal) - 1].append(0)
        curr_loc[1] += 1    
    else:
        print('WIP')
    return
   
##___MAIN CODE____##
time.sleep(delay_brickpi)

try:
    while True:
        goStraight()
        all_direction_distance = checkUltrasonic(all_direction_distance)
        """checkAlignment(all_direction_distance)"""
        if (all_direction_distance[1] < 12):
            stop() #Test to see if this is responsive enough (might overshoot too quick)
            paths_free = openPaths(all_direction_distance)
            if (all_direction_distance[0] > 12):
                print("left")
                turn(-90)
            elif (all_direction_distance[2] > 12):
                print("right")
                turn(90)
            else:
                print("turn around")
                turn(180)
        else:
            print("straight\n\n")
            
        #goStraight() for a certain amount of time
        #checkUltrasonic

        #distance_ahead = currDistance()
        #while (distance_ahead > 15):
        #    goStraight()
        #    distance_ahead = currDistance()
        #    time.sleep(delay)
        #all_direction_distance = [0, 0, 0]
        #all_direction_distance = checkUltrasonic(all_direction_distance)
        #if (all_direction_distance[0] > 15):
        #turn(90)
        
        #value = getCurrAngle(EV3_GYRO)
        #print(value)

        #myList = ','.join(map(str, myList)) # changes to csv
        #fopen('team07_map.csv', 'w')
        #fprintf(myList)
        #fclose('team07.map.csv')
        time.sleep(delay)

except KeyboardInterrupt:
    print("Keyboard Interrupt")
    BP.reset_all()
