#!/usr/bin/python
from phue import Bridge
import random
import time
import datetime
import threading


class Occupancy(object):
	"""This is to turn the Hue light on in the master bath when the PIR sensor detects motion"""
	def __init__(self,bridge_ip,duration=10):
		self._Timer_thread = None
		self.bridge_ip = bridge_ip
		self._bridge_connect()
		self._duration = duration
		
	def _bridge_connect(self):
		self._b = Bridge(self.bridge_ip) # Enter bridge IP here.

		#If running for the first time, press button on bridge and run with b.connect() uncommented
		self._b.connect()

	def _hue_for_given_time(self):
		"""This sets the color hue of the light for the time of day"""
		hour = datetime.datetime.now().hour
		if hour >= 23 and hour <= 7:
			return 47125 #hue blue
		elif hour >= 8 and hour <= 22:
			return 14910 #hue red

	def _sat_for_given_time(self):
		"""This sets the saturation of the light for the time of day"""
		hour = datetime.datetime.now().hour
		if hour >= 23 and hour <= 7:
			return 253 #sat 
		elif hour >= 8 and hour <= 22:
			return 144 #sat

	def _bri_for_given_time(self):
		"""This sets the brightness of the light for the time of day"""
		hour = datetime.datetime.now().hour
		if hour >= 23 and hour <= 7:
			return 7 #bri 5 percent
		elif hour >= 8 and hour <= 22:
			return 254 #bri 100 percent


	def trigger(self, state):
		"""Handles the trigger event of the PIR sensor"""
		if state == 1:
			self.motion_on()
			self.reset_counter()

	
	def reset_counter(self):
		"""Resets timer if motion is detected"""
		if self._Timer_thread is not None:
			self._Timer_thread.cancel()
			self._Timer_thread=None
		
		self._Timer_thread = threading.Timer(self._duration, self.motion_off)
		self._Timer_thread.start()

		
		

	def motion_on(self):
		
		lights = self._b.get_light_objects()

		self._b.set_light(5, 'on', True, transitiontime=0)
		self._b.set_light(5, 'bri', self._bri_for_given_time(), transitiontime=0)
		self._b.set_light(5, 'hue', self._hue_for_given_time(), transitiontime=0)
		self._b.set_light(5, 'sat', self._sat_for_given_time(), transitiontime=0)

	def motion_off(self):

		lights = self._b.get_light_objects()

		self._b.set_light(5, 'on', False, transitiontime=0)
		
		
if __name__ =="__main__":
    print "Starting Program"
    occupancy = Occupancy("192.168.1.130")
    occupancy.trigger(1)
    print "lights on"
#    time.sleep(5)
    occupancy.trigger(0)
    print "lights off"
    print "Master Bath Lights Are On"

