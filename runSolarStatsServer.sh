#!/bin/bash

while true; do
	tmux new-session -d -s SolarStats ./ShowSolarStatsServer.py --port 8000
	pid=$(ps aux | grep Solar | grep -v grep | cut -b 08-14 | tr -s [:blank:])
	
	sleep 30m
	kill $pid
done
