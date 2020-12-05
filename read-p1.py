#!/usr/bin/python3
# Script for reading and parsing the DSMR 5.0 smart-meter telegrams
# 2020-12 v1.0
import serial
import signal
import sys
import time
import obis_codemap

print("DSMR 5.0 P1 uitlezen")
connected = False
ser = serial.Serial()


def open_connection():
    global connected
    global ser

    # Set serial port config
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
        print('Opening connection')
        ser.open()
        connected = True
    except:
        connected = False
        sys.exit('Error opening %s. Program stopped.' % ser.name)


def close_connection():
    global connected
    global ser

    # Close port and show status
    try:
        print('Completed reading telegram')
        connected = False
        ser.close()
    except:
        connected = False
        print('Could not close the serial port.')


def read_telegram(ser):
    found_end = False
    telegram_lines = []

    print('Start reading lines')
    while not found_end:
        telegram_line = ''

        try:
            raw_line = ser.readline()
        except:
            sys.exit(
                'Could not read from serial port %s. Program stopped.' % ser.name)

        telegram_string = str(raw_line)
        telegram_line = telegram_string.strip()
        telegram_lines.append(telegram_line)

        print(telegram_line)

        if (telegram_line.startswith('!')):
            found_end = True

    return telegram_lines


def parse_telegram(telegram_lines):
    for line in telegram_lines:
        fields = line.replace(")", "").split("(")

        # Check for unknown obis code
        if fields[0] not in obis_codemap:
            print('unknown obis code: %' % fields[0])
            continue

        field_name = obis_codemap[fields[0]]

        print('found field name %' % field_name)


# Main program
signal.signal(signal.SIGINT, signal.default_int_handler)

open_connection()

while connected:
    try:
        if (ser.inWaiting() > 0):
            telegram_lines = read_telegram(ser)

            # Parse lines to JSON
            telegram_json = parse_telegram(telegram_lines)

            # Post to API

        time.sleep(1)
    except KeyboardInterrupt:
        print('User cancelled, stopping program')
        close_connection()
        sys.exit()

close_connection()
print('Program completed')
sys.exit()
