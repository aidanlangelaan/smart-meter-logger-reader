#!/usr/bin/python3
# Script for reading and parsing the DSMR 5.0 smart-meter telegrams
# 2020-12 v1.0
import json
import re
import serial
import signal
import sys
import time
import obis_codemap as data

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
        print('Completed reading stream')
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

        telegram_string = raw_line.decode()
        telegram_line = telegram_string.strip()
        telegram_lines.append(telegram_line)

        if (telegram_line.startswith('!')):
            found_end = True
            print('Found end of telegram')

    return telegram_lines


def parse_telegram(telegram_lines):
    telegram_object = {}

    for line in telegram_lines:
        fields = line.replace(")", "").split("(")
        # Check for unknown obis code
        if fields[0] not in data.obis_codemap:
            print('unknown obis code: %s' % fields[0])
            continue

        field_name = data.obis_codemap[fields[0]]

        # Don't format log messages
        if field_name.endswith("log"):
            telegram_object[field_name] = str(fields[1:])
        else:
            telegram_object[field_name] = format_value(fields[1])

    return telegram_object
    # return json.dumps(telegram_object)


def format_value(value):
    # remove leading zeroes for numbers like 000123.123
    value = re.sub("^0*([1-9])", "\\1", value)
    # remove leading zeroes (except the last one) for numbers like 000000.123
    value = re.sub("^0*([0-9]\.)", "\\1", value)
    # remove trailing unit's like "*kWh", "*kW", "*V", "*A", "*m3", "*s",...
    value = re.sub("\*.*", "", value)
    return value


def post_telegrams_to_api(telegram_list):
    telegram_json = json.dumps(telegram_list)
    print('posting to api: %s' % telegram_json)

    # TODO implement API connection


# Main program
signal.signal(signal.SIGINT, signal.default_int_handler)

open_connection()

while connected:
    telegram_list = []

    try:
        if (ser.inWaiting() > 0):
            telegram_lines = read_telegram(ser)
            telegram_object = parse_telegram(telegram_lines)

            telegram_list.append(telegram_object)

            if (telegram_list.count == 10):
                print('post to api %i telegrams' % telegram_list.count)
                telegram_list = []

        time.sleep(1)
    except KeyboardInterrupt:
        print('User cancelled, stopping program')
        close_connection()
        sys.exit()

close_connection()
print('Program completed')
sys.exit()
