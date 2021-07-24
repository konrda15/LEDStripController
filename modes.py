import time
from rpi_ws281x import *
import argparse
import random
import threading
import colorsys
import logging
from globalsettings import STANDARD_TICK_LENGTH, STRIP_LENGTH, STRIP_SEGMENTS

#STANDARD_TICK_LENGTH = 0.001
#STRIP_LENGTH = 144

def normal(e, mode_arr, mode_settings):
	logging.info("new mode: normal")
	while True:
		if e.isSet():
			return
		brightness = mode_settings.brightness
		for i in range(STRIP_LENGTH):
			mode_arr[i] = (brightness, brightness, brightness)
		time.sleep(STANDARD_TICK_LENGTH*500)

def fade(e, mode_arr, mode_settings):
	logging.info("new mode: fade")
	brightness = mode_settings.brightness
	
	fade = 1
	direction = -1
	base_change = 0.005
	change_per_tick = 0.01
	
	while True:
		if e.isSet():
			return

		change_per_tick = base_change+10*fade*base_change
		fade += change_per_tick*direction
		current_b = fade*brightness
		if current_b < 0:
			current_b = 0
		elif current_b > 1:
			current_b = 1
			
		for i in range(STRIP_LENGTH):
			mode_arr[i] = (current_b,current_b,current_b)
			
		
		if(fade <= 0):
			direction = abs(direction)
		elif(fade >= 1):
			direction = abs(direction) * (-1)
			
		time.sleep(STANDARD_TICK_LENGTH*40)


def blinking(e, mode_arr, mode_settings):
	logging.info("new mode: blinking")
	brightness = mode_settings.brightness
	
	on_off = 0 
	
	while True:
		on_off = (on_off+1)%2
		current_b = on_off*brightness
		if e.isSet():
			return
		for i in range(STRIP_LENGTH):
			mode_arr[i] = (current_b,current_b,current_b)
		
		time.sleep(STANDARD_TICK_LENGTH*500)

def fast_blinking(e, mode_arr, mode_settings):
	logging.info("new mode: fast_blinking")
	brightness = mode_settings.brightness
	
	on_off = 0 
	
	while True:
		on_off = (on_off+1)%2
		current_b = on_off*brightness
		if e.isSet():
			return
		for i in range(STRIP_LENGTH):
			mode_arr[i] = (current_b,current_b,current_b)
		
		time.sleep(STANDARD_TICK_LENGTH*150)

def strobe(e, mode_arr, mode_settings):
	logging.info("new mode: strobe")
	brightness = mode_settings.brightness
	
	on_off = 0 
	
	while True:
		on_off = (on_off+1)%50
		if on_off == 0:
			current_b = brightness
		else:
			current_b = 0
			
		if e.isSet():
			return
		for i in range(STRIP_LENGTH):
			mode_arr[i] = (current_b,current_b,current_b)
		
		time.sleep(STANDARD_TICK_LENGTH*25)

def adv_fade(e, mode_arr, mode_settings):
	logging.info("new mode: adv_fade")
	brightness = mode_settings.brightness
	
	fade = 1
	direction = -1
	change_factor = 1/10
	constant_amount = 0.001
	
	while True:
		if e.isSet():
			return

		fade += fade*change_factor*direction+constant_amount*direction
		fade = round(fade, 3)
		
		if(fade <= 0):
			direction = 1
			fade = 0
		elif(fade >= 1):
			direction = -1
			fade = 1
		
		current_b = fade*brightness
		
		for i in range(STRIP_LENGTH):
			mode_arr[i] = (current_b,current_b,current_b)
			

		time.sleep(STANDARD_TICK_LENGTH*40)
