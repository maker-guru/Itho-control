#automatic - test

import fancntl as fan
import time

pir_det = 0
fan_spd = 1

h_prev = None
delta_h = None
dh_A = 0.5


def my_round(a,n):
	if a is not None:
		return round(a,n)
	else:
		return a

while True:
	pir_det = fan.read_pir()
	h,t = fan.read_retry_humidity_temp()
	if h is not None:
		if h_prev is not None:
			if delta_h is not None:
				delta_h = dh_A*delta_h + (1-dh_A)*(h-h_prev)
			else:
				delta_h = h - h_prev
		else:
			h_prev = h
		h = round(h,2)
	if t is not None:
		t = round(t,2)

	print(pir_det,h,t,my_round(delta_h,2))

	if h is not None:
		if h>90 and fan_spd!=3:
			fan.set_fan_high()
			fan_spd=3
			print("fan high")
		elif h>80 and h<=90 and fan_spd!=2:
			fan.set_fan_medium()
			fan_spd=2
			print("fan med")
		if h<75 and fan_spd!=1:
			fan.set_fan_low()
			fan_spd=1
			print("fan low")
	time.sleep(2)
	
	
			
			