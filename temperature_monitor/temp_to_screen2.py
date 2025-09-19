import time
from machine import ADC, Pin
import math
from micropython import const

# TM1637 Constants
TM1637_CMD1 = const(64)  # 0x40 data command
TM1637_CMD2 = const(192) # 0xC0 address command
TM1637_CMD3 = const(128) # 0x80 display control command
TM1637_DSP_ON = const(8) # 0x08 display on
TM1637_DELAY = const(10) # 10us delay between clk/dio pulses
TM1637_MSB = const(128)  # msb is the decimal point or the colon

# 0-9, a-z, blank, dash, star
_SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

class TM1637(object):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""
    def __init__(self, clk, dio, brightness=7):
        self.clk = clk
        self.dio = dio

        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        time.sleep_us(TM1637_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        self.dio(0)
        time.sleep_us(TM1637_DELAY)
        self.clk(0)
        time.sleep_us(TM1637_DELAY)

    def _stop(self):
        self.dio(0)
        time.sleep_us(TM1637_DELAY)
        self.clk(1)
        time.sleep_us(TM1637_DELAY)
        self.dio(1)

    def _write_data_cmd(self):
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        self._start()
        self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | self._brightness)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            time.sleep_us(TM1637_DELAY)
            self.clk(1)
            time.sleep_us(TM1637_DELAY)
            self.clk(0)
            time.sleep_us(TM1637_DELAY)
        self.clk(0)
        time.sleep_us(TM1637_DELAY)
        self.clk(1)
        time.sleep_us(TM1637_DELAY)
        self.clk(0)
        time.sleep_us(TM1637_DELAY)

    def write(self, segments, pos=0):
        if not 0 <= pos <= 5:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        self._start()
        self._write_byte(TM1637_CMD2 | pos)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._write_dsp_ctrl()

    def encode_char(self, char):
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36]  # space
        if o == 42:
            return _SEGMENTS[38]  # star/degrees
        if o == 45:
            return _SEGMENTS[37]  # dash
        if o == 46:
            return 0x80  # decimal point (dot)
        if o >= 65 and o <= 90:
            return _SEGMENTS[o-55]  # uppercase A-Z
        if o >= 97 and o <= 122:
            return _SEGMENTS[o-87]  # lowercase a-z
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48]  # 0-9
        raise ValueError("Character out of range: {:d} '{:s}'".format(o, chr(o)))

    def encode_string(self, string):
        segments = bytearray(len(string))
        for i in range(len(string)):
            segments[i] = self.encode_char(string[i])
        return segments

    def show(self, string, colon=False):
        segments = self.encode_string(string)
        if len(segments) > 1 and colon:
            segments[1] |= 128
        self.write(segments[:4])

# TM1637 Display setup
tm = TM1637(clk=Pin(18), dio=Pin(17))

# LED setup
blue_led = Pin(25, Pin.OUT)
green_led = Pin(14, Pin.OUT)
yellow_led = Pin(13, Pin.OUT)
red_led = Pin(12, Pin.OUT)

def turn_off_all_leds():
    """Turn off all LEDs"""
    blue_led.off()
    green_led.off()
    yellow_led.off()
    red_led.off()

def control_temperature_leds(temp):
    """Control LEDs based on temperature"""
    # Turn off all LEDs first
    turn_off_all_leds()
    
    # Turn on appropriate LED based on temperature
    if temp < 20.0:
        blue_led.on()    # Blue - Cold
    elif temp < 23.0:
        green_led.on()   # Green - Cool  
    elif temp <= 25.0:
        yellow_led.on()  # Yellow - Warm
    else:
        red_led.on()     # Red - Hot
tm.show('INIT')
turn_off_all_leds()  # Turn off all LEDs at startup
time.sleep(1)

# Thermistor Configuration
R_NOMINAL = 10000      # NTC resistance at 25°C (10kΩ)
TEMP_NOMINAL = 25      # Temperature for nominal resistance (°C)
BETA = 3950            # Beta coefficient (check your NTC datasheet)
SERIES_RESISTOR = 10000  # Fixed resistor value (10kΩ)
V_SUPPLY = 3.3         # Supply voltage

# ADC setup
adc_ntc = ADC(Pin(33))  # Make sure this matches your wiring
adc_ntc.atten(ADC.ATTN_11DB)   # Full range 0-3.3V
adc_ntc.width(ADC.WIDTH_12BIT) # 12-bit resolution (0-4095)

def calculate_temperature(adc_reading):
    """Calculate temperature from ADC reading using Steinhart-Hart equation"""
    
    # Convert ADC reading to voltage
    voltage = adc_reading * V_SUPPLY / 4095.0
    
    # Handle edge cases
    if voltage <= 0.01:  # Very low voltage
        print("Warning: Very low voltage, check wiring")
        return None
    if voltage >= V_SUPPLY - 0.01:  # Very high voltage
        print("Warning: Very high voltage, check wiring") 
        return None
    
    # Calculate thermistor resistance using voltage divider
    # For voltage divider: V_out = V_in * R_ntc / (R_series + R_ntc)
    # Solving for R_ntc: R_ntc = R_series * V_out / (V_in - V_out)
    resistance = SERIES_RESISTOR * voltage / (V_SUPPLY - voltage)
    
    # Steinhart-Hart equation (simplified Beta parameter equation)
    # 1/T = 1/T0 + (1/B) * ln(R/R0)
    # Where T and T0 are in Kelvin
    temp_k = 1.0 / ((1.0 / (TEMP_NOMINAL + 273.15)) + 
                    (1.0 / BETA) * math.log(resistance / R_NOMINAL))
    
    temp_c = temp_k - 273.15
    
    return temp_c, voltage, resistance

def display_temperature(temp):
    """Display temperature on TM1637 with proper formatting"""
    if temp is None:
        tm.show('Err-')
        return
        
    if temp < -9:
        tm.show('Lo--')
    elif temp > 999:
        tm.show('Hi--')
    elif temp >= 100:
        # Show as integer for temps >= 100°C
        tm.show(str(int(temp)))
    elif temp >= 0:
        # For positive temps < 100, show with decimal point
        if temp >= 10:
            # Two digits + decimal + one digit: "23.5"
            temp_int = int(temp)
            temp_decimal = int((temp - temp_int) * 10)
            segments = tm.encode_string(str(temp_int) + str(temp_decimal))
            # Add decimal point to the second digit
            if len(segments) >= 2:
                segments[1] |= 0x80  # Add decimal point
            tm.write(segments)
        else:
            # One digit + decimal + two digits: "9.85"  
            temp_int = int(temp)
            temp_decimal = int((temp - temp_int) * 100)
            if temp_decimal < 10:
                segments = tm.encode_string(str(temp_int) + "0" + str(temp_decimal))
            else:
                segments = tm.encode_string(str(temp_int) + str(temp_decimal))
            # Add decimal point to the first digit
            if len(segments) >= 1:
                segments[0] |= 0x80  # Add decimal point
            tm.write(segments)
    else:
        # Negative temperatures - just show as integer
        tm.show(str(int(temp)))

# Main loop
print("Starting thermistor temperature monitoring...")
print("Raw\tVoltage\tResistance\tTemp")
print("---\t-------\t----------\t----")

while True:
    try:
        # Read ADC
        raw_adc = adc_ntc.read()
        
        # Calculate temperature
        result = calculate_temperature(raw_adc)
        
        if result is None:
            tm.show('Err-')
            time.sleep(2)
            continue
            
        temp_c, voltage, resistance = result
        
        # Print debug info
        print("{}\t{:.3f}V\t{:.0f}Ω\t\t{:.2f}°C".format(
            raw_adc, voltage, resistance, temp_c))
        
        # Display on TM1637
        display_temperature(temp_c)
        
        # Control LEDs based on temperature
        control_temperature_leds(temp_c)
        
        time.sleep(1)
        
    except Exception as e:
        print("Error:", e)
        tm.show('Err-')
        turn_off_all_leds()  # Turn off LEDs on error
        time.sleep(2)

# Alternative: If your thermistor is wired differently (NTC to ground)
def calculate_temperature_alt(adc_reading):
    """Alternative calculation if NTC is connected to ground"""
    voltage = adc_reading * V_SUPPLY / 4095.0
    
    if voltage <= 0.01:
        return None
    if voltage >= V_SUPPLY - 0.01:
        return None
    
    # For NTC connected to ground: R_ntc = R_series * (V_supply - V_out) / V_out
    resistance = SERIES_RESISTOR * (V_SUPPLY - voltage) / voltage
    
    temp_k = 1.0 / ((1.0 / (TEMP_NOMINAL + 273.15)) + 
                    (1.0 / BETA) * math.log(resistance / R_NOMINAL))
    
    temp_c = temp_k - 273.15
    
    return temp_c, voltage, resistance