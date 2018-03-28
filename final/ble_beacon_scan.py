from bluepy.btle import Scanner, DefaultDelegate
import requests
import RPi.GPIO as GPIO
import time
import _thread

#Beacon Identifier
BEACON_ADDR = '00:1b:35:11:be:8e'

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17

DEVICE_RSSI = 0
DISTANCE_READ = 0

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    try:
        global DISTANCE_READ
    	#Set Trigger pin to HIGH
        GPIO.output(GPIO_TRIGGER, True)

	#Allow 0.01ms for pin config, then set Trigger pin to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        #Store starting time
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        #Store echo time
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        #Calculate difference in time
        RoundTripTime = StopTime - StartTime

        #Convert time to distance using d=s*t formula
        #Speed of sound in air is 34300 cm/s
        #Divide by 2 to convert round trip distance to single direction/true distance
        distance = (RoundTripTime * 34300) / 2

        DISTANCE_READ = distance
        return 0
    except Exception as e:
        print(e)


#Bluetooth Scanner definition
class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self)

	#Define how to handle the discovery of a new Bluetooth device
        def handleDiscovery(self, dev, isNewDev, isNewData):
		
                global DEVICE_RSSI
                #Check for specified Beacon identifier
                if (str(dev.addr) == str(BEACON_ADDR)):
                    DEVICE_RSSI = dev.rssi


def sendData(rssi,us_dist):
            try:
                current_data = {'RSSI':rssi,'Sensor':us_dist}

		#Occassionally the distance recorded can be very large due to timing errors on the RPi
		#If distance recorded is very large, double check the value
                while us_dist > 1000:
                    us_dist = distance()
	

		#URL of server to POST to
                path='http://sbsrv1.cs.nuim.ie/fyp/walsh/write_data.php'
                r=requests.post(path, data=current_data)
                return r

            except requests.ConnectionError as e:
                print(e)
            except Exception:
                pass

def main():
        #Scan for Bluetooth devices for 2 seconds
        scanner = Scanner().withDelegate(ScanDelegate())
        scanner.clear()
        scanner.start()
        while(True):
                try:
                    #Open threads to poll data
                    bt_thread = _thread.start_new_thread(scanner.process,(3.0,))
                    us_thread = _thread.start_new_thread(distance,())

                    #Sleep for 4 seconds to ensure both threads safely complete                
                    time.sleep(4)

                    #Transmit data to server for processing
                    sendData(DEVICE_RSSI,DISTANCE_READ)
                    scanner.clear()
                except Exception as e:
                    print(e)
                    return


if __name__ == "__main__":
    main()
