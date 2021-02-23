import time
from rpi_ws281x import *
import argparse
import random
import threading
import colorsys
from channels import *
from modes import *
from settings import *

STRIP_MAX = 180
STRIP_START = 0
STANDARD_TICK_LENGTH = 0.001

def draw_strip(e, strip_arr, mode_arr):
    while True:
        if e.isSet():
            return
        for i in range(strip.numPixels()):
            c = Color(int(strip_arr[i][0]*mode_arr[i][0]),int(strip_arr[i][1]*mode_arr[i][1]),int(strip_arr[i][2]*mode_arr[i][2]))
            strip.setPixelColor(i, c)
        strip.show()
        time.sleep(STANDARD_TICK_LENGTH)
    
            
if __name__ == '__main__':
    strip = Adafruit_NeoPixel(180, 18, 800000, 10, False, 255, 0)
    strip.begin()
    
    strip_arr = []
    mode_arr = []
    for i in range(STRIP_MAX):
        strip_arr.append([0,0,0])
        mode_arr.append([0,0,0])
    
    global_settings = Settings(0,STANDARD_TICK_LENGTH,0,0,0,0,1)
    
    dispatcher = {
        0: clear_strip,
        1: one_color, 
        2: two_colors, 
        3: three_colors, 
        4: ping_pong,
        5: travelling,
        6: rainbow,
        7: rainbow_animation,
        8: rainbow_fade,
        9: rand_colors,
        10: alternating,
        11: alternating_blinking,
        12: alternating_travel,
        13: rolling_ball,
        14: counter,
        15: rainbow_colors,
        16: rainbow_center,
        17: color_transition,
        18: color_transition_full,
        19: color_transition_anim,
        20: color_transition_full_anim,
        21: rand_colors_distinct,
        22: game_show,
        23: sunrise,
        24: rainbow_alt,
        25: rainbow_alt_anim,
        26: rainbow_fade_alt,
        27: rainbow_center_alt,
        28: progress_bar,
        29: flags,
        }
        
    mode_dispatcher = {
        0: normal,
        1: fade,
        2: adv_fade,
        3: blinking,
        4: fast_blinking,
        5: strobe
    }
    
    e = threading.Event()
    mode_e = threading.Event()
    draw_e = threading.Event()
    index = len(dispatcher)-2
    
    
    draw_thr = threading.Thread(target=draw_strip, args=(draw_e, strip_arr, mode_arr))
    draw_thr.start()
    
    channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
    channel_thr.start()
    mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e, mode_arr, global_settings))
    mode_thr.start()
        
    while True:
        a = input()
        if a == 'd':
            index = (index+1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()
        elif a == 'a':
            index = (index-1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()
        elif a == 'w':
            global_settings.variation += 1
        elif a == 's':
            global_settings.variation -= 1
        elif a == 'j':
            global_settings.tick_length = round(min(global_settings.tick_length+0.0002,0.005),4)
            print("speed: ",  global_settings.tick_length)
        elif a == 'k':
            global_settings.tick_length = round(max(global_settings.tick_length-0.0002,0.0002),4)
            print("speed: ",  global_settings.tick_length)
        elif a == 'q':
            global_settings.brightness = round(min(1, global_settings.brightness+0.1),1)
            print("brightness: ", global_settings.brightness)
        elif a == 'e':
            global_settings.brightness = round(max(0, global_settings.brightness-0.1),1)
            print("brightness: ", global_settings.brightness)
        elif a == 'm':
            global_settings.mode = (global_settings.mode+1)%len(mode_dispatcher)
            mode_e.set()
            mode_thr.join()
            mode_e.clear()
            mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e,mode_arr, global_settings))
            mode_thr.start()
        elif a == 'x':
            e.set()
            mode_e.set()
            draw_e.set()
            channel_thr.join()
            mode_thr.join()
            draw_thr.join()
            break
        elif 'c' in a: # valid input c103, c13 for primary color and third element in dict
            if len(a) < 3 or len(a) > 4:
                print("invalid command")
                continue
            if a[0] is not 'c':
                print("invalid command")
                continue 
            try:
                temp_a = a[1]
                temp_b = a[2:len(a)]
                color_index = int(temp_a)
                color_dict_index = int(temp_b)
                
                if color_index < 1 or color_index > 3:
                    print("invalid command")
                    continue
                if color_dict_index < 0 or color_dict_index >= len(color_dict):
                    print("invalid command")
                    continue
                    
                if color_index == 1:
                    global_settings.color1 = color_dict_index
                    print("color", color_index, " changed to ", color_dict_index)
                elif color_index == 2:
                    global_settings.color2 = color_dict_index
                    print("color", color_index, " changed to ", color_dict_index)
                elif color_index == 3:
                    global_settings.color3 = color_dict_index
                    print("color", color_index, " changed to ", color_dict_index)
            except:
                print("invalid command")
                continue
        else:
            try:
                new_ch = int(a)
                if new_ch >= 0 and new_ch < len(dispatcher):
                    index = new_ch
                    e.set()
                    channel_thr.join()
                    e.clear()
                    global_settings.reset()
                    channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
                    channel_thr.start()
            except:
                print("invalid command")
                continue
                
            
