# ir_tx.py (ESP32 + MicroPython)
from machine import Pin, PWM
import time

class IRSender:
    def __init__(self, pin=18, carrier=38000, duty_pct=33):
        self.pwm = PWM(Pin(pin), freq=carrier, duty=0)  # duty: 0..1023 on ESP32
        self._on = int(1023 * duty_pct / 100)

    def _mark(self, us):
        self.pwm.duty(self._on)
        time.sleep_us(int(us))
        self.pwm.duty(0)

    def _space(self, us):
        self.pwm.duty(0)
        time.sleep_us(int(us))

    # Send a raw bursts list: [mark, space, mark, space, ...] in microseconds
    def send_raw(self, bursts_us):
        for i, dur in enumerate(bursts_us):
            if i % 2 == 0:
                self._mark(dur)
            else:
                self._space(dur)

    # NEC 32-bit (LSB first): typical TV remotes
    def send_nec32(self, code):
        # Leader
        self._mark(9000); self._space(4500)
        # 32 data bits, LSB first
        for i in range(32):
            self._mark(560)
            if (code >> i) & 1:
                self._space(1690)   # '1'
            else:
                self._space(560)    # '0'
        # Trailer
        self._mark(560)
        self._space(40000)  # inter-frame gap (safety)

# ===== Example usage =====
# Wire the IR LED through a small NPN transistor to 5V; use series resistor.
ir = IRSender(pin=13, carrier=38000, duty_pct=33)




# Test
while True:
    # NEC 32-bit example:    send_nec(0xFF609F)   # OFF

    ir.send_nec32(0xFFE01F) #on
    time.sleep(2)
    ir.send_nec32(0xFF609F) #off
    time.sleep(2)