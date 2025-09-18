from machine import Pin, PWM
import time

buzzer = PWM(Pin(25))  # GPIO 25
buzzer.freq(1000)      # set frequency to 1 kHz
buzzer.duty(512)       # duty cycle (0–1023); 512 ≈ 50%
time.sleep(0.5)        # beep for 0.5 seconds
buzzer.deinit()        # turn it off