from __future__ import print_function
from __future__ import division
import brickpi3
import grovepi
import time
import MPU9250
from math import sqrt, pi

#### Import statements, constants settings, and grovepi setup ####
BP = brickpi3.BrickPi3()
mpu9250 = MPU9250.MPU9250()
Tilt_Motor = BP.PORT_C   # This controls the tilting arm of the 
L_Motor = BP.PORT_D  # Left wheel   # positive moves wheel backward & negative forward
R_Motor = BP.PORT_B  # Right wheel
EV3_GYRO = BP.PORT_3
EV3_Ultra = BP.PORT_4
delay_brickpi = 4
delay = 0.03
gyro_iterations = 5
sonic_iterations = 5
ultrasonic_center = 2
ultrasonic_right = 7
infra1= 14		# Pin 14 is A2 Port.
infra2 = 15		# Pin 15 is A3 Port.
grovepi.pinMode(infra1,"INPUT")
grovepi.pinMode(infra2,"INPUT")
#imu = 6
grovepi.pinMode(ultrasonic_center, "INPUT")
grovepi.pinMode(ultrasonic_right, "INPUT")
all_direction_distance = [0, 0, 0]
front_distance = 20
side_distance = 40
map = [5] #1 indicates path, 0 indicates not part of path, 5 is start, 2 is heat, 3 is magnet, 4 is end
w_radius = 4.3 # radius in cm
ir_thresh = 374
mag_thresh = 204.68

####_________________________________________________________####

#### Brickpi Sensor Setup ####
BP.set_sensor_type(EV3_GYRO, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
BP.set_sensor_type(EV3_Ultra, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM) 
####________#####


def readMag():
    try:
        mag = mpu9250.readMagnet()
        mag_value = [mag['x'],mag['y'],mag['z']]
        size_mag = sqrt(mag_value[0]**2 + mag_value[1]**2 + mag_value[2]**2)
        return mag_value, size_mag
    except IOError:
        print("Magnet IO Error")
        return [-1,-1,-1], 1


# Output function
def IR_PrintValues():
    try:
        infra1= 14		# Pin 14 is A0 Port.
        infra2 = 15		# Pin 15 is A0 Port.               
        sensor1_value = grovepi.analogRead(infra1)
        sensor2_value = grovepi.analogRead(infra2)
        
        print ("One = " + str(sensor1_value) + "\tTwo = " + str(sensor2_value))
        time.sleep(.1) # Commenting out for now
    except IOError:
        print ("Error")

#Read Function		
def IR_Read():
    try:
        infra1= 14		# Pin 14 is A0 Port.
        infra2 = 15		# Pin 15 is A0 Port.                
        sensor1_value = grovepi.analogRead(infra1)
        sensor2_value = grovepi.analogRead(infra2)
        ir_mag = sqrt(sensor1_value**2 + sensor2_value**2)
        return [sensor1_value, sensor2_value],ir_mag
    except IOError:
        print ("Error")

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
        BP.set_motor_dps(L_Motor, direction * 100)  #initial turning 
        BP.set_motor_dps(R_Motor, -direction * 100) #opposite sign to create turning  
        # Constant iterations and stops                
        """elif ((abs(target_angle - angle) > 3) or (abs(target_angle - angle) > 3 and abs(target_angle - angle) < 357)):
            print("smol")
            BP.set_motor_dps(L_Motor, 0)   #this is to stop the turning before the next check 
            BP.set_motor_dps(R_Motor, 0)
            BP.set_motor_dps(L_Motor, direction * 15)
            BP.set_motor_dps(R_Motor, -direction * 15)
        else:
            BP.set_motor_dps(L_Motor, 0)
            BP.set_motor_dps(R_Motor, 0)

            if (direction == 1):
                BP.set_motor_dps(L_Motor, 5)
                BP.set_motor_dps(R_Motor, -5)
            elif (direction == -1):
                BP.set_motor_dps(L_Motor, -5)
                BP.set_motor_dps(R_Motor, 5)"""
        angle = getCurrAngle(EV3_GYRO)[0]
    BP.set_motor_power(L_Motor, 0)
    BP.set_motor_power(R_Motor, 0)      
    print("overshot\n")
    while (angle != target_angle):
        P = 0 # Proportional Feedback Value
        I = 0 # Integral Feedback Value
        KP = 1.5 # Proportional Gain value
        KI = 2 # Integral Gain value
        dT = 0.1 # Time step
        error =  direction * (angle - target_angle) # Error Value

        P = -KP * error   # Not sure if this should be positive or negative
        I +=  -KI * error * dT / 2   # Not sure if this should be positive or negative
        powerIn = (P + I) * 2
        if (abs(angle - target_angle) <= 2):
            BP.set_motor_power(L_Motor, direction * powerIn * 1.5)
            BP.set_motor_power(R_Motor, -direction * powerIn * 1.5)
            time.sleep(dT)
            print("near break")
            print(abs(angle - target_angle))
            print(target_angle)
            break
            print(abs(angle - target_angle))
        elif (abs(angle - target_angle) <= 1.1):
            print("broke")
            print(abs(angle - target_angle))
            break
        else:
            powerIn = (P + I) * 2
        BP.set_motor_power(L_Motor, direction * powerIn)
        BP.set_motor_power(R_Motor, -direction * powerIn)
        time.sleep(dT)
        
        BP.set_motor_power(L_Motor, 0)
        BP.set_motor_power(R_Motor, 0) # Unsure if this will cover set_motor_dps to 0
        angle = getCurrAngle(EV3_GYRO)[0]
        print(str(angle))
        print("abs: %d", (abs(angle - target_angle)))
    
    print("finished")
    print(getCurrAngle(EV3_GYRO)[0])
    BP.set_motor_power(L_Motor, 0)
    BP.set_motor_power(R_Motor, 0)
        
def goStraight(offset = 0):
    BP.set_motor_dps(L_Motor, 200 - offset)
    BP.set_motor_dps(R_Motor, 200 + 0.0 + offset)
    time.sleep(delay)
    """BP.set_motor_dps(L_Motor, 0)
    BP.set_motor_dps(R_Motor, 0)"""

def stop():
    BP.set_motor_dps(L_Motor, 0)
    BP.set_motor_dps(R_Motor, 0)

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
                time.sleep(0.005)
            sonic_distance = sonic_distance / sonic_iterations
        except TypeError:
            print("Error")
        except IOError:
            print("Error")
    elif (BP_Ultra != 0):
        try:
            for i in range(sonic_iterations):
                sonic_distance = sonic_distance + BP.get_sensor(BP_Ultra)
                time.sleep(0.005)
            sonic_distance = sonic_distance / sonic_iterations
        except TypeError:
            print("Error")
        except IOError:
            print("Error")
    return sonic_distance


def getCurrAngle(EV3_GYRO = EV3_GYRO):
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
def getStandardAngle(EV3_GYRO = EV3_GYRO):
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
    all_direction_distance[0] = currDistance(0, EV3_Ultra)
    all_direction_distance[1] = currDistance(ultrasonic_center, 0)
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
"""
def move_square():
    
    while (mag_mag < mag_thresh and ir_mag < ir_thresh and )
        goDistance(4,0.4)
        ir_array, ir_mag = IR_Read()
        mag_array, mag_mag = readMag()
        if (mag_mag > mag_thresh or ir_mag > ir_thresh):
            turn(180)
    return    
"""
def goDistance(distance, time):
    BP.set_motor_dps(L_Motor,(distance / (2 * pi * w_radius)) * (360 / time))
    BP.set_motor_dps(R_Motor,(distance / (2 * pi * w_radius)) * (360 / time))
    time.sleep(time)
    stop()
    

def navMaze():
    all_dist = [0, 0, 0]
    all_dist = checkUltrasonic(all_dist)
    #print("%d %d %d", all_dist[0], all_dist[1], all_dist[2])
    ir_array, ir_mag = IR_Read()
    mag_array, mag_mag = readMag()
    if (ir_mag > ir_thresh):
        print("IR Beacon found")
        turn(180)
        goStraight()
        time.sleep(0.3)
        return
    elif (mag_mag > mag_thresh):
        print("Magnetic Beacon found")
        turn(180)
        goStraight()
        time.sleep(0.3)
        return
    if (all_dist[0] > side_distance):
        stop()
        print("Turn Left")
        turn(-85)
        print("Now Going Straight")
        goStraight()
        time.sleep(5)
        stop()
        print("Finished going straight - Left")
    elif (all_dist[1] > front_distance and all_dist[0] <= side_distance):
        goStraight()
        print("straight")
        time.sleep(0.03)
    elif (all_dist[2] > side_distance and all_dist[0] <= side_distance and all_dist[1] <= front_distance):
        stop()
        print("Turn Right")
        turn(75)
        print("Now Going Straight")
        goStraight()
        time.sleep(5)
        stop()
        print("Finished going straight - Right")
    elif (all_dist[0] > side_distance and all_dist[2] > side_distance and all_dist[1] > front_distance):
        stop()
        BP.set_motor_dps(Tilt_Motor, 150)
        time.sleep(1.25)
        BP.set_motor_dps(Tilt_Motor,0)
    else:
        print("180 turn")
        turn(180)
        goStraight()
        time.sleep(0.5)

def inputArray():
    length = (input("What is the array length? "))
    width = (input("What is the array width? "))
    return [[0] * int(length) for i in range(int(width))]

def mapDirection(standard_angle, curr_loc): #curr_loc as a 1x2 array with the coordinates of the location the GEARS is at
    if (standard_angle - 360 > -45 and standard_angle < 45):
        curr_loc[1] += 1 # up
    elif (standard_angle > 45 and standard_angle < 135): 
        curr_loc[0] -= 1 # left
    elif (standard_angle > 135 and standard_angle < 225):
        curr_loc[1] -= 1 # down
    else:
        curr_loc[0] += 1 # right
    return

def coordShift(mapFinal, curr_loc):
    return [curr_loc[0], length - curr_loc[1] - 1] # coordinates for matrix

def updateMap(mapFinal, curr_loc): # add conditionals here for other numbers on map
    coordinates = coordShift(mapFinal, curr_loc)
    mapFinal[coordinates[1]][coordinates[0]] = 1

##___MAIN CODE____##
time.sleep(delay_brickpi)
try:
    BP.set_motor_dps(Tilt_Motor,0)
    while True:
        navMaze()
        time.sleep(0.05)

    """while True:
        navMaze()
        print("Finished 1 iteration")
        time.sleep(0.01)"""
    stop()
except KeyboardInterrupt:
    stop()
    print("Keyboard Interrupt")
    BP.reset_all()



"""goStraight()
    all_direction_distance = checkUltrasonic(all_direction_distance)
    #checkAlignment(all_direction_distance)
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
        time.sleep(delay)"""
