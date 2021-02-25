import time
from rpi_ws281x import *
import argparse
import random
import threading
import colorsys
from channels import *
from modes import *
from settings import *
from sensor import *
from multiprocessing import Process, Pipe

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
        time.sleep(STANDARD_TICK_LENGTH*10)

'''def command_handler(if_input, input_buffer):
    if if_input == 'ch_down':
        index = (index+1)%len(dispatcher)
        e.set()
        channel_thr.join()
        e.clear()
        global_settings.reset()
        channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
        channel_thr.start()
    elif if_input == 'ch_up':
        index = (index-1)%len(dispatcher)
        e.set()
        channel_thr.join()
        e.clear()
        global_settings.reset()
        channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
        channel_thr.start()
    elif if_input == 'var_up':
        global_settings.variation += 1
    elif if_input == 'var_down':
        global_settings.variation -= 1
    elif if_input == 's_up':
        global_settings.tick_length = round(min(global_settings.tick_length+0.0002,0.005),4)
        print("speed: ",  global_settings.tick_length)
    elif if_input == 's_down':
        global_settings.tick_length = round(max(global_settings.tick_length-0.0002,0.0002),4)
        print("speed: ",  global_settings.tick_length)
    elif if_input == 'b_up':
        global_settings.brightness = round(min(1, global_settings.brightness+0.1),1)
        print("brightness: ", global_settings.brightness)
    elif if_input == 'b_down':
        global_settings.brightness = round(max(0, global_settings.brightness-0.1),1)
        print("brightness: ", global_settings.brightness)
    elif if_input == 'm_up':
        global_settings.mode = (global_settings.mode+1)%len(mode_dispatcher)
        mode_e.set()
        mode_thr.join()
        mode_e.clear()
        mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e,mode_arr, global_settings))
        mode_thr.start()
    elif if_input == 'm_down':
        global_settings.mode = (global_settings.mode-1)%len(mode_dispatcher)
        mode_e.set()
        mode_thr.join()
        mode_e.clear()
        mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e,mode_arr, global_settings))
        mode_thr.start()
    elif if_input == 'ok':
        if len(input_buffer) == 0:
            print("no channel number")
            return
        elif len(input_buffer) == 1:
            new_ch = int(input_buffer)
        else:
            new_ch = int(input_buffer[-2:])
            
        if new_ch >= 0 and new_ch < len(dispatcher):
            index = new_ch
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()
        else:
            print("invalid channel")'''
        
def sensor_handler(e, cmd):
    input_buffer = ""
    
    while True:
        if e.isSet():
            return
        if main_conn.poll():
            if_input = main_conn.recv()
            if if_input.isnumeric():
                input_buffer += if_input
            else:
                cmd[0] = (if_input, input_buffer)
                input_buffer = ""
        time.sleep(STANDARD_TICK_LENGTH*10)
        
            
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
        4: alternating,
        5: alternating_blinking,
        6: alternating_travel,
        7: ping_pong,
        8: travelling,
        9: progress_bar,
        10: counter,
        11: rainbow_alt,
        12: rainbow_alt_anim,
        13: rainbow_center_alt,
        14: rainbow_fade_alt,
        15: color_transition,
        16: color_transition_full,
        17: color_transition_anim,
        18: color_transition_full_anim,
        19: rand_colors_distinct,
        20: rand_colors,
        21: rolling_ball,
        22: game_show,
        23: flags,
        24: sunrise,
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
    sensor_handler_e = threading.Event()

    
    draw_thr = threading.Thread(target=draw_strip, args=(draw_e, strip_arr, mode_arr))
    draw_thr.start()

    index = 1
    
    channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
    channel_thr.start()
    mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e, mode_arr, global_settings))
    mode_thr.start()

    main_conn, sensor_conn = Pipe()
    p = Process(target=if_sensor, args=(sensor_conn, global_settings))
    p.start()
    
    cmd = []
    cmd.append(("", 0))
    
    sensor_thr = threading.Thread(target=sensor_handler, args=(sensor_handler_e, cmd))
    sensor_thr.start()
    
    while True:
        if cmd[0][0] is not "":
            print("Input: ", cmd[0][0], ", Number: ", cmd[0][1])
            cmd[0] = ("",0)
        else:
            time.sleep(STANDARD_TICK_LENGTH*100)
        
        input_cmd = cmd[0][0]
        input_number = cmd[0][1]
        
        if input_cmd == 'ch_up':
            index = (index+1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()
        elif input_cmd == 'ch_down':
            index = (index-1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()
        elif input_cmd == 'var_up':
            global_settings.variation += 1
        elif input_cmd == 'var_down':
            global_settings.variation -= 1
        elif input_cmd == 's_down':
            global_settings.tick_length = round(min(global_settings.tick_length+0.0002,0.005),4)
            print("speed: ",  global_settings.tick_length)
        elif input_cmd == 's_up':
            global_settings.tick_length = round(max(global_settings.tick_length-0.0002,0.0002),4)
            print("speed: ",  global_settings.tick_length)
        elif input_cmd == 'b_up':
            global_settings.brightness = round(min(1, global_settings.brightness+0.1),1)
            print("brightness: ", global_settings.brightness)
        elif input_cmd == 'b_down':
            global_settings.brightness = round(max(0, global_settings.brightness-0.1),1)
            print("brightness: ", global_settings.brightness)
        elif input_cmd == 'm_up':
            global_settings.mode = (global_settings.mode+1)%len(mode_dispatcher)
            mode_e.set()
            mode_thr.join()
            mode_e.clear()
            mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e,mode_arr, global_settings))
            mode_thr.start()
        elif input_cmd == 'm_down':
            global_settings.mode = (global_settings.mode-1)%len(mode_dispatcher)
            mode_e.set()
            mode_thr.join()
            mode_e.clear()
            mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e,mode_arr, global_settings))
            mode_thr.start()
        elif input_cmd == 'ok':
            if len(input_number) == 0:
                print("no channel number")
                continue
            elif len(input_number) == 1:
                new_ch = int(input_number)
            else:
                new_ch = int(input_number[-2:])
                
            if new_ch >= 0 and new_ch < len(dispatcher):
                index = new_ch
                e.set()
                channel_thr.join()
                e.clear()
                global_settings.reset()
                channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
                channel_thr.start()
            else:
                print("invalid channel")
                continue
        elif input_cmd == 'color':
            if len(input_number) == 2:
                new_col = int(input_number[-1:])
            elif len(input_number) > 2:
                new_col = int(input_number[-2:])
            else:
                print("invalid color")
                continue
            color_index = int(input_number[0])
            if color_index < 1 or color_index > 3:
                print("invalid color index")
                continue
            if new_col < 0 or new_col >= len(color_dict):
                print("invalid color")
                continue
            
            if color_index == 1:
                global_settings.color1 = new_col
                print("color", color_index, " changed to ", new_col)
            elif color_index == 2:
                global_settings.color2 = new_col
                print("color", color_index, " changed to ", new_col)
            elif color_index == 3:
                global_settings.color3 = new_col
                print("color", color_index, " changed to ", new_col)
        elif input_cmd == 'reset':
            global_settings.reset()
        elif input_cmd == 'off':
            index = 0
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()
                
    '''while True:
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
            sensor_handler_e.set()
            main_conn.send("quit")
            channel_thr.join()
            mode_thr.join()
            draw_thr.join()
            sensor_thr.join()
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
                continue'''
                
            
