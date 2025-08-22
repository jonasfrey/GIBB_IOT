
from machine import Pin, time_pulse_us
import utime
n_pin_sensor_ir = 27 # D2 arduino
# Use the mapping helper from earlier to resolve Arduino D2 -> ESP32 GPIO
IR_PIN = Pin(n_pin_sensor_ir, Pin.IN, Pin.PULL_UP)  # IR receiver on Arduino D2

def _pulse(duration, level, to=25000):
    # measure a pulse and check it’s close to expected 'duration' (µs)
    t = time_pulse_us(IR_PIN, level, to)
    return t if t > 0 and abs(t - duration) < duration * 0.4 else -1

def ir_read_nec(timeout_ms=300):
    """
    Blocking read of one NEC frame.
    Returns 32-bit int (address<<16 | co    mmand<<8 | ~command) or None on timeout.
    """
    # what does this do 
    t0 = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), t0) < timeout_ms:
        # Wait for leader: ~9ms LOW, ~4.5ms HIGH
        if _pulse(9000, 0) > 0 and _pulse(4500, 1) > 0:
            data = 0
            for _ in range(32):
                if _pulse(560, 0) < 0:
                    return None
                hi = time_pulse_us(IR_PIN, 1, 10000)
                if hi < 0:
                    return None
                bit = 1 if hi > 1000 else 0  # ~560us => 0, ~1690us => 1
                data = (data << 1) | bit
            return data
    return None

# Demo loop: print decoded NEC code when a key is pressed
while True:
    code = ir_read_nec()
    if code is not None:
        print("IR:", hex(code))