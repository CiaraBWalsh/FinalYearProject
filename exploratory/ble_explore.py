from bluepy.btle import Scanner, DefaultDelegate

#Beacon Identifier
BEACON_ADDR = '00:1b:35:11:be:8e'

#Bluetooth Scanner definition
class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self)

	#Define how to handle the discovery of a new Bluetooth device
        def handleDiscovery(self, dev, isNewDev, isNewData):
		
                #Check for specified Beacon identifier
                if (str(dev.addr) == str(BEACON_ADDR)):
                    if(dev.rssi > -80):
                        print("Warning ", dev.rssi)
                    else:
                        print("Okay ", dev.rssi)

def main():
        #Scan for Bluetooth devices for 2 seconds
        scanner = Scanner().withDelegate(ScanDelegate())
        scanner.scan(200.0)

if __name__ == "__main__":
    main()
