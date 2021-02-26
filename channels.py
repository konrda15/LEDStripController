import time
from rpi_ws281x import *
import argparse
import random
import threading
import colorsys
import logging
from colors import *


STRIP_LENGTH = 180
STRIP_MAX = 180
STRIP_START = 0


def hsv_rgb(h,s,v):
    c = tuple(round(j*255) for j in  colorsys.hsv_to_rgb(h/360,s/100,v/100))
    return [c[0], c[1], c[2]]

def clear_strip(e, strip_arr, settings):
	logging.info("started channel clear_strip")
	for i in range(STRIP_LENGTH):
		strip_arr[i] = (0,0,0)

def getColorIndices(settings, default_c1, default_c2, default_c3):
	c1 = settings.color1
	if c1 == 0:
		c1 = default_c1
	c2 = settings.color2
	if c2 == 0:
		c2 = default_c2	
	c3 = settings.color3
	if c3 == 0:
		c3 = default_c3
	return (c1,c2,c3)

def one_color(e, strip_arr, settings):
	logging.info("started channel one_color")
	
	default_c1 = 2
	
	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, 0, 0)
			
		for i in range(STRIP_LENGTH):
			strip_arr[i] = color_dict[c_indices[0]]

		time.sleep(settings.tick_length*100)
        
        
def two_colors(e, strip_arr, settings):
	logging.info("started channel two_colors")
	
	default_c1 = 3
	default_c2 = 11
	
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
			
		half = int(STRIP_LENGTH/2)-1
		for i in range(0, half):
			strip_arr[i] = color_dict[c_indices[1]]
		for i in range(half, STRIP_LENGTH):
			strip_arr[i] = color_dict[c_indices[0]]
		time.sleep(settings.tick_length*100)
        
def three_colors(e, strip_arr, settings):
	logging.info("started channel three_colors")
	
	default_c1 = 3
	default_c2 = 11
	default_c3 = 19
	
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, default_c3)
			
		third = int(STRIP_LENGTH/3)-1
		twothirds = third + int(STRIP_LENGTH/3)

		for i in range(0, third):
			strip_arr[i] = color_dict[c_indices[2]]
		for i in range(third, twothirds):
			strip_arr[i] = color_dict[c_indices[1]]
		for i in range(twothirds, STRIP_LENGTH):
			strip_arr[i] = color_dict[c_indices[0]]
		time.sleep(settings.tick_length*100)

def ping_pong(e, strip_arr, settings):
	logging.info("started channel ping_pong")
	
	default_c1 = 3
	default_c2 = 1
	
	point_length = [1,2,3,4,5,6,8,10,15,20,30,40,50,60,90]
	
	pos = 0
	change = 1
	
	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
		
		var_index = settings.variation%len(point_length)
		p_length = point_length[var_index]
		
		for i in range(STRIP_LENGTH):
			strip_arr[i] = color_dict[c_indices[1]]
		for i in range(p_length):
			if pos+i >= STRIP_LENGTH:
				strip_arr[STRIP_LENGTH-i-1] = color_dict[c_indices[0]]
			else:
				strip_arr[pos+i] = color_dict[c_indices[0]]

		pos += change
		if(pos >= STRIP_LENGTH-p_length):
			change = -1
		if(pos == 0):
			change = 1
			
		time.sleep(settings.tick_length*10)

def travelling(e, strip_arr, settings):
	logging.info("started channel travelling")
	
	default_c1 = 3
	default_c2 = 1

	point_length = [1,2,3,4,5,6,8,10,15,20,30,40,50,60,90]
	
	change = 1
	pos = 0
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
		
		var_index = settings.variation%len(point_length)
		p_length = point_length[var_index]
			
		for i in range(STRIP_LENGTH):
			strip_arr[i] = color_dict[c_indices[1]]
		for i in range(p_length):
			if pos+i >= STRIP_LENGTH:
				strip_arr[i-(STRIP_LENGTH-pos)] = color_dict[c_indices[0]]
			else:
				strip_arr[pos+i] = color_dict[c_indices[0]]

		pos += change
		if(pos >= STRIP_LENGTH):
			pos = 0

			
		time.sleep(settings.tick_length*10)

def rainbow(e, strip_arr, settings):
	logging.info("started channel rainbow")

	staggering = [(1), (30), (60)]

	while True:
		if e.isSet():
			return

		var_index = settings.variation%len(staggering)
		   
		for i in range(STRIP_LENGTH):
			hue = 360 * (i/STRIP_MAX)
			hue = hue - hue%staggering[var_index]
			strip_arr[i] = hsv_rgb(hue, 100, 100)
			
		time.sleep(settings.tick_length*100)


def rainbow_animation(e, strip_arr, settings):
	logging.info("started channel rainbow_animation")

	staggering = [(1), (30), (60)]

	pos = 0
	while True:
		if e.isSet():
			return

		var_index = settings.variation%len(staggering)

		for i in range(STRIP_LENGTH):
			hue = 360 * (i/STRIP_MAX)
			hue = hue - hue%staggering[var_index]
			strip_arr[(i+pos)%STRIP_MAX] = hsv_rgb(hue, 100, 100)
			

		pos += 1
		time.sleep(settings.tick_length*10)
        
def rand_colors(e, strip_arr, settings):
	logging.info("started channel rand_colors")
	ranges = [(0,360),(0,60),(40,120),(80,260),(240,360),(300,420),(300,500)]

	while True:
		if e.isSet():
			return

		for i in range(STRIP_LENGTH):
			var_index = settings.variation%len(ranges)
			hue = random.randint(ranges[var_index][0], ranges[var_index][1])%360
			strip_arr[i] = hsv_rgb(hue, 100, 100)

		time.sleep(settings.tick_length*100)

def rainbow_fade(e, strip_arr, settings):
	logging.info("started channel rainbow_fade")

	staggering = [(1), (30), (60)]

	pos = 0
	while True:
		if e.isSet():
			return

		var_index = settings.variation%len(staggering)

		hue = pos
		hue = hue - hue%staggering[var_index]
		for i in range(STRIP_LENGTH):
			strip_arr[i] = hsv_rgb(hue, 100, 100)

		pos = (pos+1)%360
		time.sleep(settings.tick_length*20)
		
def alternating(e, strip_arr, settings):
	logging.info("started channel alternating")

	default_c1 = 2
	default_c2 = 1

	staggering = [(2), (4), (6), (10), (20), (60), (STRIP_LENGTH)]
	
	
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
			
		var_index = settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i%(STRIP_LENGTH/(staggering[var_index]/2)) < STRIP_LENGTH/staggering[var_index]:
				strip_arr[i] = color_dict[c_indices[0]]
			else:
				strip_arr[i] = color_dict[c_indices[1]]
		time.sleep(settings.tick_length*100)


def alternating_blinking(e, strip_arr, settings):
	logging.info("started channel alternating_blinking")

	staggering = [(2), (4), (6), (10), (20), (60), (STRIP_LENGTH)]
	
	default_c1 = 2
	default_c2 = 1
	
	
	pos = 0
	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)

		var_index = settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i%(STRIP_LENGTH/(staggering[var_index]/2)) < STRIP_LENGTH/staggering[var_index]:
				strip_arr[i] = color_dict[c_indices[pos]]
			else:
				strip_arr[i] = color_dict[c_indices[(pos+1)%2]]
				
		pos = (pos+1)%2
		time.sleep(settings.tick_length*500)

def alternating_travel(e, strip_arr, settings):
	logging.info("started channel alternating_travel")

	staggering = [(2), (4), (6), (10), (20), (60)]
	
	default_c1 = 2
	default_c2 = 1
	
	pos = 0
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
			
		var_index = settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i%(STRIP_LENGTH/(staggering[var_index]/2)) < STRIP_LENGTH/staggering[var_index]:
				strip_arr[(i+pos)%STRIP_LENGTH] = color_dict[c_indices[0]]
			else:
				strip_arr[(i+pos)%STRIP_LENGTH] = color_dict[c_indices[1]]
		
		pos = (pos+1)%STRIP_LENGTH
		
		time.sleep(settings.tick_length*30)

def rolling_ball(e, strip_arr, settings):
	logging.info("started channel rolling_ball")
	
	default_c1 = 2
	
	random.seed()
	center_left = int((STRIP_LENGTH/2)-1)
	center_right = int((STRIP_LENGTH/2))
	
	ball_size = 3
	ball_radius = int((ball_size-1)/2)
	
	min_pos = 0+ball_radius
	max_pos = STRIP_LENGTH - 1 - ball_radius
	
	while True:
		if e.isSet():
				return
				
		speed = random.randint(100, 600) #leds per second
		decel = random.uniform(0.3,0.5) #per second
		direction = random.randint(0,1)
		if direction == 0:
			direction = -1
		pos = random.randint(0+ball_radius, STRIP_LENGTH-ball_radius-1)
		
		while True:
			if e.isSet():
				return
			
			c_indices = getColorIndices(settings, default_c1, 0, 0)
			
			pos += (speed/100)*direction
			pos_int = int(pos)
			
			if pos_int < min_pos:
				pos = min_pos + abs(pos-min_pos) 
				direction = 1
			elif pos_int >= max_pos:
				pos = max_pos - abs(pos-max_pos)
				direction = -1
			
			pos_int = int(pos)
			
			for i in range(STRIP_LENGTH):
				strip_arr[i] = (0,0,0)

			for i in range(pos_int - ball_radius, pos_int+ball_radius+1):
				strip_arr[i] = color_dict[c_indices[0]]
			strip_arr[center_left] = (255,0,0)
			strip_arr[center_right] = (255,0,0)
			
			speed = speed - speed * (decel/100)
			if speed <= 0.5:
				break
			
			time.sleep(settings.tick_length*10)
		pos_int = int(pos)
		if pos_int < center_right:
			strip_arr[center_left] = (0,255,0)
		else:
			strip_arr[center_right] = (0,255,0)
		
		for i in range(10): #mecessary to achieve quick return when requested
			if e.isSet():
				return
			time.sleep(settings.tick_length*500)

def counter(e, strip_arr, settings):
	logging.info("started channel counter")
	
	default_c1 = 2
	
	count = 0
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, 0, 0)
			
		for i in range(STRIP_LENGTH):
			strip_arr[i] = (0,0,0)
		
		temp_count = count
		index = 0	
		while temp_count > 0:
			if temp_count%2 == 1:
				strip_arr[index] = color_dict[c_indices[0]]
			index += 1
			temp_count >>= 1
			
		count += 1
		time.sleep(settings.tick_length*200)

#deprecated
def rainbow_colors(e, strip_arr, settings):
	logging.info("started channel rainbow_colors")

	hue_range = [(160,240),(100,240), (0,30)]

	pos = 0
	while True:
		if e.isSet():
			return

		var_index = settings.variation%len(hue_range)
		
		half = int(STRIP_LENGTH/2)
		lower_lim = hue_range[var_index][0]
		upper_lim = hue_range[var_index][1]
		range_len = abs(upper_lim - lower_lim)
		
		for i in range(0,half):
			hue = lower_lim + (range_len * (i/half))
			strip_arr[(i+pos)%STRIP_MAX] = hsv_rgb(hue, 100, 100)
		
		for i in range(half, STRIP_MAX):
			hue = upper_lim - (range_len * ((i-half)/half))
			strip_arr[(i+pos)%STRIP_MAX] = hsv_rgb(hue, 100, 100)	

		pos += 1
		time.sleep(settings.tick_length*10)

def rainbow_center(e, strip_arr, settings):
	logging.info("started channel rainbow_center")

	staggering = [(1), (30), (60)]

	center_val = 0
	half = int(STRIP_LENGTH/2)
	center_left = int((STRIP_LENGTH/2)-1)
	center_right = int((STRIP_LENGTH/2))
	
	while True:
		if e.isSet():
			return

		var_index = settings.variation%len(staggering)
		for i in range(center_left, 0, -1):
			hue = center_val + 360 * ((center_left-i)/(half))
			hue = hue%360
			hue = hue - hue%staggering[var_index]
			strip_arr[i] = hsv_rgb(hue, 100, 100)
			
		for i in range(center_right, STRIP_MAX):
			hue = center_val + 360 * ((i-center_right)/(half))
			hue = hue%360
			hue = hue - hue%staggering[var_index]
			strip_arr[i] = hsv_rgb(hue, 100, 100)
			

		center_val = (center_val-1)%360
		time.sleep(settings.tick_length*10)

def color_transition(e, strip_arr, settings):
	logging.info("started channel color_transition")
	
	parts = [1,2,3,4,6,8,10,20,30]
	default_c1 = 3
	default_c2 = 11
	
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
			
		var_index = settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		color_diff = (color2[0]-color1[0], color2[1]-color1[1], color2[2]-color1[2]) 
		
		for i in range(parts[var_index]):
			for j in range(part_len):
				index = i*part_len+j
				perc = j/part_len
				strip_arr[index] = (int(color1[0]+color_diff[0]*perc), int(color1[1]+color_diff[1]*perc), int(color1[2]+color_diff[2]*perc))
				


		time.sleep(settings.tick_length*100)

def color_transition_full(e, strip_arr, settings):
	logging.info("started channel color_transition_full")
	
	parts = [1,2,3,4,6,8,10,20,30]
	default_c1 = 3
	default_c2 = 11
	
	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
			
		var_index = settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		color_diff = (color2[0]-color1[0], color2[1]-color1[1], color2[2]-color1[2]) 
		
		for i in range(parts[var_index]):
			for j in range(part_len):
				index = i*part_len+j
				perc = j/part_len
				
				if i%2 == 0:
					strip_arr[index] = (int(color2[0]-color_diff[0]*perc), int(color2[1]-color_diff[1]*perc), int(color2[2]-color_diff[2]*perc))
				else:
					strip_arr[index] = (int(color1[0]+color_diff[0]*perc), int(color1[1]+color_diff[1]*perc), int(color1[2]+color_diff[2]*perc))
				


		time.sleep(settings.tick_length*100)

def color_transition_anim(e, strip_arr, settings):
	logging.info("started channel color_transition_anim")
	
	parts = [1,2,3,4,6,8,10,20,30]
	
	default_c1 = 3
	default_c2 = 11
	
	pos = 0
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
			
		var_index = settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		color_diff = (color2[0]-color1[0], color2[1]-color1[1], color2[2]-color1[2]) 
		
		for i in range(parts[var_index]):
			for j in range(part_len):
				index = i*part_len+j
				perc = j/part_len
				strip_arr[(index+pos)%STRIP_LENGTH] = (int(color1[0]+color_diff[0]*perc), int(color1[1]+color_diff[1]*perc), int(color1[2]+color_diff[2]*perc))
				
		pos += 1

		time.sleep(settings.tick_length*10)
		
def color_transition_full_anim(e, strip_arr, settings):
	logging.info("started channel color_transition_full_anim")
	
	parts = [2,4,6,8,10,20,30]
	
	default_c1 = 3
	default_c2 = 11
	
	pos = 0
	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
			
		var_index = settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		color_diff = (color2[0]-color1[0], color2[1]-color1[1], color2[2]-color1[2]) 

		for i in range(parts[var_index]):
			for j in range(part_len):
				index = i*part_len+j
				perc = j/part_len

				if i%2 == 0:
					strip_arr[(index+pos)%STRIP_LENGTH] = (int(color2[0]-color_diff[0]*perc), int(color2[1]-color_diff[1]*perc), int(color2[2]-color_diff[2]*perc))
				else:
					strip_arr[(index+pos)%STRIP_LENGTH] = (int(color1[0]+color_diff[0]*perc), int(color1[1]+color_diff[1]*perc), int(color1[2]+color_diff[2]*perc))
				
		pos += 1

		time.sleep(settings.tick_length*10)

def rand_colors_distinct(e, strip_arr, settings):
	logging.info("started channel rand_colors_distinct")
	#color_variation = [(3,11,19), (3,11), (11,19), (3,19), (3,23,27), (5,7,28,31), (2,3), (2,11), (2,19), (11,19,23), (3,11,23)]
	number_variation = [2,3]
	
	default_c1 = 3
	default_c2 = 11
	default_c3 = 23

	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, default_c2, default_c3)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
		color3 = color_dict[c_indices[2]]
		
		var_index = settings.variation%len(number_variation)
		
		for i in range(STRIP_LENGTH):
			color_index = random.randint(0, number_variation[var_index]-1)
			strip_arr[i] = color_dict[c_indices[color_index]]

		time.sleep(settings.tick_length*100)

def game_show(e, strip_arr, settings):
	logging.info("started channel game_show")
	parts = [2,3,4,5,6,10]

	while True:
		if e.isSet():
			return
		
		var_index = settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		winner = random.randint(0, parts[var_index]-1)
		restart = False
		
		for rnd in range(30):
			if e.isSet():
				return
			if settings.variation%len(parts) != var_index:
				restart = True
				break
			
			for part in range(parts[var_index]):
				is_on = 0
				if (part+rnd)%parts[var_index] == 0:
					is_on = 1
				for i in range(part_len):
					strip_arr[i+part*part_len] = (255*is_on,255*is_on,255*is_on)
				strip_arr[part_len*part] = (255,0,0)
				strip_arr[part_len*(part+1)-1] = (255,0,0)
					
			time.sleep(settings.tick_length*200)
		
		if restart == True:
			continue
		
		#waiting period
		for part in range(parts[var_index]):
			for i in range(part_len):
				strip_arr[i+part*part_len] = (0,0,0)
			strip_arr[part_len*part] = (255,0,0)
			strip_arr[part_len*(part+1)-1] = (255,0,0)
		
		for i in range(5): #mecessary to achieve quick return when requested
			if e.isSet():
				return	
			if settings.variation%len(parts) != var_index:
				restart = True
				break
			time.sleep(settings.tick_length*500)
		
		if restart == True:
			continue
		
		#winner presentation
		for rnd in range(50):
			if e.isSet():
				return	
			if settings.variation%len(parts) != var_index:
				restart = True
				break
			for part in range(parts[var_index]):
				if part == winner:
					is_winner = True
				else:
					is_winner = False
				
				for i in range(part_len):
					is_on = 0
					if is_winner:
						is_on = random.randint(0,1)
					strip_arr[i+part*part_len] = (255*is_on,255*is_on,255*is_on)
				strip_arr[part_len*part] = (255,0,0)
				strip_arr[part_len*(part+1)-1] = (255,0,0)
			
			time.sleep(settings.tick_length*100)
		
		if restart == True:
			continue
		
		#post game waiting period
		for part in range(parts[var_index]):
			for i in range(part_len):
				strip_arr[i+part*part_len] = (0,0,0)
			strip_arr[part_len*part] = (255,0,0)
			strip_arr[part_len*(part+1)-1] = (255,0,0)
		
		for i in range(4): #mecessary to achieve quick return when requested
			if e.isSet():
				return				
			time.sleep(settings.tick_length*500)
		
def sunrise(e, strip_arr, settings):
	logging.info("started channel sunrise")
	
	center_left = int((STRIP_LENGTH/2)-1)
	center_right = int((STRIP_LENGTH/2))
	
	sun_color = (255,80,0)

	sun_radius = 0
	red_radius = 1
	
	
	while True:
		if e.isSet():
			return
		
		for i in range(STRIP_LENGTH):
			strip_arr[i] = (0,0,0)
		
		for i in range(sun_radius):
			strip_arr[center_right-i] = sun_color
			strip_arr[center_left+i] = sun_color
		
		for i in range(red_radius):
			if center_right-sun_radius-i < 0:
				break
			bg_color = (red_radius-i,int((red_radius-i)/15),0)
			strip_arr[center_right-sun_radius-i] = bg_color
			strip_arr[center_left+sun_radius+i] = bg_color
		
		
		sun_radius += 1
		red_radius = sun_radius * 4

		if sun_radius >= 20:
			for i in range(10):
				if e.isSet():
					return
				time.sleep(settings.tick_length*500)	
			sun_radius = 0
			red_radius = 1
			
		time.sleep(settings.tick_length*200)

def rainbow_wheel(pos, c1, c2, c3):
	if pos < 1/3:
		mult = pos*3
		return (int(c1[0]+(c2[0]-c1[0])*mult),int(c1[1]+(c2[1]-c1[1])*mult),int(c1[2]+(c2[2]-c1[2])*mult))
	elif pos < 2/3:
		mult = (pos-1/3)*3
		return (int(c2[0]+(c3[0]-c2[0])*mult),int(c2[1]+(c3[1]-c2[1])*mult),int(c2[2]+(c3[2]-c2[2])*mult))
	else:
		mult = (pos-2/3)*3
		return (int(c3[0]+(c1[0]-c3[0])*mult),int(c3[1]+(c1[1]-c3[1])*mult),int(c3[2]+(c1[2]-c3[2])*mult))
	
def rainbow_alt(e, strip_arr, settings):
	logging.info("started channel rainbow_alt")

	default_c1 = 3
	default_c2 = 11
	default_c3 = 19

	staggering = [(1), (1/12), (1/6)]

	while True:
		if e.isSet():
			return

		c_indices = getColorIndices(settings, default_c1, default_c2, default_c3)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
		color3 = color_dict[c_indices[2]]
		
		var_index = settings.variation%len(staggering)
		   
		for i in range(STRIP_LENGTH):
			perc = i/STRIP_LENGTH
			if staggering[var_index] != 1:
				perc -= perc%staggering[var_index]
			strip_arr[i] = rainbow_wheel(perc, color1, color2, color3)
			
		time.sleep(settings.tick_length*100)

def rainbow_alt_anim(e, strip_arr, settings):
	logging.info("started channel rainbow_alt_anim")
	
	default_c1 = 3
	default_c2 = 11
	default_c3 = 19

	staggering = [(1), (1/12), (1/6)]
	
	pos = 0
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, default_c3)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
		color3 = color_dict[c_indices[2]]

		var_index = settings.variation%len(staggering)
		   
		for i in range(STRIP_LENGTH):
			perc = i/STRIP_LENGTH
			if staggering[var_index] != 1:
				perc -= perc%staggering[var_index]
			strip_arr[(i+pos)%STRIP_LENGTH] = rainbow_wheel(perc, color1, color2, color3)
		
		pos += 1
		time.sleep(settings.tick_length*10)
		
def rainbow_fade_alt(e, strip_arr, settings):
	logging.info("started channel rainbow_fade_alt")
	
	default_c1 = 3
	default_c2 = 11
	default_c3 = 19
	
	staggering = [(1), (1/12), (1/6)]
	
	perc = 0
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, default_c3)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
		color3 = color_dict[c_indices[2]]
			
		var_index = settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			temp_perc = perc/100
			if staggering[var_index] != 1:
				temp_perc -= temp_perc%staggering[var_index]
			strip_arr[i] = rainbow_wheel(temp_perc, color1, color2, color3)
		
		perc = (perc+1)%100
		time.sleep(settings.tick_length*100)

def rainbow_center_alt(e, strip_arr, settings):
	logging.info("started channel rainbow_center_alt")
	
	default_c1 = 3
	default_c2 = 11
	default_c3 = 19

	staggering = [(1), (1/12), (1/6)]

	center_perc = 0
	center_left = int((STRIP_LENGTH/2)-1)
	center_right = int((STRIP_LENGTH/2))
	
	while True:
		if e.isSet():
			return
			
		c_indices = getColorIndices(settings, default_c1, default_c2, default_c3)
		
		color1 = color_dict[c_indices[0]]
		color2 = color_dict[c_indices[1]]
		color3 = color_dict[c_indices[2]]

		var_index = settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i <= center_left:
				perc = (center_left-i)*100/(STRIP_LENGTH)
				perc = (perc+center_perc)%100
				perc /= 100
				if staggering[var_index] != 1:
					perc -= perc%staggering[var_index]
				strip_arr[i] = rainbow_wheel(perc, color1, color2, color3)
			else:
				perc = (i-center_right)*100/(STRIP_LENGTH)
				perc = (perc+center_perc)%100
				perc /= 100
				if staggering[var_index] != 1:
					perc -= perc%staggering[var_index]
				strip_arr[i] = rainbow_wheel(perc, color1, color2, color3)
			

		center_perc = (center_perc-0.4)%100
		time.sleep(settings.tick_length*10)

def progress_bar(e, strip_arr, settings):
	logging.info("started channel progress_bar")
	
	#10sec, 30sec, 1min, 15min, 30min, 1h, 1,5h, 2h, 3h
	time_variants = [10,30,60,15*60,30*60,60*60,60*90,60*120,60*180]
	
	default_c1 = 2
	default_c2 = 1
	
	progress = 0
	time_passed = 0
	while True:
		if e.isSet():
			return
		
		c_indices = getColorIndices(settings, default_c1, default_c2, 0)
			
		var_index = settings.variation%len(time_variants)
			
		for i in range(STRIP_LENGTH):
			strip_arr[i] = color_dict[c_indices[1]]
		for i in range(STRIP_LENGTH-2, STRIP_LENGTH-2-var_index-1, -1):
			strip_arr[i] = (10,10,10)
		for i in range(progress):
			strip_arr[i] = color_dict[c_indices[0]]
		for i in range(0, STRIP_LENGTH, int(STRIP_LENGTH/4)):
			strip_arr[i] = color_dict[3]
			strip_arr[i-1] = color_dict[3]
		
		
		progress += 1
		
		restart = False	
		while True:
			if e.isSet():
				return
			if settings.variation%len(time_variants) != var_index:
				progress = 0
				restart = True
				break
			if time_passed > time_variants[var_index]/STRIP_LENGTH:
				time_passed -= time_variants[var_index]/STRIP_LENGTH
				break
			
			time_passed += settings.tick_length*100
			time.sleep(settings.tick_length*20)
		
		if progress >= STRIP_LENGTH or restart:
			progress = 0
			time_passed = 0

def flags(e, strip_arr, settings):
	logging.info("started channel flags")
	
	flag = ((3,2,3),(1,3,25),(19,2,3),(11,2,3),(3,2,11),(2,11,3),(11,25,3),(19,2,26),(2,19,3),(11,1,2),(25,19,3),(3,11,26),(11,3,19),(3,24,19),(1,2,3))
	
	while True:
		if e.isSet():
			return
			
		var_index = settings.variation%len(flag)
		
		third = int(STRIP_LENGTH/3)-1
		twothirds = third + int(STRIP_LENGTH/3)

		for i in range(0, third):
			strip_arr[i] = color_dict[flag[var_index][2]]
		for i in range(third, twothirds):
			strip_arr[i] = color_dict[flag[var_index][1]]
		for i in range(twothirds, STRIP_LENGTH):
			strip_arr[i] = color_dict[flag[var_index][0]]
		time.sleep(settings.tick_length*100)

