from machine import Pin, PWM
import time

IR_PIN = 13
pwm = PWM(Pin(IR_PIN), freq=38000, duty=0)  # start with off

def send_burst(duration_us):
    pwm.duty(512)          # turn IR on
    time.sleep_us(duration_us)
    pwm.duty(0)            # turn IR off

def send_space(duration_us):
    time.sleep_us(duration_us)

def send_nec(code):
    # Leader
    send_burst(9000)
    send_space(4500)

    # 32 data bits (LSB first)
    for i in range(32):18
        send_burst(560)
        if code & (1 << i):
            send_space(1690)  # '1'
        else:
            send_space(560)   # '0'

    # Stop bit
    send_burst(560)

# Test
while True:
    send_nec(0xFFE01F)   # ON
    time.sleep(2)
    send_nec(0xFF609F)   # OFF
    time.sleep(2)