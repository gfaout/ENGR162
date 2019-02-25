#Section 1
#Team 07
#Project 3

#Initialization and Dependency Imports
##from __future__ import print_function
##from __future__ import division
import IMU
import brickpi3
import grovepi
import time

#IMU Setup
try: 
	imu = IMU.MPU9250()
except: 
	print("IMU Initialization Error")
	
#Brickpi Setup
try:
	bp = brickpi3.BrickPi3()
	

