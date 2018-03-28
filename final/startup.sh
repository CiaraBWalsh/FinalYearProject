#!/bin/sh
# startup.sh
# Start up final year project

# Sleep to ensure system is fully booted before running
sleep 60

# Turn on Bluetooth
sudo hciconfig hci0 up
cd /home/pi/final_year_project

# Create log files
echo "" > logs/cronlog
echo "" > logs/blelog
echo "" > logs/bashlog

exit_code=0

# Run project code
while true; do
	sudo python3 ble_beacon_scan.py >> logs/blelog
	$exit_code = $?
	echo $exit_code >> logs/bashlog
done
