import unittest
import ble_beacon_scan
import json
from unittest.mock import patch
from unittest.mock import MagicMock

class TestDistance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ble_beacon_scan.DISTANCE_READ = 0
    
    def test_distance(self):
        res = ble_beacon_scan.distance()
        self.assertGreater(ble_beacon_scan.DISTANCE_READ,0)

class TestBluetooth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ble_beacon_scan.DEVICE_RSSI = 1

    def test_handleDiscovery(self):
        scanner = ble_beacon_scan.Scanner().withDelegate(ble_beacon_scan.ScanDelegate())
        res = scanner.scan(3)
        self.assertLessEqual(ble_beacon_scan.DEVICE_RSSI,0)

class TestSendData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ble_beacon_scan.DISTANCE_READ = 0
        ble_beacon_scan.DEVICE_RSSI = 0
    
    @patch('ble_beacon_scan.requests.post')
    def test_sendData(self,mock_post):

        mock_post.side_effect = [
            ble_beacon_scan.requests.ConnectionError('Test error'),
            MagicMock(status_code=200,headers={'content-type':"application/json"},text=json.dumps({'status':True}))]
        
        output = ble_beacon_scan.sendData(5,5)
        
        self.assertIsNone(output)
if __name__ == '__main__':
    unittest.main()
