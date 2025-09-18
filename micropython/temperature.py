from machine import ADC, Pin
import time
import math

# Config
R_NOMINAL = 10000      # resistance at 25°C (Ohms)
BETA = 3950            # Beta value
SERIES_RESISTOR = 10000  # your fixed resistor value (Ohms)
V_SUPPLY = 3.3

adc_ntc = ADC(Pin(33))
adc_ntc.atten(ADC.ATTN_11DB)   # full range 0–3.3V
adc_ntc.width(ADC.WIDTH_12BIT) # 0–4095 resolution

while True:
    raw = adc_ntc.read()
    voltage = raw * V_SUPPLY / 4095
    resistance = SERIES_RESISTOR * (V_SUPPLY / voltage - 1)

    # Convert to temperature (Celsius)
    temp_k = 1 / (1 / (25 + 273.15) + (1 / BETA) * math.log(resistance / R_NOMINAL))
    temp_c = temp_k - 273.15

    print("Raw:", raw,
          "Voltage:", round(voltage, 3), "V",
          "Resistance:", round(resistance), "Ω",
          "Temp:", round(temp_c, 2), "°C")

    time.sleep(1)
