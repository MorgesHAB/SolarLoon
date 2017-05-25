#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute

# import all the module we will need
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# Define the captor's modele to use the Adafruit_DHT librairy
DHTSensor = Adafruit_DHT.DHT22
# Define the pin used for the DHT22 signal, and define it as an Input
GPIO_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)
# Define a vrariable how would count the number of Data
Nbr_Data = 0
# Define the number of Data you want to record in 1 min
Nbr_Data_per_Minute = 3
Time_between_each_recorded_data = int(60 / Nbr_Data_per_Minute)  # 60 because 1 min

# We have to shedule the captor in order to record "x" data in 1 minute and not more !
try :
  while Nbr_Data < Nbr_Data_per_Minute :
    # The Adafruit_DHT librairy bring the Data of the DHT22 under the variable's name of 
    humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, GPIO_PIN)
    # Now we have the Data, we record the temperature and the humidity on file.txt
    os.chdir("/home/pi/SolarLoon_Software/Captor/Data_Captor")  # Go to the recorded data folder 
    with open("DHT22_Humidity.txt","a") as fichier :
      print >> fichier, humidity         # record humidity on file.txt
    with open("DHT22_Temperature.txt","a") as fichier2 :
      print >> fichier2, temperature     # record temperature on file.txt
    # We want to record the Pi0 time when a DHT22 data is recorded
    TIME = time.strftime("%H-%M-%S")    # take the Pi0 time 
    with open("DHT22_Time.txt","a") as fichier3 :
      print >> fichier3, TIME       # record time on file.txt
    # Wait between each recorded data (in secondes)
    time.sleep(Time_between_each_recorded_data)
    Nbr_Data +=1   

except KeyboardInterrupt :
  print("Exit")


