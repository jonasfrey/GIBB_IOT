# file: scan_outputs.py
from machine import Pin, PWM
import time

SAFE_GPIO = [2,4,5,12,13,14,15,16,17,18,19,21,22,23,25,26,27,32,33]  # not 6–11 (flash)

print("WATCH the shield: each GPIO will pulse for 0.3s. Note which LED/buzzer reacts.")
for g in SAFE_GPIO:
    try:
        p = Pin(g, Pin.OUT)
        p.value(1); time.sleep(0.3); p.value(0)
        # quick buzz test too
        try:
            pwm = PWM(Pin(g), freq=1200, duty=600)
            time.sleep(0.15)
            pwm.deinit()
        except: pass
        print("Pulsed GPIO", g)
        time.sleep(0.2)
    except Exception as e:
        print("Skip GPIO", g, e)
