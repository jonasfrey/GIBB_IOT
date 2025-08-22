arduino-cli core install arduino:avr
arduino-cli board list                      # find your /dev/ttyUSB* or /dev/ttyACM*
arduino-cli sketch new BlinkUno
# put the sketch above into BlinkUno/BlinkUno.ino
arduino-cli compile --fqbn arduino:avr:uno BlinkUno
arduino-cli upload  -p /dev/ttyUSB0 --fqbn arduino:avr:uno BlinkUno