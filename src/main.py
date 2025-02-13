import threading
import time
from src.alarm import Alarm
from src.network import NetworkManager
from src.watchdog import Watchdog
from src.ota_update import OTAUpdater
from config import settings
import logging

logger = logging.getLogger(__name__)

def main():
    alarm = Alarm(pin=15)
    network = NetworkManager()
    watchdog = Watchdog(alarm=alarm)
    ota_updater = OTAUpdater(repo_url=settings.OTA_REPO_URL)

    try:
        network.connect()
        threading.Thread(target=watchdog.check_server).start()
        # Lógica adicional para el servidor TCP y manejo de comandos
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        alarm.cleanup()

if __name__ == '__main__':
    main()
