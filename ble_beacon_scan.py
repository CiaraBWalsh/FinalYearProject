from bluepy.btle import Scanner, DefaultDelegate
from statistics import mean
import requests

rssi_values = []
BEACON_UUID='4c000215e2c56db5dffb48d2b060d0f5a71096e000010002ba'

class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
                if dev.getValueText(255) == BEACON_UUID:
                    sendData(dev.rssi)
                    print("Beacon found, RSSI = %d dB" % dev.rssi)
                    rssi_values.append(dev.rssi)


def sendData(data):
        try:
                current_data = {'RSSI':data}
                r=requests.post('http://localhost/finalyear/read_data.php', data=current_data)
                print(r.text)
        except requests.ConnectionError as e:
                print(e)


def main():
        while(True):
                scanner = Scanner().withDelegate(ScanDelegate())
                scanner.scan(2.0)
                if mean(rssi_values[-3:]) >= -60:
                        print("Too close, RSSI: %d" % mean(rssi_values[-3:]))

if __name__ == "__main__":
    main()
