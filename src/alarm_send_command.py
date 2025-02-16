import socket
import logging
from config_logging import setup_logging
from config import settings

setup_logging()
logger = logging.getLogger(__name__)

server_ip = settings.ALARM_IP
server_port = settings.ALARM_PORT
auth_token = settings.AUTH_TOKEN

def send_command(command: str) -> None:
    """
    Connects to the server, sends the authentication token and command,
    and logger.infos the server's response.

    Args:
        command (str): The command to send to the server ('ACTIVATE' or 'DEACTIVATE').
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, server_port))
            logger.info(f"Connected to {server_ip}:{server_port}")

            sock.sendall(auth_token.encode() + b'\n')
            auth_response = sock.recv(1024).decode().strip()
            if auth_response == 'AUTH_SUCCESS':
                logger.info("Authentication successful.")

                sock.sendall(command.encode() + b'\n')
                command_response = sock.recv(1024).decode().strip()
                logger.info(f"Server response: {command_response}")
            else:
                logger.warning("Authentication failed.")
            logger.info(f"Connection with {server_ip} closed.")
    except ConnectionRefusedError:
        logger.error("Connection failed. Is the server running?")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    send_command('ACTIVATE')
    send_command('DEACTIVATE')
