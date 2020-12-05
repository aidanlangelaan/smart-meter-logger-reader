#!/usr/bin/python3
# Script for reading and parsing the DSMR 5.0 smart-meter telegrams
# 2020-12 v1.0
import serial
import signal
import sys
import time

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


def read_telegram(ser):
    p1_counter = 0

    print('Start reading lines')
    while p1_counter < 26:
        telegram_line = ''

        try:
            raw_line = ser.readline()
        except:
            sys.exit(
                'Could not read from serial port %s. Program stopped.' % ser.name)

        telegram_string = str(raw_line)
        telegram_line = telegram_string.strip()

        print(telegram_line)
        p1_counter += 1


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


# Main program
signal.signal(signal.SIGINT, signal.default_int_handler)

open_connection()

while connected:
    try:
        if (ser.inWaiting() > 0):
            read_telegram(ser)
        time.sleep(1)
    except KeyboardInterrupt:
        print('User cancelled, stopping program')
        close_connection()
        sys.exit()

close_connection()
print('Program completed')
sys.exit()
