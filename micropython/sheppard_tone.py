# MicroPython — Shepard-tone–like sweep on GPIO 25 (Acebott buzzer)
from machine import Pin, PWM
import time, math

BUZZER_PIN = 26
buzzer = PWM(Pin(BUZZER_PIN), freq=220, duty=0)  # duty 0–1023 on ESP32

def shepard_tone(seconds=12, f_start=110, octaves=5, steps_per_oct=48, up=True, max_duty=700):
    """
    Approximate a Shepard tone on a single buzzer by sweeping frequency while
    applying a cyclic amplitude envelope so each octave fades in/out.
    """
    total_steps = steps_per_oct * octaves
    step_time = seconds / total_steps
    for i in range(total_steps):
        n = i if up else (total_steps - 1 - i)

        # musical (exponential) sweep
        freq = f_start * (2 ** (n / steps_per_oct))

        # position within current octave [0..1)
        frac = (n % steps_per_oct) / steps_per_oct

        # Hann window envelope -> fades one octave in while next fades out
        env = 0.15 + 0.85 * 0.5 * (1 - math.cos(2 * math.pi * frac))  # 0.15..1.0

        # update PWM
        buzzer.freq(int(freq))
        buzzer.duty(int(max_duty * env))  # scale loudness with envelope
        time.sleep(step_time)

    buzzer.duty(0)

try:
    # repeat to reinforce the endless-rise illusion
    shepard_tone(seconds=12, f_start=555, octaves=3, steps_per_oct=48, up=True)
    shepard_tone(seconds=12, f_start=555, octaves=3, steps_per_oct=48, up=True)
    # uncomment for a falling tone:
    # shepard_tone(seconds=12, f_start=110, octaves=5, steps_per_oct=48, up=False)
finally:
    buzzer.deinit()