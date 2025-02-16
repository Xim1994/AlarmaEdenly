import pytest
from unittest import mock
from src.watchdog import Watchdog
from src.alarm import Alarm

@pytest.fixture
def mock_alarm():
    """Creates a mock for the Alarm class."""
    return mock.Mock(spec=Alarm)

@pytest.fixture
def watchdog(mock_alarm):
    """Creates an instance of Watchdog with the mock Alarm."""
    return Watchdog(alarm=mock_alarm)

@mock.patch('src.watchdog.socket.create_connection', side_effect=OSError("Server unreachable"))
@mock.patch('src.watchdog.time.sleep', return_value=None)
def test_server_unreachable(mock_sleep, mock_create_connection, watchdog, mock_alarm):
    """
    Simulates an unreachable server and verifies that the alarm is activated.
    """
    def stop_after_one_iteration(*args, **kwargs):
        """Stops the watchdog after one iteration."""
        watchdog.running = False

    mock_sleep.side_effect = stop_after_one_iteration

    watchdog.check_server()

    mock_alarm.on.assert_called_once()

@mock.patch('src.watchdog.socket.create_connection')
@mock.patch('src.watchdog.time.sleep', return_value=None)
def test_incorrect_server_response(mock_sleep, mock_create_connection, watchdog, mock_alarm):
    """
    Simulates an incorrect server response and verifies that the alarm is activated.
    """
    mock_socket = mock.Mock()
    mock_socket.recv.return_value = b'INVALID'
    mock_create_connection.return_value.__enter__.return_value = mock_socket

    def stop_after_one_iteration(*args, **kwargs):
        """Stops the watchdog after one iteration."""
        watchdog.running = False

    mock_sleep.side_effect = stop_after_one_iteration

    watchdog.check_server()
    mock_alarm.on.assert_called_once()

@mock.patch('src.watchdog.socket.create_connection')
@mock.patch('src.watchdog.time.sleep', return_value=None)
def test_correct_server_response(mock_sleep, mock_create_connection, watchdog, mock_alarm):
    """
    Simulates a correct server response and verifies that the alarm is not activated.
    """
    mock_socket = mock.Mock()
    mock_socket.recv.return_value = b'PONG'
    mock_create_connection.return_value.__enter__.return_value = mock_socket

    def stop_after_one_iteration(*args, **kwargs):
        """Stops the watchdog after one iteration."""
        watchdog.running = False

    mock_sleep.side_effect = stop_after_one_iteration

    watchdog.check_server()
    mock_alarm.on.assert_not_called()
