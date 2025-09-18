from machine import Pin
import time
from math import sin

led = Pin(2, Pin.OUT)  # GPIO for D7
n_duty_cycle_nor = 0.15  # 15% duty cycle
n_microsec_period = 20000  # 50ms period = 20Hz
n_time = 0
while(True):
    n_time +=1
    led.value(1)  # turn ON
    time.sleep_us(int(n_duty_cycle_nor * n_microsec_period))
    led.value(0)  # turn OFF
    time.sleep_us(int((1 - n_duty_cycle_nor) * n_microsec_period))


    # slowly modulate the duty cycle
    #sin is not defined so we have to approximate it
    #   so we use a library that is available

    n_duty_cycle_nor = sin(n_time * 0.05) * .5 + .5  # 0.15 to 0.85