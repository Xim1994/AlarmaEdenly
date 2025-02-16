import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class NetworkManager:
    def __init__(self, ssid: str, password: str) -> None:
        self.ssid = ssid
        self.password = password

    def connect(self) -> bool:
        """
        Connect to the specified Wi-Fi network using nmcli.
        Returns True if the connection is successful, False otherwise.
        """
        try:
            current_ssid = self.get_current_ssid()
            if current_ssid == self.ssid:
                logger.info(f"Already connected to Wi-Fi SSID: {self.ssid}")
                return True

            subprocess.run(['nmcli', 'device', 'disconnect', 'wlan0'], check=True)
            logger.info("Disconnected from any existing Wi-Fi connection.")

            result = subprocess.run(
                ['nmcli', 'device', 'wifi', 'connect', self.ssid, 'password', self.password],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Connected to Wi-Fi SSID: {self.ssid}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to connect to {self.ssid}: {e.stderr.strip()}")
            return False

    def disconnect(self) -> bool:
        """
        Disconnect from the current Wi-Fi network.
        Returns True if disconnection is successful, False otherwise.
        """
        try:
            subprocess.run(['nmcli', 'device', 'disconnect', 'wlan0'], check=True)
            logger.info("Wi-Fi disconnected successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to disconnect Wi-Fi: {e.stderr.strip()}")
            return False

    def get_current_ssid(self) -> Optional[str]:
        """
        Retrieve the SSID of the currently connected Wi-Fi network.
        Returns the SSID as a string if connected, or None if not connected.
        """
        try:
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'],
                check=True,
                capture_output=True,
                text=True
            )
            for line in result.stdout.splitlines():
                active, ssid = line.split(':')
                if active == 'yes':
                    return ssid
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve current SSID: {e.stderr.strip()}")
            return None
