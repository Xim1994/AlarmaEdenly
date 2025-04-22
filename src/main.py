import threading
import time
import logging
from alarm import Alarm
from network import NetworkManager
from watchdog import Watchdog
from server import TCPServer
from alarm_config import settings
from config_logging import setup_logging

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize components
        alarm = Alarm(pin=settings.ALARM_PIN)
        network = NetworkManager(settings.WIFI_SSID, settings.WIFI_PASSWORD)
        print("A")
        watchdog = Watchdog(alarm=alarm)
        print("B")
        tcp_server = TCPServer(alarm=alarm)
        print("F")

        # Connect to the network
        network.connect()

        # Start watchdog and TCP server in separate threads
        threading.Thread(target=watchdog.check_server, daemon=True).start()
        print("C")
        threading.Thread(target=tcp_server.start, daemon=True).start()
        print("D")

        logger.info("System initialized and running.")

        # Keep the main thread alive
        while True:
            sleep_duration = 3600
            logger.info(f"System entering sleep mode for {sleep_duration} seconds.")
            time.sleep(sleep_duration)

    except Exception as e:
        logger.error(f"An error occurred in the main application: {e}")
    finally:
        # Clean up resources
        alarm.cleanup()
        tcp_server.stop()
        logger.info("System shutdown complete.")

if __name__ == '__main__':
    main()
