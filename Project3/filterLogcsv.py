from MPU9250 import MPU9250
import numpy as np
import sys
import smbus
import time

from IMUFilters import AvgCali
from IMUFilters import genWindow
from IMUFilters import WindowFilterDyn
from IMUFilters import KalmanFilter
from IMUFilters import FindSTD
from IMUFilters import InvGaussFilter


mpu9250 = MPU9250()
feele = open("dataSet.csv","w")

#Parameters
width=1
depth=100
dly=0.01
adv = True
#/////////

accelx=genWindow(width,0)#Can play with width to adjust system
accely=genWindow(width,0)
accelz=genWindow(width,0)
gyrox=genWindow(width,0)#Can play with width to adjust system
gyroy=genWindow(width,0)
gyroz=genWindow(width,0)
flter=[[0.7,1.0],[0.7,1.0],[0.7,1.0],[0.7,1.0],[0.7,1.0],[0.7,1.0]]# [r,q]Will need to play with each filter value
biases=AvgCali(mpu9250,depth,dly)
state=[[0.0,0.0,0.0,0.0,0.0,0.0],[0,0,0,0,0,0]]#Estimated error (p) and measurement state (x) 
out=[0,0,0,0,0,0]
std=FindSTD(biases,mpu9250,dly)
pick = 1 #1 uses window filter, anything else uses Kalman
count = 3 #Number of standard deviations used for filtering

t0=time.time()

try:
        while True:
                if pick == 1:
                        accel = mpu9250.readAccel()
                        gyro = mpu9250.readGyro()
                        #mag = mpu9250.readMagnet()
	
                        accelx=WindowFilterDyn(accelx,dly,InvGaussFilter(adv,accel['x'], biases[0],std[0],count))
                        accely=WindowFilterDyn(accely,dly,InvGaussFilter(adv,accel['y'], biases[1],std[1],count))
                        accelz=WindowFilterDyn(accelz,dly,InvGaussFilter(adv,accel['z'], biases[2],std[2],count))
                        gyrox=WindowFilterDyn(gyrox,dly,InvGaussFilter(adv,gyro['x'], biases[3],std[3],count))
                        gyroy=WindowFilterDyn(gyroy,dly,InvGaussFilter(adv,gyro['y'], biases[4],std[4],count))
                        gyroz=WindowFilterDyn(gyroz,dly,InvGaussFilter(adv,gyro['z'], biases[5],std[5],count))
                        out[0]=accelx[0]
                        out[1]=accely[0]
                        out[2]=accelz[0]
                        out[3]=gyrox[0]
                        out[4]=gyroy[0]
                        out[5]=gyroz[0]
                else:
                        state=KalmanFilter(mpu9250,state,flter,dly)
                        out[0]=InvGaussFilter(adv,state[1][0], biases[0],std[0],count)
                        out[1]=InvGaussFilter(adv,state[1][1], biases[1],std[1],count)
                        out[2]=InvGaussFilter(adv,state[1][2], biases[2],std[2],count)
                        out[3]=InvGaussFilter(adv,state[1][3], biases[3],std[3],count)
                        out[4]=InvGaussFilter(adv,state[1][4], biases[4],std[4],count)
                        out[5]=InvGaussFilter(adv,state[1][5], biases[5],std[5],count)
                
                feele.write("acell,")
                feele.write(str(out[0]))
                feele.write (",")
                feele.write(str(out[1]))
                feele.write (",")
                feele.write(str(out[2]))
                feele.write(",")
                
                feele.write ("gyro,",)
                feele.write(str(out[3]))
                feele.write (",",)
                feele.write(str(out[4]))
                feele.write (",",)
                feele.write(str(out[5]))
                feele.write(",")

                t=time.time()
                delt=t-t0
                feele.write("time,")
                feele.write(str(delt))
                feele.write("\n")
                t0=time.time()

# Integrate a wait to allow for new data to be available
#               time.sleep(0.5)

except KeyboardInterrupt:
        feele.close()
        sys.exit()

