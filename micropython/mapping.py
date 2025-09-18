# MicroPython: Arduino UNO → ESP32 (ACEBOT) pin map + table print

mapping = [
    ("Power", "3.3V", None, "3V3"),
    ("Power", "5V",   None, "5V"),
    ("Power", "GND",  None, "GND"),
    ("Power", "VIN",  None, "VIN"),
    ("Power", "RESET",None, "RST"),

    ("Analog", "A0",  36, "GPIO36"),
    ("Analog", "A1",  39, "GPIO39"),
    ("Analog", "A2",  34, "GPIO34"),
    ("Analog", "A3",  35, "GPIO35"),
    ("Analog", "A4",  32, "GPIO32"),
    ("Analog", "A5",  33, "GPIO33"),

    ("Digital", "D0/RX", 3,  "GPIO3  (UART0 RX)"),
    ("Digital", "D1/TX", 1,  "GPIO1  (UART0 TX)"),
    ("Digital", "D2",    25, "GPIO25"),
    ("Digital", "D3",    26, "GPIO26"),
    ("Digital", "D4",    27, "GPIO27"),
    ("Digital", "D5",    14, "GPIO14"),
    ("Digital", "D6",    12, "GPIO12"),
    ("Digital", "D7",    13, "GPIO13"),
    ("Digital", "D8",     2, "GPIO2"),
    ("Digital", "D9",    15, "GPIO15"),
    ("Digital", "D10",    5, "GPIO5  (SS)"),
    ("Digital", "D11",   23, "GPIO23 (MOSI)"),
    ("Digital", "D12",   19, "GPIO19 (MISO)"),
    ("Digital", "D13",   18, "GPIO18 (SCK)"),

    ("I2C",    "SDA",   21, "GPIO21"),
    ("I2C",    "SCL",   22, "GPIO22"),
    ("Misc",   "AREF", None, "— (ESP32 uses 3.3V ref)"),
    ("Misc",   "IOREF",None, "—"),
]

# Print table
hdr = ("Group", "Arduino", "ESP32 GPIO", "Notes")
w = (8, 10, 11, 24)
print("{:<{}} {:<{}} {:<{}} {:<{}}".format(hdr[0],w[0],hdr[1],w[1],hdr[2],w[2],hdr[3],w[3]))
print("-"*sum(w))
for group, ar, gpio, note in mapping:
    gpio_str = "None" if gpio is None else str(gpio)
    print("{:<{}} {:<{}} {:<{}} {:<{}}".format(group,w[0],ar,w[1],gpio_str,w[2],note,w[3]))

# Optional helper: look up ESP32 GPIO by Arduino label
def esp32_gpio(arduino_label: str):
    for _, ar, gpio, _ in mapping:
        if ar.upper() == arduino_label.upper():
            return gpio
    return None