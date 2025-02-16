import socket
import threading
import logging
from src.alarm import Alarm
from config import settings

logger = logging.getLogger(__name__)

class TCPServer:
    """
    A TCP server that listens for client connections to control an alarm system.
    Clients must authenticate using a predefined token and can send commands
    to activate or deactivate the alarm.
    """

    def __init__(self, alarm: Alarm) -> None:
        """
        Initializes the TCPServer with the specified alarm instance.
        Sets up the server socket and binds it to the configured host and port.

        Args:
            alarm (Alarm): An instance of the Alarm class to control.
        """
        self.host: str = settings.TCP_HOST
        self.port: int = settings.TCP_PORT
        self.auth_token: str = settings.AUTH_TOKEN
        self.alarm: Alarm = alarm
        self.server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running: bool = False

    def start(self) -> None:
        """
        Starts the TCP server to accept client connections.
        For each client connection, a new thread is spawned to handle communication.
        """
        self.is_running = True
        logger.info(f"TCP server listening on {self.host}:{self.port}")
        try:
            while self.is_running:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"Connection from {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except Exception as e:
            logger.error(f"TCP server error: {e}")
        finally:
            self.server_socket.close()

    def stop(self) -> None:
        """
        Stops the TCP server by setting the running flag to False and closing the server socket.
        """
        self.is_running = False
        self.server_socket.close()

    def handle_client(self, client_socket: socket.socket, client_address: tuple) -> None:
        """
        Handles communication with a connected client.
        Authenticates the client using a predefined token and processes commands
        to activate or deactivate the alarm.

        Args:
            client_socket (socket.socket): The socket object representing the client connection.
            client_address (tuple): The address of the connected client.
        """
        try:
            auth_data = client_socket.recv(1024).decode().strip()
            if auth_data == self.auth_token:
                client_socket.send(b"AUTH_SUCCESS\n")
                logger.info(f"Client {client_address} authenticated successfully.")
            else:
                client_socket.send(b"AUTH_FAILURE\n")
                logger.warning(f"Client {client_address} failed authentication.")
                return

            while True:
                command_data = client_socket.recv(1024).decode().strip()
                if not command_data:
                    break
                command = command_data.upper()
                if command == 'ACTIVATE':
                    self.alarm.on()
                    client_socket.send(b"Alarm activated\n")
                    logger.info(f"Client {client_address} sent 'ACTIVATE' command.")
                elif command == 'DEACTIVATE':
                    self.alarm.off()
                    client_socket.send(b"Alarm deactivated\n")
                    logger.info(f"Client {client_address} sent 'DEACTIVATE' command.")
                else:
                    client_socket.send(b"Unknown command\n")
                    logger.warning(f"Client {client_address} sent unknown command: {command}")
        except Exception as e:
            logger.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connection with {client_address} closed.")

