#!/usr/bin/env python
# -*- coding: utf-8 -*-

import OPi.GPIO as GPIO
from time import sleep         

GPIO.setboard(GPIO.ZEROPLUS2H5)        
GPIO.setmode(GPIO.SOC)          	 # set up SOC numbering

alive_gpio = GPIO.PA+7              
GPIO.setup(alive_gpio, GPIO.OUT)     

try:
    print 'Arduino-OPi watchdog started'
    while True:
        GPIO.output(alive_gpio, 1)       # set port/pin value to 1/HIGH/True
        sleep(0.7)
        GPIO.output(alive_gpio, 0)
        sleep(80)

except KeyboardInterrupt:
    GPIO.output(alive_gpio, 0)
    GPIO.cleanup()              		 # clean up after yourself
    print 'Arduino-OPi watchdog finished'
