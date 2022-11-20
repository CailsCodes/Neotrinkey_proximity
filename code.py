
from time import sleep

import board
import touchio
import usb_cdc
from adafruit_apds9960.apds9960 import APDS9960
from neopixel import NeoPixel

colours = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "purple": (255, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "off": (0, 0, 0)
    }

# APDS9960_UP = 0x01    
# PDS9960_DOWN = 0x02  
# APDS9960_LEFT = 0x03  
# APDS9960_RIGHT = 0x04 

on_button = touchio.TouchIn(board.TOUCH1)
off_button = touchio.TouchIn(board.TOUCH2)

gestures = [None, 'up', 'down', 'left', 'right']

apds = APDS9960(board.I2C())
apds.enable_proximity = True
apds.enable_color = True
apds.enable_gesture = True

serial = usb_cdc.data

pixels = NeoPixel(board.NEOPIXEL, 2, auto_write=False)
pixels.brightness = 0.2
pixels.fill(colours['off'])
pixels.show()

stream_headers = "proximity,r,g,b,c,gesture"

def clear_pixels():
    pixels.fill(colours["off"])
    pixels.show()

def blink(colour="green", n=3):
    clear_pixels()
    for _ in range(n):
        pixels.fill(colours[colour])
        pixels.show()
        sleep(0.5)
        clear_pixels()
        sleep(0.5)

def buffer_cycle(colour="blue"):
    for led in range(2):
        pixels.fill(colours["off"])
        pixels[led] = colours[colour]
        pixels.show()
        sleep(0.2)
    clear_pixels()

def wait_for_connection():
    while not serial.connected:
        buffer_cycle()
    blink("green", n=1)
    serial.write(b'connected')

def hold_button(button, colour="off"):
    state = []
    clear_pixels()
    for i in range(2):
        if button.value:
            state.append(True)
            pixels[i] = colours[colour]
            pixels.show()
        else:
            break
        sleep(1)
    clear_pixels()
    return True if (len(state) == 2) else False

def get_colour_AL():
    r,g,b,c = apds.color_data
    return (r,g,b), c

def get_proximity():
    prox = apds.proximity
    # can introduce conversion if desired
    return prox

def get_gesture():
    gest = gestures[apds.gesture()]
    return gest

def send_data(prox, colour, light, gesture):
    col = ','.join([str(c) for c in colour])
    text = ','.join([str(prox),str(col),str(light),str(gesture)])
    msg = bytearray(text, 'utf-8')
    serial.write(msg)
    blink(n=1)

def main():
    clear_pixels()
    wait_for_connection()
    while serial.connected:
        colour, light = get_colour_AL()
        proximity = get_proximity()
        gesture = get_gesture()
        send_data(proximity, colour, light, gesture)
        sleep(3)
    main()

        
if __name__ == '__main__':
    main()
