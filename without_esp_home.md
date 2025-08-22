python3 -m pip install --user esptool mpremote

# optional: wipe first time
python3 -m esptool --port /dev/ttyUSB0 erase_flash
# write firmware at 0x1000
python3 -m esptool --port /dev/ttyUSB0 --baud 460800 write_flash 0x1000 /path/to/ESP32_GENERIC-*.bin

# open REPL to confirm
mpremote connect /dev/ttyUSB0 repl

# run a local file one-off
mpremote connect /dev/ttyUSB0 run ./blink.py

# copy to device filesystem
mpremote connect /dev/ttyUSB0 fs put ./main.py
