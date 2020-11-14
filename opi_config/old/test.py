import time 
import OPi.GPIO as GPIO
GPIO.setboard(GPIO.ZEROPLUS2H5)
GPIO.setmode(GPIO.BOARD)
GPIO.output(11, 1)
time.sleep(10)
