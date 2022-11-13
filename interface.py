import serial
from sys import platform
from time import sleep

platform_to_port = {
    "linux" : '/dev/ttyACM1',
    "darwin" : '/dev/tty.usbmodem14103',
    "win32" : 'COM7'
    }

try:
    usb_port = platform_to_port[platform]
except IndexError:
    raise OSError(f"OS {platform} not supported")

ser = serial.Serial(usb_port)

attempts = 0

while attempts <=3:
    if ser.in_waiting != 0:
        msg = ser.read_all().decode('utf-8')
        print(msg)
        if attempts != 0:
            attempts = 0
    else:
        attempts += 1

    sleep(4)
