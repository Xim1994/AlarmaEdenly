import socket
import time
import logging
from src.alarm import Alarm
from config import settings

logger = logging.getLogger(__name__)

class Watchdog:
    def __init__(self, alarm: Alarm) -> None:
        self.server_ip: str = settings.SERVER_IP
        self.server_port: int = settings.SERVER_PORT
        self.alarm: Alarm = alarm

    def check_server(self) -> None:
        while True:
            try:
                with socket.create_connection((self.server_ip, self.server_port), timeout=5) as sock:
                    sock.sendall(b'PING')
                    response: bytes = sock.recv(1024)
                    if response != b'PONG':
                        raise ConnectionError('Respuesta incorrecta del servidor.')
                    logger.info('Conexión con el servidor central verificada.')
            except (socket.timeout, ConnectionError, OSError) as e:
                logger.error(f'Error en la comunicación con el servidor central: {e}')
                self.alarm.on()
            time.sleep(10)  # Intervalo de comprobación
