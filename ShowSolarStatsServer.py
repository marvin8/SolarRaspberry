#!/usr/bin/env python3

import pifacecommon
import pifacecad
from threading import Barrier

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time

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


class ListeningServer(BaseHTTPRequestHandler):

	#	GET is for clients geting the predi
	def do_GET(self):
		self.send_response(200)
		self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

	#	POST is for submitting data.
	def do_POST(self):

		print( "incomming http: ", self.path )

		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		print("headers: ", self.headers)
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		parseQS = urllib.parse.parse_qs(post_data.decode('UTF-8'))
		print("parseQS: ", parseQS)
		print("potential: ", parseQS['potential'][0])
		print("energy: ", parseQS['energy'][0])
		print("powernow: ", parseQS['powernow'][0])
		print("power5min: ", parseQS['power5min'][0])
	
		self.send_response(200)


if __name__ == "__main__":
	stats = {}
	stats['potential'] = 26.4
	stats['energy'] = 11200
	stats['powernow'] = 2753
	stats['power5min'] = 3214

	hostName = ""
	hostPort = 8000

	cad = pifacecad.PiFaceCAD()
	statsdisplay = StatsDisplay(cad)
	statsdisplay.update(stats)

#	server = HTTPServer((hostName, hostPort), ListeningServer(statsdisplay))
	server = HTTPServer((hostName, hostPort), ListeningServer)

	server.serve_forever()

	global end_barrier
	end_barrier = Barrier(2)

	# wait for button press
	switchlistener = pifacecad.SwitchEventListener(chip=cad)
	switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
	switchlistener.activate()
	end_barrier.wait()

	#exit
	server.server_close()
	statsdisplay.close()
	switchlistener.deactivate()

