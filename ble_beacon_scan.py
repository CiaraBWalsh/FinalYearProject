from bluepy.btle import Scanner, DefaultDelegate
from statistics import mean
import requests
import RPi.GPIO as GPIO
import time

rssi_values = []
BEACON_UUID='4c000215e2c56db5dffb48d2b060d0f5a71096e000010002ba'

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
        	StartTime = time.time()

	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back

	distance = (TimeElapsed * 34300) / 2

	return distance


class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
                if dev.getValueText(255) == BEACON_UUID:
                    sendData(dev.rssi,distance())
                    print("Beacon found, RSSI = %d dB" % dev.rssi)
                    rssi_values.append(dev.rssi)


def sendData(rssi,us_dist):
        try:
                current_data = {'RSSI':rssi}
		print(us_dist)
                path='http://sbsrv1.cs.nuim.ie/fyp/walsh/read_data.php'    #the url you want to POST to
                r=requests.post(path, data=current_data)
                #print(r.text)
        except requests.ConnectionError as e:
                print(e)


def main():
        while(True):
                scanner = Scanner().withDelegate(ScanDelegate())
                scanner.scan(2.0)

if __name__ == "__main__":
    main()
