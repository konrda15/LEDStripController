#---------------------------------------------------------------------#
#Name - IR&NECDataCollect.py
#Description - Reads data from the IR sensor but uses the official NEC Protocol (command line version)
#Author - Lime Parallelogram
#Licence - Attribution Lime
#Date - 06/07/19 - 18/08/19
#---------------------------------------------------------------------#
#Imports modules
import RPi.GPIO as GPIO
import time
from datetime import datetime
from multiprocessing import Process, Pipe

PIN_IN = 11

key_codes = { #5381 samsung
    16657686751: "1",
    16657719391: "2", 
    16657703071: "3", 
    16657682671: "4", 
    16657715311: "5", 
    16657698991: "6", 
    16657690831: "7", 
    16657723471: "8", 
    16657707151: "9", 
    16657713271: "0", 
    16657694911: "off", 
    16657715821: "nothing", 
    16657736221: "play", 
    16657699501: "pause", 
    16657703581: "nothing", 
    16657719901: "s_down", 
    16657683181: "s_up", 
    16657680121: "var_up", 
    16657712761: "var_down", 
    16657720921: "ch_down", 
    16657696441: "ch_up", 
    16657684201: "ok", 
    16657701031: "color", 
    16657724491: "reset", 
    16657735711: "b_up", 
    16657731631: "b_down", 
    16657696951: "m_up", 
    16657680631: "m_down", 
    }
	
#==================#
#Promps for values
#Input pin

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_IN,GPIO.IN)


def ConvertInt(BinVal): #Converts binary data to hexidecimal
    tmpB2 = int(str(BinVal), 2)
    return tmpB2
		
def getData(): #Pulls data from sensor
    num1s = 0 #Number of consecutive 1s
    command = [] #Pulses and their timings
    binary = 1 #Decoded binary command
    previousValue = 0 #The previous pin state
    value = GPIO.input(PIN_IN) #Current pin state
    
    waitTime = datetime.now()
    
    while value: #Waits until pin is pulled low
        if (datetime.now() - waitTime).seconds > 3:
            return 0
        value = GPIO.input(PIN_IN)
        

    startTime = datetime.now() #Sets start time

    while True:
        if value != previousValue: #Waits until change in state occurs
            now = datetime.now() #Records the current time
            pulseLength = now - startTime #Calculate time in between pulses
            startTime = now #Resets the start time
            command.append((previousValue, pulseLength.microseconds)) #Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
	
        #Interrupts code if an extended high period is detected (End Of Command)	
        if value:
            num1s += 1
        else:
            num1s = 0

        if num1s > 10000:
            break
	
        #Reads values again
        previousValue = value
        value = GPIO.input(PIN_IN)
		
	#Covers data to binary
    for (typ, tme) in command:
        if typ == 1:
            if tme > 1000: #According to NEC protocol a gap of 1687.5 microseconds repesents a logical 1 so over 1000 should make a big enough distinction
                binary = binary * 10 + 1
            else:
                binary *= 10
                
    if len(str(binary)) > 34: #Sometimes the binary has two rouge charactes on the end
        binary = int(str(binary)[:34])
        
    return binary
	

#==================#
#Main program loop
def if_sensor(sensor_conn, settings):
#if __name__ == '__main__':
    while True:
        if sensor_conn.poll():
            if sensor_conn.recv() == "quit":
                return                
        command = ConvertInt(getData())	
        #print("Hex value: " + str(command))
        try:
            sensor_conn.send(key_codes[command])
            time.sleep(0.2)
        except:
            pass
            #print("not found")

    GPIO.cleanup()

