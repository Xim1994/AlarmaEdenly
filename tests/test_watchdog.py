import unittest
from unittest.mock import patch, MagicMock
from src.watchdog import Watchdog
from src.alarm import Alarm

class TestWatchdog(unittest.TestCase):
    @patch('src.watchdog.socket.create_connection')
    def test_check_server_success(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b'PONG'
        mock_create_connection.return_value.__enter__.return_value = mock_socket

        alarm = MagicMock(spec=Alarm)
        watchdog = Watchdog(alarm=alarm)
        watchdog.check_server()

        alarm.on.assert_not_called()

    @patch('src.watchdog.socket.create_connection')
    def test_check_server_failure(self, mock_create_connection):
        mock_create_connection.side_effect = Exception("Connection failed")

        alarm = MagicMock(spec=Alarm)
        watchdog = Watchdog(alarm=alarm)
        watchdog.check_server()

        alarm.on.assert_called_once()

if __name__ == '__main__':
    unittest.main()
