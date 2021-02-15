import time
from rpi_ws281x import *
import argparse
import random
import threading
import colorsys

TICK_LENGTH = 0.001
STRIP_LENGTH = 180
STRIP_MAX = 180
STRIP_START = 0


def hsv_rgb(h,s,v):
    c = tuple(round(j*255) for j in  colorsys.hsv_to_rgb(h/360,s/100,v/100))
    return [c[0], c[1], c[2]]

def clear_strip(e, strip_arr, ch_settings):
	for i in range(STRIP_LENGTH):
		strip_arr[i] = (0,0,0)
		
def one_color(e, strip_arr, ch_settings):
	print("one color")
	while True:
		if e.isSet():
			return
		for i in range(STRIP_LENGTH):
			strip_arr[i] = (255,60,0)

		time.sleep(TICK_LENGTH*100)
        
        
def two_colors(e, strip_arr, ch_settings):
	print("two colors")
	while True:
		if e.isSet():
			return
		half = int(STRIP_LENGTH/2)-1
		for i in range(0, half):
			strip_arr[i] = (0,0,255)
		for i in range(half, STRIP_LENGTH):
			strip_arr[i] = (150,255,150)
		time.sleep(TICK_LENGTH*100)
        
def three_colors(e, strip_arr, ch_settings):
	print("three colors")
	while True:
		if e.isSet():
			return
		third = int(STRIP_LENGTH/3)-1
		twothirds = third + int(STRIP_LENGTH/3)

		for i in range(0, third):
			strip_arr[i] = (0,0,255)
		for i in range(third+1, twothirds):
			strip_arr[i] = (0,255,0)
		for i in range(twothirds+1, STRIP_LENGTH):
			strip_arr[i] = (255,0,0)
		time.sleep(TICK_LENGTH*100)

def animation1(e, strip_arr, ch_settings):
	print("animation1")
	pos = 0
	change = 1
	radius = 5
	while True:
		if e.isSet():
			return
			
		for i in range(STRIP_LENGTH):
			if(abs(i-pos) <= radius):
				strip_arr[i] = (255,0,0)
			else:
				strip_arr[i] = (0,0,0)

		pos += change
		if(pos >= STRIP_MAX-radius):
			change = -1
		if(pos <= STRIP_START+radius):
			change = 1
			
		time.sleep(TICK_LENGTH*10)

def animation2(e, strip_arr, ch_settings):
	print("animation2")

	radius = 5
	pos = radius
	change = 1

	while True:
		if e.isSet():
			return
			
		for i in range(STRIP_LENGTH):
			if(abs(i-pos) <= radius or abs(i-pos) > STRIP_MAX-radius):
				strip_arr[i] = (255,0,0)
			else:
				strip_arr[i] = (0,0,0)

		pos += change
		if(pos >= STRIP_MAX):
			pos = 0

			
		time.sleep(TICK_LENGTH*10)

def rainbow(e, strip_arr, ch_settings):
	print("rainbow")

	staggering = [(1), (30), (60)]

	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)
		   
		for i in range(STRIP_LENGTH):
			hue = 360 * (i/STRIP_MAX)
			hue = hue - hue%staggering[var_index]
			strip_arr[i] = hsv_rgb(hue, 100, 100)
			
		time.sleep(TICK_LENGTH*100)


def rainbow_animation(e, strip_arr, ch_settings):
	print("rainbow_animation")

	staggering = [(1), (30), (60)]

	pos = 0
	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)

		for i in range(STRIP_LENGTH):
			hue = 360 * (i/STRIP_MAX)
			hue = hue - hue%staggering[var_index]
			strip_arr[(i+pos)%STRIP_MAX] = hsv_rgb(hue, 100, 100)
			

		pos += 1
		time.sleep(TICK_LENGTH*10)
        
def rand_colors(e, strip_arr, ch_settings):
	print("rand_colors")
	ranges = [(0,360),(0,60),(40,120),(80,260),(240,360),(300,420),(300,500)]

	while True:
		if e.isSet():
			return

		for i in range(STRIP_LENGTH):
			var_index = ch_settings.variation%len(ranges)
			hue = random.randint(ranges[var_index][0], ranges[var_index][1])%360
			strip_arr[i] = hsv_rgb(hue, 100, 100)

		time.sleep(TICK_LENGTH*100)

def rainbow_fade(e, strip_arr, ch_settings):
	print("rainbow_fade")

	staggering = [(1), (30), (60)]

	pos = 0
	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)

		hue = pos
		hue = hue - hue%staggering[var_index]
		for i in range(STRIP_LENGTH):
			strip_arr[i] = hsv_rgb(hue, 100, 100)

		pos = (pos+1)%360
		time.sleep(TICK_LENGTH*20)
		
def alternating(e, strip_arr, ch_settings):
	print("alternating")

	staggering = [(2), (4), (6), (10), (20), (60), (STRIP_LENGTH)]
	
	
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i%(STRIP_LENGTH/(staggering[var_index]/2)) < STRIP_LENGTH/staggering[var_index]:
				strip_arr[i] = (255,255,255)
			else:
				strip_arr[i] = (0,0,0)
		time.sleep(TICK_LENGTH*100)


def alternating_blinking(e, strip_arr, ch_settings):
	print("alternating_blinking")

	staggering = [(2), (4), (6), (10), (20), (60), (STRIP_LENGTH)]
	
	alternatives = [(0,0,0), (255,255,255)]
	
	pos = 0
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i%(STRIP_LENGTH/(staggering[var_index]/2)) < STRIP_LENGTH/staggering[var_index]:
				strip_arr[i] = alternatives[pos]
			else:
				strip_arr[i] = alternatives[(pos+1)%2]
				
		pos = (pos+1)%2
		time.sleep(TICK_LENGTH*500)

def alternating_travel(e, strip_arr, ch_settings):
	print("alternating_travel")

	staggering = [(2), (4), (6), (10), (20), (60)]
	
	alternatives = [(0,0,0), (255,255,255)]
	
	pos = 0
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i%(STRIP_LENGTH/(staggering[var_index]/2)) < STRIP_LENGTH/staggering[var_index]:
				strip_arr[(i+pos)%STRIP_LENGTH] = alternatives[0]
			else:
				strip_arr[(i+pos)%STRIP_LENGTH] = alternatives[1]
		
		pos = (pos+1)%STRIP_LENGTH
		
		time.sleep(TICK_LENGTH*30)
