# Itho-control
 Control of Itho Daalderop mechanical ventilation unit

In this project a Itho RTF remote control is hooked up with a raspberry pi to create an automated system. 





The Adafruit library is necessary for reading the DHT22 sensor.
Installing Python library for reading DHT22/AM2302 sensor
	sudo apt-get install python-dev
	git clone https://github.com/adafruit/Adafruit_Python_DHT
	cd Adafruit\_Python\_DHT && sudo python setup.py install
	
For MQTT the paho library is required. This libary can be installed with
	pip install paho-mqtt

Starting at boot
A systemd service is used to let program run when the pi boots. Copy file fanctl.service (as su) to /etc/systemd/system/fanctl.service. After copying the service can be start/stopped with
	sudo systemctl start fanctl.service
	sudo systemctl stop fanctl.service
To have it start automatically at boot:
	sudo systemctl enable fanctl.service
More info on creating services for rpi can be found at: https://www.raspberrypi.org/documentation/linux/usage/systemd.md

Status updates and measurements are available on port 6776. Each line is formatted as:
[timestamp] [fanspd] [pir sensor] [relative humidity] [temperature] [delta humidity]




