#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute

# import all the module we will need
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os
import subprocess

# Define the captor's modele to use the Adafruit_DHT librairy
DHTSensor = Adafruit_DHT.DHT22
# Define the pin used for the DHT22 signal, and define it as an Input
GPIO_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)

try :
	# Go to the sender data folder 
	os.chdir("/home/pi/SolarLoon_Software/LoRa_Sending_Data") 
	time.sleep(2)
	# The Adafruit_DHT librairy bring the Data of the DHT22 under the variable's name of 
	humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, GPIO_PIN)
	HUMIDITY = humidity
	msg_Humidity = str(HUMIDITY+" %")
	subprocess.call(["./chisterapi", msg_Humidity])  

except KeyboardInterrupt :
  print("Exit")


