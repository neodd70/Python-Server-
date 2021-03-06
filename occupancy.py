#!/usr/bin/python
from phue import Bridge
import random
import time
import datetime
import threading


class Occupancy(object):
	"""This is to turn the Hue light on in the master bath when the PIR sensor detects motion"""
	BULB_NUMBER=3
	def __init__(self,bridge_ip,duration=180):
		self._Timer_thread = None
		self.bridge_ip = bridge_ip
		self._bridge_connect()
		self._duration = duration
		self._button_override = False
		
	def _bridge_connect(self):
		self._b = Bridge(self.bridge_ip) # Enter bridge IP here.

		#If running for the first time, press button on bridge and run with b.connect() uncommented
		self._b.connect()

	def _hue_for_given_time(self):
		"""This sets the color hue of the light for the time of day"""
		hour = datetime.datetime.now().hour
		if hour >= 23 or hour <= 7:
			return 47125 #hue blue			
		elif hour >= 8 and hour <= 22:
			return 14910 #hue white
			

	def _sat_for_given_time(self):
		"""This sets the saturation of the light for the time of day"""
		hour = datetime.datetime.now().hour
		if hour >= 23 or hour <= 7:
			return 253 #sat			
		elif hour >= 8 and hour <= 22:
			return 144 #sat
			

	def _bri_for_given_time(self):
		"""This sets the brightness of the light for the time of day"""
		hour = datetime.datetime.now().hour
		if hour >= 23 or hour <=7:
			return 7 #bri 5 percent			
		elif hour >= 8 and hour <= 22:
			return 254 #bri 100 percent
			


	def trigger(self, state):
		"""Handles the trigger event of the PIR sensor"""
		if state == 1:
			if self._button_override == True:
				pass
			else:
				self.reset_counter()
				self.motion_on()


	def button(self, state):
		"""Handles the button press event"""
		if state == 1:
			self._button_override = True
			self.reset_counter(600)#seconds
			self.motion_on()

	
	def reset_counter(self, duration=None):
		"""Resets timer if motion is detected"""
		if duration is None:
			duration = self._duration
		if self._Timer_thread is not None:
			self._Timer_thread.cancel()
			self._Timer_thread=None
		
		self._Timer_thread = threading.Timer(duration, self.motion_off)
		self._Timer_thread.start()

		
	def motion_on(self):
		"""Sets light brightness and color according to button press or PIR state"""
		lights = self._b.get_light_objects()
		if self._button_override == True:
			self._b.set_light(self.BULB_NUMBER, 'on', True, transitiontime=20)
			time.sleep(.02)
			self._b.set_light(self.BULB_NUMBER, 'bri', 254 , transitiontime=20)
			time.sleep(.02)
			self._b.set_light(self.BULB_NUMBER, 'hue', 14910 , transitiontime=20)
			time.sleep(.02)
			self._b.set_light(self.BULB_NUMBER, 'sat', 144 , transitiontime=20)
			time.sleep(.02)

		else:
			self._b.set_light(self.BULB_NUMBER, 'on', True, transitiontime=20)
			time.sleep(.02)
			self._b.set_light(self.BULB_NUMBER, 'bri', self._bri_for_given_time(), transitiontime=20)
			time.sleep(.02)
			self._b.set_light(self.BULB_NUMBER, 'hue', self._hue_for_given_time(), transitiontime=20)
			time.sleep(.02)
			self._b.set_light(self.BULB_NUMBER, 'sat', self._sat_for_given_time(), transitiontime=20)
			time.sleep(.02)

	def motion_off(self):

		lights = self._b.get_light_objects()
		self._button_override = False
		self._b.set_light(self.BULB_NUMBER, 'on', False, transitiontime=30)
		
		
if __name__ =="__main__":
    print "Starting Program"
    occupancy = Occupancy("192.168.1.130")
    occupancy.trigger(1)
    print "lights on"
#    time.sleep(5)
    occupancy.trigger(0)
    print "lights off"
    print "Master Bath Lights Are On"

