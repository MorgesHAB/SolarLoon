#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute

# import all the module we will need
import gps
import time
import os
import RPi.GPIO as GPIO

# Define vrariables how would count the number of GPS Data
Nbr_GPS_Time_Data = 0
NBr_GPS_Speed_Data = 0
NBr_GPS_Altitude_Data = 0
Nbr_GPS_Longitude_Data = 0
NBr_GPS_Latitude_Data = 0

# Define the number of Data you want to record in 1 min
Nbr_Data_per_Minute = 12
Time_between_each_recorded_data = int(60 / Nbr_Data_per_Minute)  # 60 because 1 min

# As we don't see if the camera is capturing a photo, we will 
# shedule a LED that will light on when an altitude data is
# recording on file.txt

# So we setup the GPIO of the LED
GPIO_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)  # define this pin as an output

# Setup the LoRa GPS Hat    
# Read on the localhost 2947 port (gpsd)
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
  
try :   
  while True :
     report = session.next()   # Wait the next TPV report
     # Uncomment the next line to see all the data on the TPV report
     #print report
     os.chdir("/home/pi/SolarLoon_Software/GPS/GPS_DATA") # Go to the recorded data folder 
     # The GPS takes GPS data every secondes, so we take only the GPS data
     # every "x" secondes
     if report['class'] == 'TPV':
         if hasattr(report, 'time'):        # if there's GPS time data
            if Nbr_GPS_Time_Data % Time_between_each_recorded_data == 0 : # % = the rest of the division
             with open("Time.txt","a") as fichier :
                print >> fichier, report.time     # record time on file.txt
            Nbr_GPS_Time_Data +=1
         if hasattr(report, 'speed'):
            if NBr_GPS_Speed_Data % Time_between_each_recorded_data == 0 :
             with open("Speed.txt","a") as fichier2 :
              print >> fichier2, report.speed * gps.MPS_TO_KPH
            NBr_GPS_Speed_Data +=1
         if hasattr(report, 'alt'):
            if NBr_GPS_Altitude_Data % Time_between_each_recorded_data == 0 :
             with open("Altitude.txt","a") as fichier3 :
              print >> fichier3, report.alt    
            NBr_GPS_Altitude_Data +=1
         if hasattr(report, 'lon'):
            if Nbr_GPS_Longitude_Data % Time_between_each_recorded_data == 0 :
             with open("Longitude.txt","a") as fichier4 :
              print >> fichier4, report.lon
            Nbr_GPS_Longitude_Data +=1
         if hasattr(report, 'lat'):
            if NBr_GPS_Latitude_Data % Time_between_each_recorded_data == 0 :
             with open("Latitude.txt","a") as fichier5 :
              print >> fichier5, report.lat
             GPIO.output(GPIO_PIN, GPIO.HIGH)
             time.sleep(2)
             GPIO.output(GPIO_PIN, GPIO.LOW)
             GPIO.cleanup()
            NBr_GPS_Latitude_Data +=1 


except KeyError:
   pass
except KeyboardInterrupt:
  GPIO.cleanup()
  quit()
except StopIteration:
   session = None
   print "GPSD has terminated)"
