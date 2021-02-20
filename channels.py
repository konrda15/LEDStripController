import time
from rpi_ws281x import *
import argparse
import random
import threading
import colorsys
from colors import *

TICK_LENGTH = 0.001
STRIP_LENGTH = 180
STRIP_MAX = 180
STRIP_START = 0


def hsv_rgb(h,s,v):
    c = tuple(round(j*255) for j in  colorsys.hsv_to_rgb(h/360,s/100,v/100))
    return [c[0], c[1], c[2]]

def clear_strip(e, strip_arr, ch_settings):
	print("clear_strip")
	for i in range(STRIP_LENGTH):
		strip_arr[i] = (0,0,0)
		
def one_color(e, strip_arr, ch_settings):
	print("one_color")
	
	start_index = 2
	
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%(len(color_dict)-start_index)
		color_index = start_index+var_index
			
		for i in range(STRIP_LENGTH):
			strip_arr[i] = color_dict[color_index]

		time.sleep(TICK_LENGTH*100)
        
        
def two_colors(e, strip_arr, ch_settings):
	print("two_colors")
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
	print("three_colors")
	while True:
		if e.isSet():
			return
		third = int(STRIP_LENGTH/3)-1
		twothirds = third + int(STRIP_LENGTH/3)

		for i in range(0, third):
			strip_arr[i] = color_dict[15]
		for i in range(third, twothirds):
			strip_arr[i] = color_dict[16]
		for i in range(twothirds, STRIP_LENGTH):
			strip_arr[i] = color_dict[17]
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

def rolling_ball(e, strip_arr, ch_settings):
	print("rolling_ball")
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
				strip_arr[i] = (255,255,255)
			strip_arr[center_left] = (255,0,0)
			strip_arr[center_right] = (255,0,0)
			
			speed = speed - speed * (decel/100)
			if speed <= 0.5:
				break
			
			time.sleep(TICK_LENGTH*10)
		pos_int = int(pos)
		if pos_int < center_right:
			strip_arr[center_left] = (0,255,0)
		else:
			strip_arr[center_right] = (0,255,0)
		
		for i in range(10): #mecessary to achieve quick return when requested
			if e.isSet():
				return
			time.sleep(TICK_LENGTH*500)

def counter(e, strip_arr, ch_settings):
	print("counter")
	count = 0
	while True:
		if e.isSet():
			return
		for i in range(STRIP_LENGTH):
			strip_arr[i] = (0,0,0)
		
		temp_count = count
		index = 0	
		while temp_count > 0:
			if temp_count%2 == 1:
				strip_arr[index] = (255,255,255)
			index += 1
			temp_count >>= 1
			
		count += 1
		time.sleep(TICK_LENGTH*100)

def rainbow_colors(e, strip_arr, ch_settings):
	print("rainbow_colors")

	hue_range = [(160,240),(100,240), (0,30)]

	pos = 0
	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(hue_range)
		
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
		time.sleep(TICK_LENGTH*10)

def rainbow_center(e, strip_arr, ch_settings):
	print("rainbow_center")

	staggering = [(1), (30), (60)]

	center_val = 0
	half = int(STRIP_LENGTH/2)
	center_left = int((STRIP_LENGTH/2)-1)
	center_right = int((STRIP_LENGTH/2))
	
	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)
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
		time.sleep(TICK_LENGTH*10)

def color_transition(e, strip_arr, ch_settings):
	print("color_transition")
	
	parts = [1,2,3,4,6,8,10,20,30]
	color1 = (255,0,0)
	color2 = (0,0,255)
	
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		color_diff = (color2[0]-color1[0], color2[1]-color1[1], color2[2]-color1[2]) 
		
		for i in range(parts[var_index]):
			for j in range(part_len):
				index = i*part_len+j
				perc = j/part_len
				strip_arr[index] = (int(color1[0]+color_diff[0]*perc), int(color1[1]+color_diff[1]*perc), int(color1[2]+color_diff[2]*perc))
				


		time.sleep(TICK_LENGTH*100)

def color_transition_full(e, strip_arr, ch_settings):
	print("color_transition_full")
	
	parts = [1,2,3,4,6,8,10,20,30]
	color1 = (255,0,0)
	color2 = (255,150,0)
	
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(parts)
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
				


		time.sleep(TICK_LENGTH*100)

def color_transition_anim(e, strip_arr, ch_settings):
	print("color_transition_anim")
	
	parts = [1,2,3,4,6,8,10,20,30]
	color1 = (255,0,0)
	color2 = (0,0,255)
	pos = 0
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		color_diff = (color2[0]-color1[0], color2[1]-color1[1], color2[2]-color1[2]) 
		
		for i in range(parts[var_index]):
			for j in range(part_len):
				index = i*part_len+j
				perc = j/part_len
				strip_arr[(index+pos)%STRIP_LENGTH] = (int(color1[0]+color_diff[0]*perc), int(color1[1]+color_diff[1]*perc), int(color1[2]+color_diff[2]*perc))
				
		pos += 1

		time.sleep(TICK_LENGTH*10)
		
def color_transition_full_anim(e, strip_arr, ch_settings):
	print("color_transition_full_anim")
	
	parts = [1,2,3,4,6,8,10,20,30]
	color1 = color_dict[2]
	color2 = color_dict[3]
	pos = 0
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(parts)
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

		time.sleep(TICK_LENGTH*10)

def rand_colors_distinct(e, strip_arr, ch_settings):
	print("rand_colors_distinct")
	color_variation = [(3,11,19), (3,11), (11,19), (3,19), (3,23,27), (5,7,28,31), (2,3), (2,11), (2,19), (11,19,23), (3,11,23)]

	while True:
		if e.isSet():
			return
		
		var_index = ch_settings.variation%len(color_variation)
		
		for i in range(STRIP_LENGTH):
			color_index = random.randint(0, len(color_variation[var_index])-1)
			strip_arr[i] = color_dict[color_variation[var_index][color_index]]

		time.sleep(TICK_LENGTH*100)

def game_show(e, strip_arr, ch_settings):
	print("game_show")
	parts = [2,3,4,5,6,10]

	while True:
		if e.isSet():
			return
		
		var_index = ch_settings.variation%len(parts)
		part_len = int(STRIP_LENGTH/parts[var_index])
		winner = random.randint(0, parts[var_index]-1)
		restart = False
		
		for rnd in range(40):
			if e.isSet():
				return
			if ch_settings.variation%len(parts) != var_index:
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
					
			time.sleep(TICK_LENGTH*200)
		
		if restart == True:
			continue
		
		#waiting period
		for part in range(parts[var_index]):
			for i in range(part_len):
				strip_arr[i+part*part_len] = (0,0,0)
			strip_arr[part_len*part] = (255,0,0)
			strip_arr[part_len*(part+1)-1] = (255,0,0)
		
		for i in range(4): #mecessary to achieve quick return when requested
			if e.isSet():
				return	
			if ch_settings.variation%len(parts) != var_index:
				restart = True
				break
			time.sleep(TICK_LENGTH*500)
		
		if restart == True:
			continue
		
		#winner presentation
		for rnd in range(50):
			if e.isSet():
				return	
			if ch_settings.variation%len(parts) != var_index:
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
			
			time.sleep(TICK_LENGTH*100)
		
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
			time.sleep(TICK_LENGTH*500)
		
def sunrise(e, strip_arr, ch_settings):
	print("sunrise")
	
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
				time.sleep(TICK_LENGTH*500)	
			sun_radius = 0
			red_radius = 1
			
		time.sleep(TICK_LENGTH*200)

def rainbow_wheel(pos):
	if pos < 1/3:
		mult = pos*3
		return (int(255-255*mult),int(255*mult),0)
	elif pos < 2/3:
		mult = (pos-1/3)*3
		return (0,int(255-255*mult),int(255*mult))
	else:
		mult = (pos-2/3)*3
		return (int(255*mult),0,int(255-255*mult))
	
def rainbow_alt(e, strip_arr, ch_settings):
	print("rainbow_alt")

	staggering = [(1), (1/12), (1/6)]

	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)
		   
		for i in range(STRIP_LENGTH):
			perc = i/STRIP_LENGTH
			if staggering[var_index] != 1:
				perc -= perc%staggering[var_index]
			strip_arr[i] = rainbow_wheel(perc)
			
		time.sleep(TICK_LENGTH*100)

def rainbow_alt_anim(e, strip_arr, ch_settings):
	print("rainbow_alt_anim")

	staggering = [(1), (1/12), (1/6)]
	
	pos = 0
	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)
		   
		for i in range(STRIP_LENGTH):
			perc = i/STRIP_LENGTH
			if staggering[var_index] != 1:
				perc -= perc%staggering[var_index]
			strip_arr[(i+pos)%STRIP_LENGTH] = rainbow_wheel(perc)
		
		pos += 1
		time.sleep(TICK_LENGTH*10)
		
def rainbow_fade_alt(e, strip_arr, ch_settings):
	print("rainbow_fade_alt")

	staggering = [(1), (1/12), (1/6)]
	
	perc = 0
	while True:
		if e.isSet():
			return
			
		var_index = ch_settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			temp_perc = perc/100
			if staggering[var_index] != 1:
				temp_perc -= temp_perc%staggering[var_index]
			strip_arr[i] = rainbow_wheel(temp_perc)
		
		perc = (perc+1)%100
		time.sleep(TICK_LENGTH*100)

def rainbow_center_alt(e, strip_arr, ch_settings):
	print("rainbow_center_alt")

	staggering = [(1), (1/12), (1/6)]

	center_perc = 0
	center_left = int((STRIP_LENGTH/2)-1)
	center_right = int((STRIP_LENGTH/2))
	
	while True:
		if e.isSet():
			return

		var_index = ch_settings.variation%len(staggering)
		
		for i in range(STRIP_LENGTH):
			if i <= center_left:
				perc = (center_left-i)*100/(STRIP_LENGTH)
				perc = (perc+center_perc)%100
				perc /= 100
				if staggering[var_index] != 1:
					perc -= perc%staggering[var_index]
				strip_arr[i] = rainbow_wheel(perc)
			else:
				perc = (i-center_right)*100/(STRIP_LENGTH)
				perc = (perc+center_perc)%100
				perc /= 100
				if staggering[var_index] != 1:
					perc -= perc%staggering[var_index]
				strip_arr[i] = rainbow_wheel(perc)
			

		center_perc = (center_perc-0.4)%100
		time.sleep(TICK_LENGTH*10)
