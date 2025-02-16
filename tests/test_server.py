import pytest
import socket
import threading
from unittest import mock
from src.server import TCPServer
from src.alarm import Alarm
from config import settings

@pytest.fixture
def mock_alarm():
    """Fixture to create a mock Alarm instance."""
    return mock.create_autospec(Alarm)

@pytest.fixture
def tcp_server(mock_alarm):
    """Fixture to initialize and start the TCPServer."""
    server = TCPServer(alarm=mock_alarm)
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    yield server
    server.stop()
    server_thread.join()

def test_successful_authentication_and_activate_command(tcp_server, mock_alarm):
    """Test successful authentication followed by ACTIVATE command."""
    with socket.create_connection((settings.ALARM_IP, settings.ALARM_PORT)) as sock:
        sock.sendall(settings.AUTH_TOKEN.encode() + b'\n')
        response = sock.recv(1024).decode().strip()
        assert response == "AUTH_SUCCESS"

        sock.sendall("ACTIVATE".encode() + b'\n')
        response = sock.recv(1024).decode().strip()    
        assert response == "Alarm activated"
        mock_alarm.on.assert_called_once()

def test_successful_authentication_and_deactivate_command(tcp_server, mock_alarm):
    """Test successful authentication followed by DEACTIVATE command."""
    with socket.create_connection((settings.ALARM_IP, settings.ALARM_PORT)) as sock:
        sock.sendall(settings.AUTH_TOKEN.encode() + b'\n')
        response = sock.recv(1024).decode().strip()
        assert response == "AUTH_SUCCESS"

        sock.sendall("DEACTIVATE".encode() + b'\n')
        response = sock.recv(1024).decode().strip()    
        assert response == "Alarm deactivated"
        mock_alarm.off.assert_called_once()

def test_failed_authentication(tcp_server, mock_alarm):
    """Test failed authentication with incorrect token."""
    with socket.create_connection((settings.ALARM_IP, settings.ALARM_PORT)) as sock:
        sock.sendall("wrong_token".encode() + b'\n')
        response = sock.recv(1024).decode().strip()
        assert response == "AUTH_FAILURE"
        mock_alarm.on.assert_not_called()
        mock_alarm.off.assert_not_called()

def test_unknown_command_after_authentication(tcp_server, mock_alarm):
    """Test handling of unknown command after successful authentication."""
    with socket.create_connection((settings.ALARM_IP, settings.ALARM_PORT)) as sock:
        sock.sendall(settings.AUTH_TOKEN.encode() + b'\n')
        response = sock.recv(1024).decode().strip()
        assert response == "AUTH_SUCCESS"

        sock.sendall("UNKNOWN_COMMAND".encode() + b'\n')
        response = sock.recv(1024).decode().strip() 
        assert response == "Unknown command"
        mock_alarm.on.assert_not_called()
        mock_alarm.off.assert_not_called()
