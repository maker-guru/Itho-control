#automatic - test

import logging
import fancntl as fan
import time
import msgrelay

pir_det = 0
fan_spd = 1

#for filterning humidity changes
h_prev = None
delta_h = None
dh_A = 0.5

#constants for controlling fan 
RH_HIGH = 90  		#switch level for high fan
RH_MEDIUM = 80  	#switch level medium fan
RH_LOW = 70			#switch level low fan
RH_HYSTERESIS = 10	#hysteresis for switching fan
CNTL_PERIOD = 3		#desired control period in seconds


#constants for relaying messages
PORT = 6776
HOSTNAME = '0.0.0.0'


def my_round(a,n):
	if a is not None:
		return round(a,n)
	else:
		return a


if __name__ == '__main__':
	#setup logging
	logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(message)s')
	logger = logging.getLogger(__name__)
	
	#create msg relay to make status info available over port
	mr = msgrelay.MsgRelay(HOSTNAME,PORT)
	
	while True:
		# read sensor data
		logger.debug("start reading sensor data")

		# timestamp measurement
		t_meas = time.time()	
		
		#read sensors
		pir_det = fan.read_pir()
		h,t = fan.read_retry_humidity_temp(2,0.5)
		logger.debug("sensor data read in %s [s]",round(time.time()-t_meas,2))
		if h is not None:
			if h_prev is not None:
				if delta_h is not None:
					delta_h = dh_A*delta_h + (1-dh_A)*(h-h_prev)
				else:
					delta_h = h - h_prev
			h_prev = h
			h = round(h,2)
		if t is not None:
			t = round(t,2)
			
		#determine control action
		logger.debug("determine control action")
		if h is not None:
			if fan_spd == 1:
				if h>RH_HIGH:
					fan.set_fan_high()
					fan_spd = 3
					logger.info("fan high")
				elif h>RH_MEDIUM:
					fan.set_fan_medium()
					fan_spd = 2
					logger.info("fan medium")
			elif fan_spd == 2:
				if h>RH_HIGH:
					fan.set_fan_high()
					fan_spd = 3
					logger.info("fan high")
				elif h<RH_MEDIUM - RH_HYSTERESIS:
					fan.set_fan_low()
					fan_spd = 1
					logger.info("fan low")
			elif fan_spd ==3:
				if h<RH_HIGH - RH_HYSTERESIS:
					fan.set_fan_medium()
					fan_spd = 2
					logger.info("fan medium")
			else:
				logger.error("unknown state")
				
		#log sensor data and actions
		meas = time.strftime("%H:%M:%S",time.localtime(t_meas)) + " " + str(fan_spd) + " " + str(pir_det) + " " + str(h) +" "+ str(t) + " " + str(my_round(delta_h,1))
		logger.info(meas)
		meas = meas + " \r\n"
		mr.relay_msg(meas.encode('utf-8'))

		#accept connections 
		delta_t = t_meas + CNTL_PERIOD - time.time()
		if (delta_t>0):
			mr.accept_conn(delta_t)   #timeout set match remainder of control period
		
	#shut down message relay
	logger.info("closing connections")
	mr.close_conn()
	
			
			