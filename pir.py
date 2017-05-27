#!/usr/bin/env python

import sys
import RPi.GPIO as io
import os
import subprocess
from threading import Thread
from time import sleep

io.setmode(io.BCM)
SHUTOFF_DELAY = 60 * 5 		# Five minutes
PIR_PIN = 18       			# 12 on the board. Change this to whichever GPIO pin you use.
io.setup(PIR_PIN, io.IN)
hdmiOn = False 				# I don't want to test if the screen is on every loop. So I keep track of the state.
movmentDetected = False 

def main():
	# The global is important, otherwise Python creates a local variable just for this method.
	global movmentDetected
	global hdmiOn
	
	# There needs to be two loops, and the only way to run them at the same time is to
	# thread one of them.
	t = Thread(target=sensorWorker, args=())
	t.start()

	# Main loop checks to see if the movmentDetected variable is still false, and hdmiOn is true.
	# It checks this only after the timeout has completed.
	while True:
		movmentDetected = False #Reset the var just before this loop sleeps.
		# We don't want the screen turning off and on rapidly. 
		# And we don't want to waste electricity. 
		# So we wait five minutes to check if there was movement detected.
		sleep(SHUTOFF_DELAY) 
		# The only state we need to worry about is if the screen is on, and no movement was detected.
		if not movmentDetected and hdmiOn: 
			turn_off()

def turn_on():
	global hdmiOn
	hdmiOn = True
	subprocess.call("sh /home/pi/rpi-hdmi.sh on", shell=True)

def turn_off():
	global hdmiOn
	hdmiOn = False
	subprocess.call("sh /home/pi/rpi-hdmi.sh off", shell=True)

def sensorWorker ():
	global movmentDetected
	global hdmiOn
	
	while True:
		# Rather than continuously loop, which eats up processor time. 
		# Using the wait_for_edge reduces the processor load to around 2%. 
		# If I used a continous loop with no wait, the processor load would be 100%.
		io.wait_for_edge(PIR_PIN, io.RISING)
		# Wait for edge can be triggered by power supply fluctuations and static electricity.
		# So I wait a tenth of a second.
		sleep(.1)
		# Then test if movement is still detected.
		if io.input(PIR_PIN):
			movmentDetected = True
			if not hdmiOn:
				turn_on() # If there is movement detected, we want the screen to turn on right now.

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		io.cleanup()