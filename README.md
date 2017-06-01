SolarLoon_Software  
Edited by Lionel Isoz  
For the MorgesHAB project  
https://morgeshab.wordpress.com/  

Hi eveyryone,  
These repository is used for the MorgesHAB project, a high altitude balloon project.  
These programmes would be used to measure the temperature, the humidity and the pressure in the stratosphere. We will also have use a GPS LoRa Hat how would record the GPS coordinates and send it by radio.  
A raspicam module V2 is also aboard.  
Check our website for more informations --> https://morgeshab.wordpress.com/  

So if you want to do the same as us, here is the instructions :  
For the Hardware, you will need :  

	Raspbery Pi 0
	SD card (32GB)
	DHT22 (Humidity & temperature captor)
	BMP180 (Pressure & temperature captor)
	DS18B20 (Temperature captor)
	Raspicam V2 (Warning: connection to Pi0)
	2 LoRa GPS Hat (sender & receiver)
	Battery (outpout 5V)
	Monitpor, mouse, keyboard
	Internet connection (RJ45-USB adapter)

*** If you never touch a raspberry Pi --> explications at the end  

So first activate the differents communications protocols :

	sudo raspi-config

Activate 1-wire, SPI, I2C and the camera, in interfacing options 
And modify this file :
	
	sudo nano /boot/config.txt
write :
	
	dtparam=i2c_arm=on
	dtoverlay=w1-gpio,gpiopin=21  # change the 1-wire to the pin 40 (GPIO21)
Save :
	
	Ctl+X --> Y --> Enter
Then 
	
	sudo reboot

Then put the Ethernet cable on your raspberry Pi 0 (With an RJ45-USB adapter)
Make sure your raspberry is upgrade with :
	
	sudo apt-get update
	sudo apt-get upgrade -y


For the camera module, we need to install a module :
	
	sudo apt-get install python-picamera


For the BMP180 :
	
	sudo apt-get install python_smbus_i2c_tools -y

For the DHT22 :
	
	cd /homepi/SolarLoon_Software/Captor/Adafruit_Python_DHT/
	sudo apt-get update
	sudo apt-get install build-essential python-dev python-openssl
	sudo python setup.py install


---------------------------------------------------------------------

For the GPS LoRa Hat :
Source : http://wiki.dragino.com/index.php?title=Getting_GPS_to_work_on_Raspberry_Pi_2_Model_B

Enable the UART :
By default the UART is enabled to allow you to connect a terminal window and login,  
We needed to disable this to free it up for the GPS Module.  
Edit the boot options to change the UART so it doesnt provide a terminal connection by default:  
	
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

Now you have to compile some programmes so go in this directory 

	cd /home/pi/SolarLoon_Software/LORA_Sender
	make
If there isn't something to make, 

	sudo nano /src/main.cpp 
	Enter , Ctrl X , Y, Enter 
	cd .. 
	make

Then activate all the programmes :

Go in root :
	
	sudo su -

Edited the crontab (If it's the first time, choose the open's mode, take the mode 2)
	
	crontab -e 

Add these lignes to the cron at the end of the file :

	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Captor/BMP180.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Captor/DHT22.py
	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Captor/DS18B20_GPS.py

	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/GPS/GPS_RECORDER.py

	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/Raspicam/raspicam.py

	*/1  *  *  *  *  python /home/pi/SolarLoon_Software/LORA_Sender/MAIN_SENDER.py


Then modify this file to activate script on the boot :
	
	sudo nano /etc/rc.local

Add these lignes juste befor the "exit 0":

	sudo bash   /home/pi/SolarLoon_Software/GPS/ACTIVATE_GPS.sh
	(sudo python /home/pi/SolarLoon_Software/RTC_Pi0_GPS/RTC_Pi0_GPS.py)

And Now it's finish !

---------------------------------------------------------------------

*** If you never touch a raspberry Pi, I will explain you from the start  
So fisrt, we need to install a operating system.  
I recommend to use Raspbian Jessie Lite  
This one --> https://www.raspberrypi.org/downloads/raspbian/  
When you have donwloaded it, unzip it and write the file.img on the SD card (use Win32 disk imager for example)  
Next connect a monitor (with the HDMI port), a mouse, a keyboard and put on the electrical cable (5V)  
The Raspberry Pi will start and if all right, you will have to put the user name and the password  

	user name : pi
	password : raspberry

Warning, if your keyboard is in qwertz you will have to put "raspberrz" for the password  
To change it :
	
	sudo raspi-config
	Localisations options
	Change keyboard layout
	choose your keyboard