from machine import Pin
import time
from math import sin

step = Pin(2, Pin.OUT)  
n_us = 5000
n_speed = 1.0 # 100% speed
n_time = 0
while(True):
    n_time +=1
    step.value(1)  # turn ON
    time.sleep_us(int(n_us*(1./n_speed)))
    step.value(0)  # turn OFF
    time.sleep_us(int(n_us*(1./n_speed)))

    # n_speed = sin(n_time * 0.1) * .5 + .5  # 0.15 to 0.85