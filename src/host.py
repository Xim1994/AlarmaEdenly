import socket
import logging
from config_logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def start_server(host: str = '0.0.0.0', port: int = 80):
    """
    Starts a TCP server that listens on the specified host and port.
    Responds with 'PONG' to any 'PING' messages received.

    Args:
        host (str): The IP address to bind the server to. Defaults to '0.0.0.0' (all interfaces).
        port (int): The port number to bind the server to. Defaults to 80.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((host, port))
            server_socket.listen(5)
            logger.info(f"Server listening on {host}:{port}")

            while True:
                logger.info("Waiting for a connection...")
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    logger.info(f"Connection established with {client_address}")
                    data = client_socket.recv(1024).strip()
                    if data == b'PING':
                        client_socket.sendall(b'PONG')
                        logger.info("Received 'PING', sent 'PONG'")
                    else:
                        client_socket.sendall(b'Unknown command')
                        logger.warning(f"Received unrecognized message: {data}")
                    logger.info(f"Connection with {client_address} closed.")
        except PermissionError:
            logger.error(f"Permission denied: Unable to bind to port {port}. Administrative privileges may be required.")
        except OSError as e:
            logger.error(f"OS error occurred: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    start_server()
