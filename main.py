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
TICK_LENGTH = 0.001

def draw_strip(e, strip_arr, mode_arr):
    while True:
        if e.isSet():
            return
        for i in range(strip.numPixels()):
            c = Color(int(strip_arr[i][0]*mode_arr[i][0]),int(strip_arr[i][1]*mode_arr[i][1]),int(strip_arr[i][2]*mode_arr[i][2]))
            strip.setPixelColor(i, c)
        strip.show()
        time.sleep(TICK_LENGTH)
            
if __name__ == '__main__':
    strip = Adafruit_NeoPixel(180, 18, 800000, 10, False, 255, 0)
    strip.begin()
    
    strip_arr = []
    mode_arr = []
    for i in range(STRIP_MAX):
        strip_arr.append([0,0,0])
        mode_arr.append([0,0,0])
    
    ch_settings = ChSettings(0,0,0)
    mode_settings = ModeSettings(0,1)
    
    dispatcher = {
        0: clear_strip,
        1: one_color, 
        2: two_colors, 
        3: three_colors, 
        4: animation1,
        5: animation2,
        6: rainbow,
        7: rainbow_animation,
        8: rainbow_fade,
        9: rand_colors,
        10: alternating,
        11: alternating_blinking,
        12: alternating_travel,
        13: rolling_ball
        }
        
    mode_dispatcher = {
        0: normal,
        1: fade,
        2: blinking,
        3: fast_blinking,
        4: strobe
    }
    
    e = threading.Event()
    mode_e = threading.Event()
    draw_e = threading.Event()
    index = len(dispatcher)-2
    
    
    draw_thr = threading.Thread(target=draw_strip, args=(draw_e, strip_arr, mode_arr))
    draw_thr.start()
    
    channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, ch_settings))
    channel_thr.start()
    mode_thr = threading.Thread(target=mode_dispatcher[mode_settings.mode], args=(mode_e, mode_arr, mode_settings))
    mode_thr.start()
        
    while True:
        a = input()
        if a == 'd':
            index = (index+1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, ch_settings))
            channel_thr.start()
        elif a == 'a':
            index = (index-1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, ch_settings))
            channel_thr.start()
        elif a == 'w':
            ch_settings.variation += 1
        elif a == 's':
            ch_settings.variation -= 1
        elif a == 'm':
            mode_settings.mode = (mode_settings.mode+1)%len(mode_dispatcher)
            mode_e.set()
            mode_thr.join()
            mode_e.clear()
            mode_thr = threading.Thread(target=mode_dispatcher[mode_settings.mode], args=(mode_e,mode_arr, mode_settings))
            mode_thr.start()
        elif a == 'x':
            e.set()
            mode_e.set()
            draw_e.set()
            channel_thr.join()
            mode_thr.join()
            draw_thr.join()
            break
                
            
