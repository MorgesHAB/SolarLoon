#!/usr/bin/python
#coding=utf-8
# This script will be actived each minute

# import all the module we will need
import gps
import time
import os
import RPi.GPIO as GPIO
import Adafruit_DHT
import smbus
from ctypes import c_short
import glob
import subprocess

#--------------------------------------------------------------#
# Setup the DHT22 captor  
# Define the captor's modele to use the Adafruit_DHT librairy
DHTSensor = Adafruit_DHT.DHT22
# Define the pin used for the DHT22 signal, and define it as an Input
GPIO_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)
#--------------------------------------------------------------#
# Setup the DS18B20 captor  
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

#--------------------------------------------------------------#
# Setup the BMP180 captor
DEVICE = 0x77 # Default device I2C address
 
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1 
 
def convertToString(data):
  # Simple function to convert binary data into
  # a string
  return str((data[1] + (256 * data[0])) / 1.2)

def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index] << 8) + data[index + 1]).value

def getUshort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index] << 8) + data[index + 1]

def readBmp180Id(addr=DEVICE):
  # Chip ID Register Address
  REG_ID     = 0xD0
  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)
  
def readBmp180(addr=DEVICE):
  # Register Addresses
  REG_CALIB  = 0xAA
  REG_MEAS   = 0xF4
  REG_MSB    = 0xF6
  REG_LSB    = 0xF7
  # Control Register Address
  CRV_TEMP   = 0x2E
  CRV_PRES   = 0x34 
  # Oversample setting
  OVERSAMPLE = 3    # 0 - 3
  
  # Read calibration data
  # Read calibration data from EEPROM
  cal = bus.read_i2c_block_data(addr, REG_CALIB, 22)

  # Convert byte data to word values
  AC1 = getShort(cal, 0)
  AC2 = getShort(cal, 2)
  AC3 = getShort(cal, 4)
  AC4 = getUshort(cal, 6)
  AC5 = getUshort(cal, 8)
  AC6 = getUshort(cal, 10)
  B1  = getShort(cal, 12)
  B2  = getShort(cal, 14)
  MB  = getShort(cal, 16)
  MC  = getShort(cal, 18)
  MD  = getShort(cal, 20)

  # Read temperature
  bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
  time.sleep(0.005)
  (msb, lsb) = bus.read_i2c_block_data(addr, REG_MSB, 2)
  UT = (msb << 8) + lsb

  # Read pressure
  bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
  time.sleep(0.04)
  (msb, lsb, xsb) = bus.read_i2c_block_data(addr, REG_MSB, 3)
  UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

  # Refine temperature
  X1 = ((UT - AC6) * AC5) >> 15
  X2 = (MC << 11) / (X1 + MD)
  B5 = X1 + X2
  temperature = int(B5 + 8) >> 4

  # Refine pressure
  B6  = B5 - 4000
  B62 = int(B6 * B6) >> 12
  X1  = (B2 * B62) >> 11
  X2  = int(AC2 * B6) >> 11
  X3  = X1 + X2
  B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

  X1 = int(AC3 * B6) >> 13
  X2 = (B1 * B62) >> 16
  X3 = ((X1 + X2) + 2) >> 2
  B4 = (AC4 * (X3 + 32768)) >> 15
  B7 = (UP - B3) * (50000 >> OVERSAMPLE)

  P = (B7 * 2) / B4

  X1 = (int(P) >> 8) * (int(P) >> 8)
  X1 = (X1 * 3038) >> 16
  X2 = int(-7357 * P) >> 16
  pressure = int(P + ((X1 + X2 + 3791) >> 4))

  return (temperature/10.0,pressure/100.0)  


#--------------------------------------------------------------#
# Setup the LoRa GPS Hat    
# Read on the localhost 2947 port (gpsd)
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Define vrariable how would count the number of GPS Data
Nbr_GPS_Data = 0
# Define the number of Data you want to record in 1 min
Nbr_Data_per_Minute = 4
Time_between_each_recorded_data = int(60 / Nbr_Data_per_Minute)  # 60 because 1 min

FIRST_TIME = True
Check_if_all_msg = False
Nbr_received_DATA = 0
#--------------------------------------------------------------#


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
                 if Check_if_all_msg == False :
                    if hasattr(report, 'time') :
                      GPSTIME = str(report.time)
                      Nbr_received_DATA +=1
                    if hasattr(report, 'speed') :
                      SPEED = str(report.speed * gps.MPS_TO_KPH)
                      Nbr_received_DATA +=1
                    if hasattr(report, 'lon') :
                      LONGITUDE = str(report.lon)
                      Nbr_received_DATA +=1
                    if hasattr(report, 'lat') :
                      LATITUDE = str(report.lat)
                      Nbr_received_DATA +=1
                    if hasattr(report, 'alt') :
                      ALTITUDE = str(report.alt)
                      Nbr_received_DATA +=1
                    if Nbr_received_DATA == 5 :
                      Check_if_all_msg = True
                      Nbr_received_DATA = 0
                    if Nbr_received_DATA != 5 :
                      Nbr_received_DATA = 0
                    if Nbr_received_DATA == 5 :
                      Check_if_all_msg = True
                      Nbr_received_DATA = 0
                    if Nbr_received_DATA != 5 :
                      Nbr_received_DATA = 0
                    if Check_if_all_msg == True :
                      # The Adafruit_DHT librairy bring the Data of the DHT22 under the variable's name of 
                      humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, GPIO_PIN)
                      HUMIDITY = str(humidity)
                      msg_Humidity = str(HUMIDITY+" %")
                      # The function readBmp180() bring the Data of the BMP180 
                      #under the variable's name of 
                      (temperature,pressure) = readBmp180()
                      PRESSURE = str(pressure)
                      msg_Pressure = str(PRESSURE+" hPa")
                      # The function read_temp() bring the Data of the DS18B20
                      TEMPERATURE = str(read_temp())
                      msg_Temperature = TEMPERATURE+" °C"
                      # We send the GPS Data to the programme C++ how send the message by radio
                      # Warning, the order GPSTIME, SPEED, ... plays a role 
                      subprocess.call(["./chisterapi", GPSTIME, SPEED, LONGITUDE, LATITUDE, ALTITUDE, msg_Temperature, msg_Pressure, msg_Humidity])
                      Check_if_all_msg = False
               Nbr_GPS_Data +=1
        
    except KeyError:
       pass
    except KeyboardInterrupt:
      quit()
      print("Exit")
    except StopIteration:
       session = None
       print "GPSD has terminated"

