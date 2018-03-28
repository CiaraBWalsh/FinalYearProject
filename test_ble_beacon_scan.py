import unittest
import ble_beacon_scan
import json
from unittest.mock import patch
from unittest.mock import MagicMock

# Test to ensure that the distance is read correctly
class TestDistance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ble_beacon_scan.DISTANCE_READ = 0
    
    def test_distance(self):
        res = ble_beacon_scan.distance()
        self.assertGreater(ble_beacon_scan.DISTANCE_READ,0)

# Test to ensure that Bluetooth device discovery is handled correctly
class TestBluetooth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ble_beacon_scan.DEVICE_RSSI = 1
        ble_beacon_scan.BEACON_ADDR = '00:1b:35:11:be:8e' 

    def test_handleDiscovery(self):
        scanner = ble_beacon_scan.Scanner().withDelegate(ble_beacon_scan.ScanDelegate())
        res = scanner.scan(3)
        self.assertLessEqual(ble_beacon_scan.DEVICE_RSSI,0)

# Test to ensure that the sendData function operates correctly
class TestSendData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ble_beacon_scan.DISTANCE_READ = 0
        ble_beacon_scan.DEVICE_RSSI = 0
    
    @patch('ble_beacon_scan.requests.post')
    def test_sendData(self,mock_post):

        url = 'http://google.com'
        mock_post.return_value.status_code = 200
        
        output = ble_beacon_scan.sendData(5,5)
        
        self.assertEqual(output.status_code,200)
if __name__ == '__main__':
    unittest.main()
