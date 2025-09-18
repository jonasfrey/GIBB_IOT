from machine import Pin
import time

# Arduino D2 (IR receiver pin) → ESP32 GPIO25 from your mapping
ir = Pin(27, Pin.IN)

while True:
    # print("IR value")
    # print without newline
    print(ir.value(), end="") 
    # print(ir.value()) 
    # time.sleep_us(2)