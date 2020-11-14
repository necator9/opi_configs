from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port

alive = port.PA7
gpio.init()
gpio.setcfg(alive, gpio.OUTPUT)

while True:
    gpio.output(alive, 1)
    sleep(0.7)
    gpio.output(alive, 0)
    sleep(80)
