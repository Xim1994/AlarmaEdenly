import unittest
from unittest.mock import patch, MagicMock
from src.network import NetworkManager

class TestNetworkManager(unittest.TestCase):
    @patch('src.network.network.WLAN')
    def test_connect_success(self, mock_wlan):
        mock_instance = MagicMock()
        mock_instance.isconnected.return_value = False
        mock_wlan.return_value = mock_instance

        network_manager = NetworkManager()
        network_manager.connect()

        mock_instance.active.assert_called_with(True)
        mock_instance.connect.assert_called_once()

    @patch('src.network.network.WLAN')
    def test_connect_failure(self, mock_wlan):
        mock_instance = MagicMock()
        mock_instance.isconnected.return_value = False
        mock_wlan.return_value = mock_instance

        network_manager = NetworkManager()
        with self.assertRaises(ConnectionError):
            network_manager.connect()

if __name__ == '__main__':
    unittest.main()
