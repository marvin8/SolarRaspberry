#!/bin/bash

restartEvery=$1

while true; do
	/usr/bin/tmux new-session -d -s SolarStats ./ShowSolarStatsServer.py --port 8000
	pid=$(/bin/ps aux | /bin/grep Solar | /bin/grep python3 | /usr/bin/cut -b 08-14 | /usr/bin/tr -s [:blank:])
	
	/bin/sleep $restartEvery
	/bin/kill $pid
	/bin/sleep 5s
done
