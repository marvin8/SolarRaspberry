#!/usr/bin/env python3

import pifacecommon
import pifacecad
from threading import Barrier

class StatsDisplay(object):
	def __init__(self, cad, stats):
		self.stats = stats
		self.cad = cad
		self.cad.lcd.backlight_on()
		self.cad.lcd.blink_off()
		self.cad.lcd.cursor_off()

	def close(self):
		self.cad.lcd.clear()
		self.cad.lcd.backlight_off()

	def update(self):
		self.cad.lcd.clear()
		self.cad.lcd.write("{potential} V  ".format(
			potential=self.stats['potential']))
		self.cad.lcd.write("{energy} Wh\n".format(
			energy=self.stats['energy']))
		self.cad.lcd.write("{powernow} W  ".format(
			powernow=self.stats['powernow']))
		self.cad.lcd.write("{power5min} W".format(
			power5min=self.stats['power5min']))

if __name__ == "__main__":
	stats = {}
	stats['potential'] = 26.4
	stats['energy'] = 11200
	stats['powernow'] = 2753
	stats['power5min'] = 3214

	cad = pifacecad.PiFaceCAD()
	statsdisplay = StatsDisplay(cad, stats)
	statsdisplay.update()

	global end_barrier
	end_barrier = Barrier(2)

	# wait for button press
	switchlistener = pifacecad.SwitchEventListener(chip=cad)
	switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
	switchlistener.activate()
	end_barrier.wait()

	#exit
	statsdisplay.close()
	switchlistener.deactivate()

