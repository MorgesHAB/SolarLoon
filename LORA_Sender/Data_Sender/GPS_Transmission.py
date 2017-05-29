#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute

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
Check_if_all_msg = False
Nbr_received_DATA = 0

while Nbr_GPS_Data < 60 :
    try:
         # Go to the sender data folder 
         os.chdir("/home/pi/SolarLoon_Software/LORA_Sender")
         if FIRST_TIME :
 	          subprocess.call(["./chisterapi", " Data are comming !"])
            FIRST_TIME = False
         report = session.next()
         # The GPS takes GPS data every secondes, so we send only the GPS data
         # every "x" secondes
         if report['class'] == 'TPV':
             # if there's GPS time data
             if hasattr(report, 'time' and 'speed' and 'lon' and 'lat' and 'alt'):  
               # Select only the wanted data
               if Nbr_GPS_Data % Time_between_each_recorded_data == 0 :
                 # We want to be sure that we receive all the GPS data !
                 # We will have to change the type of GPS Data in structure type
                 if Check_if_all_msg == false :
                    if report.time :
                      GPSTIME = str(report.time)
                      Nbr_received_DATA +=1
                    if report.speed :
                      SPEED = str(report.speed * gps.MPS_TO_KPH)
                      Nbr_received_DATA +=1
                    if report.lon :
                      LONGITUDE = str(report.lon)
                      Nbr_GPS_Data +=1
                    if report.lat :
                      LATITUDE = str(report.lat)
                      Nbr_received_DATA +=1
                    if report.alt :
                      ALTITUDE = str(report.alt)
                      Nbr_received_DATA +=1
                    if Nbr_received_DATA == 5 :
                      Check_if_all_msg = True
                      Nbr_received_DATA = 0
                  if Check_if_all_msg == True :
                    # We send the GPS Data to the programme C++ how send the message by radio
                    # Warning, the order GPSTIME, SPEED, ... plays a role 
                    subprocess.call(["./chisterapi", GPSTIME, SPEED, LONGITUDE, LATITUDE, ALTITUDE])
               Nbr_GPS_Data +=1
             

    except KeyError:
       pass
    except KeyboardInterrupt:
      quit()
      print("Exit")
    except StopIteration:
       session = None
       print "GPSD has terminated"

