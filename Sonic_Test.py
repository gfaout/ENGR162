from __future__ import print_function
from __future__ import division
import grovepi
import time
import grovepi_functions as grove


try:
        while True:
                try:
                        distance = grove.curr_distance()
                        print(distance)
                except TypeError:
                        print("TypeError")

                except IOError:
                        print("IOError")
except KeyboardInterrupt:
        print("Ending")

    
