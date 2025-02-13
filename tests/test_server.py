import unittest
from unittest.mock import patch, MagicMock
from src.server import TCPServer
from src.alarm import Alarm

class TestTCPServer(unittest.TestCase):
    @patch('src.server.socket.socket')
    def test_handle_client_auth_success_activate(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_client_socket.recv.side_effect = [b'valid_token\n', b'ACTIVATE\n']
        mock_socket.return_value.accept.return_value = (mock_client_socket, ('127.0.0.1', 12345))

        alarm = MagicMock(spec=Alarm)
        server = TCPServer(alarm=alarm)
        server.handle_client(mock_client_socket)

        mock_client_socket.send.assert_any_call(b"AUTH_SUCCESS\n")
        mock_client_socket.send.assert_any_call(b"Alarm activated\n")
        alarm.on.assert_called_once()

    @patch('src.server.socket.socket')
    def test_handle_client_auth_failure(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_client_socket.recv.return_value = b'invalid_token\n'
        mock_socket.return_value.accept.return_value = (mock_client_socket, ('127.0.0.1', 12345))

        alarm = MagicMock(spec=Alarm)
        server = TCPServer(alarm=alarm)
        server.handle_client(mock_client_socket)

        mock_client_socket.send.assert_called_with(b"AUTH_FAILURE\n")
        alarm.on.assert_not_called()

if __name__ == '__main__':
    unittest.main()
