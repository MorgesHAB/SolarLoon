#!/usr/bin/python
#coding=utf-8
# This script will be actived on the boot of the raspberry Pi 0

# import all the module we will need
import gps
import time
import os
import RPi.GPIO as GPIO
import subprocess

# Setup the LoRa GPS Hat    
# Read on the localhost 2947 port (gpsd)
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Define vrariable how would count the number of GPS Data
Nbr_GPS_Data = 0
# Define the number of Data you want to record in 1 min
Nbr_Data_per_Minute = 12
Time_between_each_recorded_data = int(60 / Nbr_Data_per_Minute)  # 60 because 1 min

FIRST_TIME = True

while True :
    try:
         if FIRST_TIME :
 	          subprocess.call(["./chisterapi", " Data are comming !"])
            FIRST_TIME = False
         # Go to the sender data folder 
         os.chdir("/home/pi/SolarLoon_Software/LoRa_Sending_Data") 
         report = session.next()
         # The GPS takes GPS data every secondes, so we send only the GPS data
         # every "x" secondes
         if report['class'] == 'TPV':
             # if there's GPS time data
             if hasattr(report, 'time' and 'speed' and 'lon' and 'lat' and 'alt'):  
               # Select only the wanted data
               if Nbr_GPS_Data % Time_between_each_recorded_data == 0 :
                 # We have to change the type of GPS Data in structure type
                 GPSTIME = str(report.time)
                 SPEED = str(report.speed)
                 LATITUDE = str(report.lat)
                 LONGITUDE = str(report.lon)
                 ALTITUDE = str(report.alt)
                 # We send the GPS Data to the programme C++ how send the message by radio
                 # Warning, the order GPSTIME, SPEED, ... plays a role 
         	       subprocess.call(["./chisterapi", GPSTIME, SPEED, LATITUDE, LONGITUDE, ALTITUDE])
               Nbr_GPS_Data +=1
             

    except KeyError:
       pass
    except KeyboardInterrupt:
      quit()
      print("Exit")
    except StopIteration:
       session = None
       print "GPSD has terminated"

