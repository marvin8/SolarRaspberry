#!/usr/bin/env python3

import rpyc

if __name__ == "__main__":
	c = rpyc.connect("localhost", 8000)
	stats = {}
	stats['potential'] = 26.4
	stats['energy'] = 11200
	stats['powernow'] = 2753
	stats['power5min'] = 3214

	c.root.update_stats(stats)
