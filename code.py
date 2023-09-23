# [DX] 2023
# Example code for using an OV7670 parallel camera module with a Raspberry Pi Pico with CircuitPython
# takes a picture and saves it in the SD card

import board
import busio
import time
import digitalio
import storage
import sdcardio

from displayio import (
    Bitmap,
    Group,
    Palette,
    TileGrid,
    ColorConverter,
    Colorspace,
)

from adafruit_ov7670 import (
    OV7670,
    OV7670_SIZE_DIV2,
    OV7670_COLOR_RGB,
    OV7670_COLOR_YUV,
    OV7670_TEST_PATTERN_COLOR_BAR,
    OV7670_NIGHT_MODE_2,
)

with digitalio.DigitalInOut(board.GP22) as shutdown:
    shutdown.switch_to_output(True)
    time.sleep(0.001)
    bus = busio.I2C(board.GP9, board.GP8) # scl sda

cam = OV7670(
    bus,
    data_pins=[
        board.GP12, #D0
        board.GP13, #D1
        board.GP14, #D2
        board.GP15, #D3
        board.GP16, #D4
        board.GP17, #D5
        board.GP18, #D6
        board.GP19, #D7
    ],
    clock=board.GP11,
    vsync=board.GP7,
    href=board.GP21,
    mclk=board.GP20,
    shutdown=board.GP22,
    reset=board.GP10
)
 
cam.size = OV7670_SIZE_DIV2 # 340 x 240
cam.colorspace = OV7670_COLOR_RGB # RGB565 colorspace
#cam.colorspace = OV7670_COLOR_RGB # Uncomment to use YUV colorspace
# cam.flip_x = False # Uncomment to flip X axis
# cam.flip_y = True  # Uncomment to flip Y axis
#cam.test_pattern = OV7670_TEST_PATTERN_COLOR_BAR # Uncomment to see the camera's bar test pattern 


# Set up SD card
sck = board.GP2
si = board.GP3
so = board.GP4
cs = board.GP5
spi = busio.SPI(sck, si, so)
sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

buf = Bitmap(cam.width, cam.height, 65535)
IMAGE_FILE = "/sd/image" # Image file on the SD card

with open(IMAGE_FILE, "wb") as outfile: # Take a picture and save it to the SD card
    cam.capture(buf)
    buf.dirty()
    outfile.write(buf)

print("done idk")