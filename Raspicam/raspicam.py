#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute

# First write "sudo apt-get install picamera-??????" on the raspbery pi terminal

# import all the module we will need
import time 
import os
import RPi.GPIO as GPIO
import picamera
from random import randrange

# As we don't see if the camera is capturing a photo, we will 
# shedule a LED that will light on when a picture is taking

# So we setup the GPIO of the LED
GPIO_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)  # define this pin as an output

# Define a vrariable how would count the number of Data
Nbr_Pictures = 0
# Define the number of Data you want to record in 1 min
Nbr_Pictures_per_Minute = 12
Time_between_each_recorded_pictures = int(60 / Nbr_Pictures_per_Minute)  # 60 because 1 min
Time_the_LED_is_on = 3  # secondes

# setup the camera with the module picamera
camera=picamera.PiCamera()

try :
	while Nbr_Pictures < Nbr_Pictures_per_Minute :
		 # Now we have the Data, we record the temperature and the humidity on file.txt
		 os.chdir("/home/pi/SolarLoon_Software/Raspicam/Data_Photos")  # Go to the recorded photos folder 
		 random_number = str(randrange(999)) # ***
		 # We will name the picture with the time when the pictures is taking
		 Time_picture = str(time.strftime('%H%M%S'))
		 Name_of_pictures = Time_picture+"_"+random_number
		 camera.capture("{0}.jpg".format(Name_of_pictures))  # take a picture
		 # Now we shedule the LED 
		 GPIO.output(GPIO_PIN, GPIO.HIGH)
		 time.sleep(Time_the_LED_is_on)
		 GPIO.output(GPIO_PIN, GPIO.LOW)
		 time.sleep(Time_between_each_recorded_pictures - Time_the_LED_is_on)
		 Nbr_Pictures +=1

except KeyboardInterrupt :
  print("Exit")
  GPIO.cleanup()

# ***
# We will name the picture with the time of the Pi 0, but if the raspberry Pi reboot,
# the time go back a bit, so it's posssible that the new pictures have the same name 
# as the older and so errase the old pictures. So we will put a random number after 
# the name of the picture in order to never take the risk to have the same name of pictures !  