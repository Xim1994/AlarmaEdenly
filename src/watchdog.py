import socket
import time
import logging
from alarm import Alarm
from config_logging import settings

logger = logging.getLogger(__name__)

class Watchdog:
    """
    Monitors the connection to the central server by sending periodic 'PING' messages.
    If an incorrect response is received or a connection error occurs, the associated
    alarm is activated.
    """

    def __init__(self, alarm: Alarm) -> None:
        """
        Initializes the Watchdog with server details and an alarm instance.

        Args:
            alarm (Alarm): An instance of the Alarm class to be triggered on connection failure.
        """
        self.server_ip: str = settings.SERVER_IP
        self.server_port: int = settings.SERVER_PORT
        self.alarm: Alarm = alarm
        self.running = True

    def check_server(self) -> None:
        """
        Continuously checks the connection to the central server every 10 seconds.
        Sends a 'PING' message and expects a 'PONG' response. If the response is incorrect
        or a connection error occurs, the alarm is activated.
        """
        while self.running:
            try:
                logger.info(f'Checking connection to {self.server_ip}:{self.server_port}')
                with socket.create_connection((self.server_ip, self.server_port), timeout=15) as sock:
                    sock.sendall(b'PING')
                    response: bytes = sock.recv(1024)
                    if response != b'PONG':
                        raise ConnectionError('Incorrect response from the server.')
                    logger.info('Connection with the central server verified.')
            except (socket.timeout, ConnectionError, OSError) as e:
                logger.error(f'Error communicating with the central server: {e}')
                self.alarm.on()
            time.sleep(settings.WATCHDOG_INTERVAL)
