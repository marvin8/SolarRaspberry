#!/usr/bin/env python3

import argparse
import pifacecommon
import pifacecad
import rpyc
from rpyc.utils.server import ThreadedServer

parser = argparse.ArgumentParser(description="Display Server to accept solar data from client to show on display")
parser.add_argument("--port", action="store", default="8000", type=int)
args = parser.parse_args()


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
		self.cad.lcd.write("{potential:>4} V  ".format(
			potential=self.stats['potential']))
		self.cad.lcd.write("{energy:>5} Wh\n".format(
			energy=self.stats['energy']))
		self.cad.lcd.write("{powernow:>4} W  ".format(
			powernow=self.stats['powernow']))
		self.cad.lcd.write("{power5min:>5} W".format(
			power5min=self.stats['power5min']))

class DisplayServer(rpyc.Service):

	def __init__(self, service):
		self.cad=pifacecad.PiFaceCAD()
		self.display = StatsDisplay(self.cad)
		pass

	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def exposed_update_stats(self, stats):
		self.display.update(stats)


if __name__ == "__main__":

	t = ThreadedServer(DisplayServer, port=args.port)
	t.start()

