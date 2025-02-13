import socket
import threading
import logging
from src.alarm import Alarm
from config import settings

logger = logging.getLogger(__name__)

class TCPServer:
    def __init__(self, alarm: Alarm) -> None:
        self.host: str = settings.TCP_HOST
        self.port: int = settings.TCP_PORT
        self.auth_token: str = settings.AUTH_TOKENdo
        self.alarm: Alarm = alarm
        self.server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running: bool = False

    def start(self) -> None:
        self.is_running = True
        logger.info(f"Servidor TCP escuchando en {self.host}:{self.port}")
        try:
            while self.is_running:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"Conexión desde {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            logger.error(f"Error en el servidor TCP: {e}")
        finally:
            self.server_socket.close()

    def stop(self) -> None:
        self.is_running = False
        self.server_socket.close()

    def handle_client(self, client_socket: socket.socket) -> None:
        try:
            data: str = client_socket.recv(1024).decode().strip()
            if data == self.auth_token:
                client_socket.send(b"AUTH_SUCCESS\n")
                command: str = client_socket.recv(1024).decode().strip().upper()
                if command == 'ACTIVATE':
                    self.alarm.on()
                    client_socket.send(b"Alarma activada\n")
                    logger.info("Comando 'ACTIVATE' recibido: Alarma activada")
                elif command == 'DEACTIVATE':
                    self.alarm.off()
                    client_socket.send(b"Alarma desactivada\n")
                    logger.info("Comando 'DEACTIVATE' recibido: Alarma desactivada")
                else:
                    client_socket.send(b"Comando desconocido\n")
                    logger.warning(f"Comando desconocido recibido: {command}")
            else:
                client_socket.send(b"AUTH_FAILURE\n")
                logger.warning("Intento de autenticación fallido")
        except Exception as e:
            logger.error(f"Error al manejar la conexión del cliente: {e}")
        finally:
            client_socket.close()
