import time
from rpi_ws281x import *
import argparse
import random
import threading
import logging
from channels import *
from modes import *
from settings import *
from sensor import *
from multiprocessing import Process, Pipe

STANDARD_TICK_LENGTH = 0.001

def draw_strip(e, pause_e, strip_arr, mode_arr, global_settings):
    while True:
        if e.isSet():
            return
            
        pause_e.wait()
        numPixels = strip.numPixels()
            
        for i in range(numPixels):
            c = Color(int(strip_arr[i][0]*mode_arr[i][0]),int(strip_arr[i][1]*mode_arr[i][1]),int(strip_arr[i][2]*mode_arr[i][2]))
            if global_settings.reverse:
                strip.setPixelColor(i, c)
            else:
                strip.setPixelColor(numPixels-1-i, c)
        strip.show()
        
        if(global_settings.channel <= 3 and global_settings.mode == 0):
            time.sleep(STANDARD_TICK_LENGTH*500)
        else:
            time.sleep(STANDARD_TICK_LENGTH*10)

        
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

def console_input(e, cmd):
    while True:
        if e.isSet():
            return
        
        new_input = input("Enter your command: ")
        new_input_split = new_input.split()
        
        if len(new_input_split) == 1:
            cmd[0] = (new_input_split[0], '0')
        elif len(new_input_split) == 2:
            if new_input_split[1].isnumeric():
                cmd[0] = (new_input_split[0], new_input_split[1])
            else:
                cmd[0] = (new_input_split[0], '0')
        else:
            print("invalid console input")
        
        time.sleep(STANDARD_TICK_LENGTH * 100)
            
if __name__ == '__main__':
    logging.basicConfig(filename='ledstrip.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('LEDStripController started')
    
    strip = Adafruit_NeoPixel(144, 18, 800000, 10, False, 255, 0)
    strip.begin()
    
    strip_arr = []
    mode_arr = []
    for i in range(STRIP_MAX):
        strip_arr.append([0,0,0])
        mode_arr.append([0,0,0])
    
    global_settings = Settings(0,STANDARD_TICK_LENGTH,0,0,0,1,0,1,False)
    
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
    pause_e = threading.Event()
    pause_e.set()
    
    draw_thr = threading.Thread(target=draw_strip, args=(draw_e, pause_e, strip_arr, mode_arr, global_settings))
    draw_thr.start()
    if draw_thr.isAlive():
        logging.info('draw_thr started')
    
    channel_thr = threading.Thread(target=dispatcher[global_settings.channel], args=(e,strip_arr, global_settings))
    channel_thr.start()
    if channel_thr.isAlive():
        logging.info('channel_thr started')
    
    mode_thr = threading.Thread(target=mode_dispatcher[global_settings.mode], args=(mode_e, mode_arr, global_settings))
    mode_thr.start()
    if mode_thr.isAlive():
        logging.info('mode_thr started')
        
    main_conn, sensor_conn = Pipe()
    p = Process(target=if_sensor, args=(sensor_conn, global_settings))
    p.start()
    if p.is_alive():
        logging.info('sensor process started')
    
    cmd = []
    cmd.append(("", 0))
    
    sensor_thr = threading.Thread(target=sensor_handler, args=(sensor_handler_e, cmd))
    sensor_thr.start()
    if sensor_thr.isAlive():
        logging.info('sensor_thr started')
    
    console_thr = threading.Thread(target=console_input, args=(sensor_handler_e, cmd)) #use same event
    console_thr.start()
    if console_thr.isAlive():
        logging.info('console_thr started')
    
    while True:
        if cmd[0][0] is not "":
            temp_log_str = "Input: " + cmd[0][0] + ", Number: " + cmd[0][1]
            logging.info(temp_log_str)
            cmd[0] = ("",0)
        else:
            time.sleep(STANDARD_TICK_LENGTH*100)
        
        input_cmd = cmd[0][0]
        input_number = cmd[0][1]
        
        if input_cmd == 'ch_up':
            global_settings.channel = (global_settings.channel+1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.variation = 0
            channel_thr = threading.Thread(target=dispatcher[global_settings.channel], args=(e,strip_arr, global_settings))
            channel_thr.start()
            
        elif input_cmd == 'ch_down':
            global_settings.channel = (global_settings.channel-1)%len(dispatcher)
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.variation = 0
            channel_thr = threading.Thread(target=dispatcher[global_settings.channel], args=(e,strip_arr, global_settings))
            channel_thr.start() 
            
        elif input_cmd == 'var_up':
            global_settings.variation += 1
            
            temp_log_str = 'new variation: ' + str(global_settings.variation)
            logging.info(temp_log_str)
            
        elif input_cmd == 'var_down':
            global_settings.variation -= 1
            
            temp_log_str = 'new variation: ' + str(global_settings.variation)
            logging.info(temp_log_str)
            
        elif input_cmd == 's_down':
            global_settings.tick_length = round(min(global_settings.tick_length+0.0002,0.005),4)
            
            temp_log_str = 'new speed: ' + str(global_settings.tick_length)
            logging.info(temp_log_str)
            
        elif input_cmd == 's_up':
            global_settings.tick_length = round(max(global_settings.tick_length-0.0002,0.0002),4)
            
            temp_log_str = 'new speed: ' + str(global_settings.tick_length)
            logging.info(temp_log_str)
            
        elif input_cmd == 'b_up':
            global_settings.brightness = round(min(1, global_settings.brightness+0.1),1)
            
            temp_log_str = 'new brightness: ' + str(global_settings.brightness)
            logging.info(temp_log_str)
            
        elif input_cmd == 'b_down':
            global_settings.brightness = round(max(0, global_settings.brightness-0.1),1)
            
            temp_log_str = 'new brightness: ' + str(global_settings.brightness)
            logging.info(temp_log_str)
            
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
                logging.info("input error: no channel number")
                continue
            elif len(input_number) == 1:
                new_ch = int(input_number)
            else:
                new_ch = int(input_number[-2:])
                
            if new_ch >= 0 and new_ch < len(dispatcher):
                global_settings.channel = new_ch
                e.set()
                channel_thr.join()
                e.clear()
                global_settings.variation = 0
                channel_thr = threading.Thread(target=dispatcher[global_settings.channel], args=(e,strip_arr, global_settings))
                channel_thr.start()
            else:
                logging.info("input error: invalid channel")
                continue
                
        elif input_cmd == 'color':
            if len(input_number) == 2:
                new_col = int(input_number[-1:])
            elif len(input_number) > 2:
                new_col = int(input_number[-2:])
            else:
                logging.info("input error: invalid color")
                continue
            color_index = int(input_number[0])
            if color_index < 1 or color_index > 3:
                logging.info("input error: invalid color index")
                continue
            if new_col < 0 or new_col >= len(color_dict):
                logging.info("input error: invalid color")
                continue
            
            if color_index == 1:
                global_settings.color1 = new_col
                temp_log_str = "color" + str(color_index) + " changed to " + str(new_col)
                logging.info(temp_log_str)
            elif color_index == 2:
                global_settings.color2 = new_col
                temp_log_str = "color" + str(color_index) + " changed to " + str(new_col)
                logging.info(temp_log_str)
            elif color_index == 3:
                global_settings.color3 = new_col
                temp_log_str = "color" + str(color_index) + " changed to " + str(new_col)
                logging.info(temp_log_str)
                
        elif input_cmd == 'reset':
            global_settings.reset()
            logging.info('reset settings')
        
        elif input_cmd == 'pause':
            pause_e.clear()
            logging.info('pause') 
        
        elif input_cmd == 'play':
            pause_e.set()
            logging.info('play') 
         
        elif input_cmd == 'reverse':
            if global_settings.reverse:
                global_settings.reverse = False
            else:
                global_settings.reverse = True
            logging.info('reverse') 
               
        elif input_cmd == 'off' and input_number == '999':
            e.set()
            mode_e.set()
            draw_e.set()
            sensor_handler_e.set()
            main_conn.send("quit")
            channel_thr.join()
            mode_thr.join()
            draw_thr.join()
            sensor_thr.join()
            console_thr.join()
            logging.info('quit LEDStripController')
            break
            
        elif input_cmd == 'off':
            index = 0
            e.set()
            channel_thr.join()
            e.clear()
            global_settings.reset()
            channel_thr = threading.Thread(target=dispatcher[index], args=(e,strip_arr, global_settings))
            channel_thr.start()   
