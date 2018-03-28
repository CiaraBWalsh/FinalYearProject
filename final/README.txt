***README***

The source code for this project may be found in its entirety on GitHub at the following link:
https://github.com/CiaraBWalsh/FinalYearProject

The files contained within this repository are organised into 2 sub folders, final and exploratory.
The final folder contains the code used in the finalised version of this project, and are described as follows:
		ble_beacon_scan.py - The sensor data collection script for the RPi3
		index.html - User Interface
		read_data.php - Data analysis script
		write_data.php - Server script to convert incoming JSON data to a MongoDB document
		startup.sh - Bash script wrapper for ble_beacon_scan.py to allow it to be run through a crontab
		test_ble_beacon_scan.py - Unit tests
		
The exploratory folder contains all the code developed during the exploratory work portion of the project development.

***Instructions***

Running this project involves the configuration of a Raspberry Pi 3 running Raspbian Jessie to be able to use Bluetooth Low Energy.
This requires the installation of several packages, including blueZ.

Install the required packages as follows:
$ sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev blueZ

The code also makes use of the bluepy Python library, to install this run:
$ sudo apt-get install python3-pip
$ sudo pip3 install bluepy

Follow the circuit diagram provided in the appendices to connect the ultrasonic sensor.

The project also requires a server with Apache and MongoDB installed.

To run this project, install the python script onto the RPi3 and the PHP/HTML scripts onto the server.

In a RPi3 terminal run the following:
$ sudo hcitool hci0 up
$ sudo python3 ble_beacon_scan.py
 
Open the index.html file in a web browser.
