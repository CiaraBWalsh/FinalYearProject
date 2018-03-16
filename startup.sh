#!/bin/sh
# startup.sh
# Start up final year project

sleep 60
sudo hciconfig hci0 up
cd /home/pi/final_year_project

echo "" > logs/cronlog
echo "" > logs/blelog
echo "" > logs/bashlog

exit_code=0

while true; do
	sudo python3 ble_beacon_scan.py >> logs/blelog
	$exit_code = $?
	echo $exit_code >> logs/bashlog
done
