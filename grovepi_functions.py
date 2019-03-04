import grovepi
import time

import grovepi_functions as grove

ultrasonic = 4
sonic_iterations = 5

grovepi.pinMode(ultrasonic, "INPUT")


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


