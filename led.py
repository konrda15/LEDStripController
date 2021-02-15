import time
from rpi_ws281x import *
import argparse
import random

# LED strip configuration:
LED_COUNT      = 500      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(180, 18, 800000, 10, False, 255, 0)
    
strip.begin()

colors = [Color(0,255,0), Color(0,0,255), Color(255,0,0), Color(255,255,0), Color(255,0,255), Color(0,255,255)]

pos = 0
change = 1
radius = 5
while True:
	for i in range(strip.numPixels()):
		#strip.setPixelColor(i, Color(random.randint(0,150),random.randint(0,150),random.randint(0,150)))
		#strip.setPixelColor(i, colors[random.randint(0,len(colors)-1)])
		#strip.setPixelColor(i, Color(0,0,0))
		if(abs(i-pos) <= radius):
			strip.setPixelColor(i, Color(255,0,0))
		else:
			strip.setPixelColor(i, Color(0,0,0))
	strip.show()
	pos += change
	if(pos >= 180-radius):
		change = -1
	if(pos <= 0+radius):
		change = 1
	time.sleep(0.01)

