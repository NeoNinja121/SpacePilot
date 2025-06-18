import board
import neopixel
import time

# One RGB LED on pin 6
pixel = neopixel.NeoPixel(board.D6, 1)

# Flash red
pixel[0] = (255, 0, 0)
time.sleep(1)

# Flash green
pixel[0] = (0, 255, 0)
time.sleep(1)

# Flash blue
pixel[0] = (0, 0, 255)
time.sleep(1)

# Turn off
pixel[0] = (0, 0, 0)
