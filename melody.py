from machine import Pin, PWM
import time

buzzer = PWM(Pin(25))

def beep(freq, duration_ms):
    buzzer.freq(freq)
    buzzer.duty(512)
    time.sleep(duration_ms / 1000)
    buzzer.duty(0)
    time.sleep(0.02)  # short pause between notes

# Simple melody: C4, D4, E4, C4
melody = [
    (262, 300),  # C4
    (294, 300),  # D4
    (330, 300),  # E4
    (262, 500),  # C4
    (262, 300),  # C4
    (294, 300),  # D4
    (330, 300),  # E4
    (262, 500),  # C4
]

for note, duration in melody:
    beep(note, duration)

buzzer.deinit()