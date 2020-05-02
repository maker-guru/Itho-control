#FAN CONTROLLER

import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
import time

#pin definitions (BCM numbering)
LOW_PIN = 17
HIGH_PIN = 4
TIMER_PIN = 18
MEDIUM_PIN = 27
DHT_PIN = 22
PIR_PIN = 23

#humidy sensor type
DHT_SENSOR = DHT.DHT22

#pulse width [s] for switching fan
PULSE_LENGTH = 0.2

#setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN,GPIO.IN)
GPIO.setup(HIGH_PIN,GPIO.OUT)
GPIO.setup(MEDIUM_PIN,GPIO.OUT)
GPIO.setup(LOW_PIN,GPIO.OUT)
GPIO.setup(TIMER_PIN,GPIO.OUT)


def read_humidity_temp():
	h,t = DHT.read(DHT_SENSOR,DHT_PIN)
	return h,t

def read_retry_humidity_temp(retries=15,delay_seconds=2):
	h,t = DHT.read_retry(DHT_SENSOR,DHT_PIN)
	return h,t

	
def read_pir():
	status_pir = GPIO.input(PIR_PIN)
	return status_pir

def set_fan(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(PULSE_LENGTH)
	GPIO.output(pin,GPIO.LOW)
	
def set_fan_high():
	set_fan(HIGH_PIN)
	
def set_fan_medium():
	set_fan(MEDIUM_PIN)
	
def set_fan_low():
	set_fan(LOW_PIN)
	
def set_fan_timer():
	set_fan(TIMER_PIN)

if __name__ == "__main__":
    print("fan controller" )

