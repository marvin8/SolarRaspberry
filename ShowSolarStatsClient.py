#!/usr/bin/env python3

import argparse
import rpyc

parser = argparse.ArgumentParser(description="Client to send solar data to Raspberry Pi to display")
parser.add_argument("--server", action="store", default="localhost")
parser.add_argument("--port", action="store", default="8000", type=int)
parser.add_argument("--potential", action="store", required=True)
parser.add_argument("--energy", action="store", required=True)
parser.add_argument("--powernow", action="store", required=True)
parser.add_argument("--power5min", action="store", required=True)
args = parser.parse_args()

if __name__ == "__main__":
	c = rpyc.connect(args.server, args.port)
	stats = {}
	stats['potential'] = args.potential
	stats['energy'] = args.energy
	stats['powernow'] = args.powernow
	stats['power5min'] = args.power5min

	c.root.update_stats(stats)
