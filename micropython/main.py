from machine import Pin, PWM
import time

buzzer = PWM(Pin(27))  # change GPIO as needed
buzzer.freq(1000)
buzzer.duty(512)
time.sleep(0.5)
buzzer.deinit()