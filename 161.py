Project3Team20Code.py

#Section 1
#Team 20
#Project 3

###Initialization###
##Imports_____##
from __future__ import print_function
from __future__ import division
import brickpi3
import IMU
import grovepi
import time
##____________##

"""
##MPUSetup____##
try:
    mpu = IMU.MPU9250()
except OSError:
    print("Error mpu")
##____________##
"""

##BrickPiSetup##
bp = brickpi3.BrickPi3()

bp.offset_motor_encoder(bp.PORT_A, bp.get_motor_encoder(bp.PORT_A))
bp.offset_motor_encoder(bp.PORT_D, bp.get_motor_encoder(bp.PORT_D))
bp.set_sensor_type(bp.PORT_1, bp.SENSOR_TYPE.CUSTOM, [(bp.SENSOR_CUSTOM.PIN1_ADC)]) # Configure for an analog on sensor port pin 1, and poll the analog line on pin 1.

##____________##

##GrovePiSetup##
line_finderLeft = 5
line_finderRight = 6
hall_sensor = 4
ultrasonic_ranger = 3

grovepi.pinMode(line_finderLeft,"INPUT")
grovepi.pinMode(line_finderRight,"INPUT")
grovepi.pinMode(hall_sensor,"INPUT")
##____________##

##Functions___##
#Returns -1 if left sensor detects, 1 if right sensor detects, and 0 if no sensors detect line
def ReadLines():
    left = grovepi.digitalRead(line_finderLeft)
    right = grovepi.digitalRead(line_finderRight)
    output = 0

    if (left == 0 and right == 0):
        output = 0
        #print ("No Lines Detected!")
        
    elif (left == 1 and right == 0):
        output = -1
        #print ("Line On Left Sensor")
        
    elif (left == 0 and right == 1):
        output = 1
        #print ("Line On Right Sensor")
        
    else:
        #print("Error- Line Detected On Both Sensors")
        pass
    
    return (output)

#Returns 0 if magnetic field is strong enough and -1 if magnetic field is not detected
def ReadMagneticField():
    try:
        mag = bp.get_sensor(bp.PORT_1)[0]
        #print("Raw value: %4d   Voltage: %5.3fv" % (mag, (mag / (4095.0 / bp.get_voltage_5v()))))
        if(mag >= 2100):
            mag = 1
        else:
            mag = 0
    except brickpi3.SensorError:
        print("Sensor Error")
    except IOError:
        print("Error")
        
    return mag

"""
#returns array like [accelx, accely, accelz, gyrox, gyroy, gyroz]
def ReadAcceAndRot(iterations, delay = 0.02):
    measurements = [0.0,0.0,0.0,0.0,0.0,0.0]
    
    for x in range(iterations):
        acc = mpu.readAccel()
        rot = mpu.readGyro()
        
        measurements[0] += acc['x'] / iterations
        measurements[1] += acc['y'] / iterations
        measurements[2] += acc['z'] / iterations
        measurements[3] += rot['x'] / iterations
        measurements[4] += rot['y'] / iterations
        measurements[5] += rot['z'] / iterations
        time.sleep(delay)
        
    return (measurements)
"""

#Returns distance in cm
def ReadUltrasonic(iterations, delay = 0.01):
    reading = 255
    try:
        reading = 0
        for x in range(0,iterations):
            reading += grovepi.ultrasonicRead(ultrasonic_ranger) / iterations
            time.sleep(delay)
            
    except TypeError:
        print("Error")
        
    return (reading)

#Returns angular velocity when given linear velocity
def CalcDPS(velo, wheelSize = 26.0):
    dps = 360 * velo / wheelSize
    return (dps)

#Sets motor angular velocity
def SetMotorDPS(dps, offset = 0):
    
    #Positive offset means we want to turn right
    moveSpeedC = dps - CalcDPS(offset)
    moveSpeedB = dps + CalcDPS(offset)
    
    #Setting motor speed
    if(offset > 0):
        bp.set_motor_dps(bp.PORT_C, moveSpeedC - dps)
        bp.set_motor_dps(bp.PORT_B, moveSpeedB)

    elif(offset < 0):
        bp.set_motor_dps(bp.PORT_C, moveSpeedC)
        bp.set_motor_dps(bp.PORT_B, moveSpeedB - dps)

    else:
        bp.set_motor_dps(bp.PORT_C, dps)
        bp.set_motor_dps(bp.PORT_B, dps)

#Calcs DPS and Sets Motor speed
def MoveAtVelo(velo, offset = 0):
    dps = CalcDPS(velo)
    SetMotorDPS(dps, offset)

#Sets the robot to drive a certain distance in a certain time 
def TravelDisInTime(distance, time):
    velo = distance / time
    CalcDPS(velo)
    currentDis = 0
    
    while (currentDis < distance):
        currentDis += velo / 50
        time.sleep(0.02)
        
    MoveAtVelo(0)
    
def ChangeOffset(direction):
    offsetChange = 0
    
    if(direction == 0):
        offsetChange = 0

    elif(direction == 1):
        offsetChange = botDefaultSpeed / 2
        
    elif(direction == -1):
        offsetChange = -botDefaultSpeed / 2

    return (offsetChange)

def ClampOffset(offset):
    #Top speed / offset right
    if(offset > botMaxSpeed - botDefaultSpeed):
        offset = botMaxSpeed - botDefaultSpeed
        print("Max Right Turn, Offset = ", offset)
        
    #Top speed / offset left
    if(offset < botDefaultSpeed - botMaxSpeed):
        offset = botDefaultSpeed - botMaxSpeed
        print("Max Right Left, Offset = ", offset)

    return (offset)

def IncrementMagTimer():
    global magTimer
    global magFields
    global magCounter
    if(magTimer <= 0):
        if(ReadMagneticField() == 1):
            magFields.insert(0, 1)
            magFields.pop(3)

            if(all(magFields)):
                magCounter += 1
                print("MagneticFields detected: ", magCounter)
                magTimer = magTimerMax
        else:
            magFields.insert(0, 0)
            magFields.pop(3)

    else:
        magTimer -= timeStep

def MagTurn():
    global botOffset
    while(ReadLines() != -1):
        bp.set_motor_dps(bp.PORT_C, CalcDPS(botDefaultSpeed))
        bp.set_motor_dps(bp.PORT_B, CalcDPS(-botDefaultSpeed / 2))
        time.sleep(timeStep)
    
#Start Code_________________________________________
ContinueMission = True
useLines = True
move = True
dropCargo = False
botDefaultSpeed = 30
botMaxSpeed = botDefaultSpeed * 3
botOffset = 0
magTimer = 0
magTimerMax = 2
magTurnTimer = 0.3
magDropTimer = 0.9
magCounter = 0
magCounterDestin = 3
timeStep = 0.05
magFields = [0,0,0]

try:

    bp.set_motor_position(bp.PORT_A, 0)
    bp.set_motor_position(bp.PORT_D, 0)
    time.sleep(10)
    while ContinueMission:
        IncrementMagTimer()
        lines = 0
         
        if(useLines):
            #___________Sensing_____
            if(magCounter == magCounterDestin):
                if(magTurnTimer <= 0):
                    MagTurn()
                    magCounter += 1
                    move = True
                else:
                    magTurnTimer -= timeStep
                    MoveAtVelo(botDefaultSpeed, 0)
                    move = False
                    
            elif(magCounter == magCounterDestin + 2):
                if(magDropTimer <= 0):
                    dropCargo = True
                    magCounter += 1    
                else:
                    magDropTimer -= timeStep
                
                    
            elif(magCounter == magCounterDestin + 4):
                ContinueMission = False

            #Check if hit line
            else:
                lines = ReadLines()
            #########################
                    
            #___________Moving_____
            #If hitting line then turn
            if(lines != 0):    
                botOffset = ChangeOffset(lines)
                MoveAtVelo(botDefaultSpeed, botOffset)

            #Default curve to left
            elif(move == True):
                bp.set_motor_dps(bp.PORT_C, CalcDPS(botDefaultSpeed))
                bp.set_motor_dps(bp.PORT_B, CalcDPS(botDefaultSpeed * 7 / 10))
            ########################
                    
            #___________Cargo_____
            if(dropCargo == True):
                bp.set_motor_position(bp.PORT_A, -90)
                bp.set_motor_position(bp.PORT_D, -90)

            else:
                bp.set_motor_position(bp.PORT_A, 0)
                bp.set_motor_position(bp.PORT_D, 0)
            ########################

        else:
            #bp.set_motor_dps(bp.PORT_C, CalcDPS(botDefaultSpeed))
            #bp.set_motor_dps(bp.PORT_B, CalcDPS(botDefaultSpeed))
            bp.set_motor_position(bp.PORT_A, 0)
            bp.set_motor_position(bp.PORT_D, 0)
            #print(bp.get_motor_encoder(bp.PORT_A))
            pass
    
        time.sleep(timeStep)

    bp.reset_all()
    
except KeyboardInterrupt:
    bp.reset_all()
    
