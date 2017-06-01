#!/bin/bash

cd /home/pi/SolarLoon_Software/Captor/Data_Captor/

truncate -s 0 GPS_Captor.txt
truncate -s 0 BMP180_Pressure.txt
truncate -s 0 BMP180_Temperature.txt
truncate -s 0 BMP180_Time.txt
truncate -s 0 DHT22_Humidity.txt
truncate -s 0 DHT22_Temperature.txt
truncate -s 0 DHT22_Time.txt
truncate -s 0 DS18B20_Temperature.txt
truncate -s 0 DS18B20_Time.txt
truncate -s 0 Time_GPS_Captor.txt


cd /home/pi/SolarLoon_Software/GPS/GPS_DATA/

truncate -s 0 Time.txt
truncate -s 0 Speed.txt
truncate -s 0 Longitude.txt
truncate -s 0 Latitude.txt
truncate -s 0 Altitude.txt


cd /home/pi/SolarLoon_Software/Raspicam/Data_Photos/

rm -rf Data_Photos
mkdir Data_Photos
