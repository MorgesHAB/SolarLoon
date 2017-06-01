#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute
# Warning : used the 1-wire protocol (Default : Pin 7)

# import all the module we will need
import os
import glob
import time
import RPi.GPIO as GPIO
import gps

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

# Define a vrariable how would count the number of captor Data
Nbr_Data_Temperature = 0
# Define the number of Data you want to record in 1 min
Nbr_Data_per_Minute = 3
Time_between_each_recorded_data = int(60 / Nbr_Data_per_Minute)  # 60 because 1 min

# Setup the LoRa GPS Hat
# Read on the localhost 2947 port (gpsd)
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
# Define a vrariables how would count the number of GPS Data
Nbr_GPS_Altitude_Data = 1
Nbr_GPS_Time_Data = 1

# We have to shedule the captor in order to record "x" data in 1 minute and not more !
try :
  # Go to the recorded data folder 
  os.chdir("/home/pi/SolarLoon_Software/Captor/Data_Captor")
  while Nbr_Data_Temperature < Nbr_Data_per_Minute :
    #print(read_temp())
	# Now we have the Data, we record the temperature and the humidity on file.txt
	with open("DS18B20_Temperature.txt","a") as fichier :
        print >> fichier, read_temp()         # record temperature on file.txt
    # We want to record the Pi0 time when a DS18B20 data is recorded
    TIME = time.strftime("%H-%M-%S")
    with open("DS18B20_Time.txt","a") as fichier2 :
        print >> fichier2, TIME       # record time on file.txt
    # Wait between each recorded data (in secondes)
    time.sleep(Time_between_each_recorded_data)
    Nbr_Data_Temperature +=1 
  # The GPS takes GPS data every secondes, so we take only 
  #the GPS data when a captor Data is recorded
  while Nbr_GPS_Altitude_Data and Nbr_GPS_Time_Data < 61 :
    report = session.next()   # Wait the next TPV report 
    if report['class'] == 'TPV':
        if hasattr(report, 'alt'):    # if there's GPS altitude data
            if Nbr_GPS_Altitude_Data % Time_between_each_recorded_data == 0 :  # % = the rest of the division
               with open("Altitude_GPS_Captor.txt","a") as fichier3 :
                 print >> fichier3, report.alt    # record altitude on file.txt
            Nbr_GPS_Altitude_Data +=1    
        if hasattr(report, 'time'):   # if there's GPS time data
            if Nbr_GPS_Time_Data % Time_between_each_recorded_data == 0 :
               with open("Time_GPS_Captor.txt","a") as fichier5 :
                 print >> fichier5, report.time   # record time on file.txt
            Nbr_GPS_Time_Data +=1    

except KeyboardInterrupt:
    print("Exit")
    
