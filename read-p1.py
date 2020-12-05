#!/usr/bin/python3
# Script for reading and parsing the DSMR 5.0 smart-meter telegrams
import serial
import sys

version = '1.0'
print("DSMR 5.0 P1 uitlezen",  version)

# Set serial port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize = serial.SEVENBITS
ser.parity = serial.PARITY_EVEN
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 20
ser.port = "/dev/ttyUSB0"

# Open the connection
try:
    ser.open()
except:
    sys.exit("Error opening %s. Program stopped." % ser.name)

p1_counter = 0

# Print each telegram line
while p1_counter < 26:
    telegram_line = ''

    try:
        raw_line = ser.read()
    except:
        sys.exit("Could not read from serial port %s. Program stopped." % ser.name)

    telegram_string = str(raw_line)
    telegram_line = telegram_string.strip()

    print(telegram_line)
    p1_counter += 1

# Close port and show status
try:
    ser.close()
except:
    sys.exit("Oops %s. Program closed. Could not close the serial port." % ser.name)
