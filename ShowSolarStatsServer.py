#!/usr/bin/env python3

import pifacecommon
import pifacecad
from threading import Barrier

import rpyc
from rpyc.utils.server import ThreadedServer

class StatsDisplay(object):
	def __init__(self, cad):
		self.cad = cad
		self.cad.lcd.backlight_on()
		self.cad.lcd.blink_off()
		self.cad.lcd.cursor_off()

	def close(self):
		self.cad.lcd.clear()
		self.cad.lcd.backlight_off()

	def update(self, stats):
		self.stats = stats
		self.cad.lcd.clear()
		self.cad.lcd.write("{potential} V  ".format(
			potential=self.stats['potential']))
		self.cad.lcd.write("{energy} Wh\n".format(
			energy=self.stats['energy']))
		self.cad.lcd.write("{powernow} W  ".format(
			powernow=self.stats['powernow']))
		self.cad.lcd.write("{power5min} W".format(
			power5min=self.stats['power5min']))

class DisplayServer(rpyc.Service):

	def __init__(self, service):
		self.cad=pifacecad.PiFaceCAD()
		self.display = StatsDisplay(self.cad)
		pass

	def on_connect(self):
		print("Connected")
		pass

	def on_disconnect(self):
#		self.display.close()
		print("Disconnceted")
		pass

	def exposed_update_stats(self, stats):
		print("Disply to be updated with stats: ", stats)
		self.display.update(stats)
		print("Disply updated!")


if __name__ == "__main__":

	hostPort = 8000

	t = ThreadedServer(DisplayServer, port=hostPort)
	t.start()

