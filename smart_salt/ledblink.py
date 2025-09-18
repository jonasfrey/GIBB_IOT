from machine import Pin
import time

led = Pin(2, Pin.OUT)  # GPIO for D7
while(True):
    led.value(1)  # turn ON
    time.sleep(1)
    led.value(0)  # turn OFF
    time.sleep(1)
