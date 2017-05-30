#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute
# Warning : used the 1-wire protocol (Default : Pin 7)

# import all the module we will need
import os
import glob
import RPi.GPIO as GPIO
import subprocess

# We have to write that on the terminal raspberry Pi
os.system('modprobe w1-gpio')    
os.system('modprobe w1-therm')  
# Read on the 1-wire port
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 # Define a function taht will return the temperature
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

try :
    # Go to the sender data folder 
    os.chdir("/SolarLoon_Software/LORA_Sender")
    TEMPERATURE = str(read_temp())
    msg_Temperature = TEMPERATURE+" °C"
    subprocess.call(["./chisterapi", msg_Temperature])  

except KeyboardInterrupt:
    print("Exit")
    
