#!/usr/bin/python3
# Script for reading and parsing smart-meter telegrams
# 2023-07 v1.0
import argparse
import json
import re
import signal
import sys
import time
import serial
import obis_codemap as data

CONNECTED = False
SLEEP_TIME = 1
MAX_TELEGRAM_COUNT = 1
MODE = 'cronjob'

SMART_METER_VERSION = '5.0'
BAUDRATE = 115200
BYTE_SIZE = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOP_BITS = serial.STOPBITS_ONE
PORT = "/dev/ttyUSB0"
SERIAL_CONNECTION = serial.Serial()


def open_connection():
    global CONNECTED
    global SERIAL_CONNECTION

    # Set serial port config
    SERIAL_CONNECTION.baudrate = BAUDRATE
    SERIAL_CONNECTION.bytesize = BYTE_SIZE
    SERIAL_CONNECTION.parity = PARITY
    SERIAL_CONNECTION.stopbits = STOP_BITS
    SERIAL_CONNECTION.xonxoff = 0
    SERIAL_CONNECTION.rtscts = 0
    SERIAL_CONNECTION.timeout = 20
    SERIAL_CONNECTION.port = PORT

    # Open the connection
    try:
        print('Opening connection')
        SERIAL_CONNECTION.open()
        CONNECTED = True
    except:
        CONNECTED = False
        sys.exit(f'Error opening {SERIAL_CONNECTION.name}. Program stopped.')


def close_connection():
    global CONNECTED
    global SERIAL_CONNECTION

    # Close port and show status
    try:
        print('Closing connection')
        CONNECTED = False
        SERIAL_CONNECTION.close()
    except:
        CONNECTED = False
        print('Could not close the serial port.')


def read_telegram():
    global SERIAL_CONNECTION
    error_count = 0

    found_end = False
    telegram_lines = []

    print('Start reading telegram')
    while not found_end:
        telegram_line = ''

        if (error_count > 10):
            return None

        try:
            raw_line = SERIAL_CONNECTION.readline()
        except:
            print(f'Failed to read from serial port {SERIAL_CONNECTION.name}')
            error_count += 1
            continue

        telegram_string = raw_line.decode()
        telegram_line = telegram_string.strip()

        if (telegram_line != ''):
            telegram_lines.append(telegram_line)

        if (telegram_line.startswith('!')):
            found_end = True
            print('Found end of telegram')

    return telegram_lines


def parse_telegram(lines):
    telegram_object = {}

    for line in lines:
        fields = line.strip().replace(")", "").split("(")

        if (line.strip() == "" or line.isspace() or line is None or len(line.strip()) == 0):
            continue

        working_field = fields[0].strip()
        if (working_field == '' or working_field.startswith('!') or working_field.startswith('/')):
            continue

        if fields[0] not in data.obis_codemap:
            print(f'unknown obis code: {working_field}, line: {line}')
            continue

        field_name = data.obis_codemap[working_field]

        # Don't format log messages
        if field_name.endswith("log"):
            telegram_object[field_name] = str(fields[1:])
        else:
            telegram_object[field_name] = format_value(fields[1])

    return telegram_object


def format_value(value):
    # remove leading zeroes for numbers like 000123.123
    value = re.sub("^0*([1-9])", "\\1", value)
    # remove leading zeroes (except the last one) for numbers like 000000.123
    value = re.sub("^0*([0-9]\.)", "\\1", value)
    # remove trailing unit's like "*kWh", "*kW", "*V", "*A", "*m3", "*s",...
    value = re.sub("\*.*", "", value)
    return value


def post_telegrams_to_api(telegrams):
    print('Posting parsed telegrams to api')

    telegram_json = json.dumps(telegrams)
    print(telegram_json)

    # TODO implement API connection


# Main program
signal.signal(signal.SIGINT, signal.default_int_handler)

# Define and parse command line arguments
parser = argparse.ArgumentParser(description='Read and parse smart meter telegrams',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--version', help='The version of of your smartmeter',
                    choices=['4.2', '5.0'], type=str, default=SMART_METER_VERSION)
parser.add_argument('-c', '--count', help='Amount of telegrams to handle in a single run',
                    type=int, default=MAX_TELEGRAM_COUNT)
parser.add_argument('-p', '--port', help='Which port to connect to',
                    type=str, default=PORT)
parser.add_argument('mode', help='The way you will be using this script', choices=[
                    'continuous', 'cronjob'], default=MODE)
args = parser.parse_args()

SMART_METER_VERSION = args.version if args.version else SMART_METER_VERSION
MAX_TELEGRAM_COUNT = args.count if args.count else MAX_TELEGRAM_COUNT
PORT = args.port if args.port else PORT
MODE = args.mode if args.mode else MODE

if (SMART_METER_VERSION == '4.2'):
    print(f'DSMR {args.version} uitlezen')
    BAUDRATE = 115200
    BYTE_SIZE = serial.SEVENBITS
    PARITY = serial.PARITY_EVEN
    STOP_BITS = serial.STOPBITS_ONE
else:
    print(f'ESMR {args.version} uitlezen')
    BAUDRATE = 115200
    BYTE_SIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOP_BITS = serial.STOPBITS_ONE

open_connection()

telegram_list = []
while CONNECTED:
    try:
        if (SERIAL_CONNECTION.inWaiting() > 0):
            lines = read_telegram()
            if (lines is None):
                continue

            parsed_telegram = parse_telegram(lines)
            if (parsed_telegram['dsmr_version'] != ''):
                telegram_list.append(parsed_telegram)

            if (len(telegram_list) == MAX_TELEGRAM_COUNT):
                post_telegrams_to_api(telegram_list)
                telegram_list = []

                if (MODE == 'cronjob'):
                    break

        time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print('User cancelled, stopping program')
        close_connection()
        sys.exit()

close_connection()

print('Program completed')
sys.exit()
