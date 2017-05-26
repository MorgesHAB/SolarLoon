SolarLoon_Software \n
Edited by Lionel Isoz \n
For the MorgesHAB project \n
https://morgeshab.wordpress.com/  \n

*** If you never touch a raspberry Pi --> explications at the end  \n

So first activate the differents communications protocols :

	sudo raspi-config

Activate 1-wire, SPI, I2C and the camera, in interfacing options 
	
	sudo nano /boot/config.txt
write :
	
	dtparam=i2c_arm=on
	dtoverlay=w1-gpio,gpiopin=21  #changer le 1-wire à la pin 40 (GPIO21)
Save :
	
	Ctl+X , Y , Enter
Then :
	
	sudo reboot

Then put the Ethernet cable on your raspberry Pi 0 (With an RJ45-USB adapter)
Make sure your raspberry is upgrade with :
	
	sudo apt-get update
	sudo apt-get upgrade -y


For the camera module, we need to install a module :
	
	sudo apt-get install python-picamera


For the BMP180 :
	
	sudo apt-get install python_smbus_i2c_tools -y


---------------------------------------------------------------------

For the GPS LoRa Hat :
Source : http://wiki.dragino.com/index.php?title=Getting_GPS_to_work_on_Raspberry_Pi_2_Model_B

Enable the UART :
By default the UART is enabled to allow you to connect a terminal window and login, We needed to disable this to free it up for the GPS Module. Edit the boot options to change the UART so it doesnt provide a terminal connection by default: 
	sudo nano /boot/cmdline.txt 


Change: 
	
	dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 
	console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline 
	rootwait 

to: 
	
	dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 
	rootfstype=ext4 elevator=deadline rootwait 

Then write :

	sudo systemctl stop serial-getty@ttyAMA0.service
	sudo systemctl disable serial-getty@ttyAMA0.service

And :

	sudo reboot

Install GPSD :

	sudo apt-get install gpsd gpsd-clients python-gps 

(Warning to have upgrade the raspberry Pi)

Then :

	sudo systemctl stop gpsd.socket
	sudo systemctl disable gpsd.socket

Run gpsd :

	sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock

Or :

	sudo bash /home/pi/SolarLoon_Software/GPS/ACTIVATE_GPS.sh

You can test if you receive GPS with (Go outside ! ;-):
	
	cgps -s

---------------------------------------------------------------------

Make sure you have install wiringpi and git with :
	
	sudo apt-get install wiringpi
	sudo apt-get install git


Now you have done all the configurations, install all the software :

	sudo git clone https://github.com/MorgesHAB/SolarLoon_Software/

Then activate all the programmes :

Go in root :
	
	sudo su -

Edited the crontab :
	
	crontab -e (2)

Add these lignes to the cron at the end of the file :

	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Captor/BMP180.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Captor/DHT22.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Captor/DS18B20_GPS.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Raspicam/raspicam.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/LoRa_Sending_Data/DATA_Sender_GPS_Captor/Humidity_Transmission.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/LoRa_Sending_Data/DATA_Sender_GPS_Captor/Pressure_Transmission.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/LoRa_Sending_Data/DATA_Sender_GPS_Captor/Temperature_Transmission.py

Then activate script on the boot :
	
	sudo nano /etc/rc.local

Add these lignes juste befor the "exit 0":

	sudo bash /home/pi/SolarLoon_Software/GPS/ACTIVATE_GPS.sh
	sudo python /home/pi/SolarLoon_Software/GPS/GPS_RECORDER.py
	sudo python /home/pi/SolarLoon_Software/LoRa_Sending_Data/DATA_Sender_GPS_Captor/GPS_Transmission.py
	sudo python /home/pi/SolarLoon_Software/RTC_Pi0_GPS/RTC_Pi0_GPS.py

maybe 
	
	sudo ./home/pi/SolarLoon_Software/LoRa_Sending_Data/chisterapi

For the DHT22 we still need a librairy :
Go the the right direction :
	
	cd home/pi/SolarLoon_Software/Captor/

Then install the librairy in GitHub :
	
	git clone https://github.com/adafruit/Adafruit_Python_DHT.git 
	cd Adafruit_Python_DHT/
	sudo python setup.py install  

And Now it's finish !


*** If you never touch a raspberry Pi, I will explain you from the start
So fisrt, we need to install a operating system.