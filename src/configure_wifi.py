import os
import logging
from pathlib import Path
from alarm_config.settings import WIFI_SSID, WIFI_PASSWORD, LOG_FILE, LOG_LEVEL

logger = logging.getLogger(__name__)

def configure_wifi(ssid: str, password: str) -> None:
    """
    Configures the Wi-Fi settings on the Raspberry Pi by updating the wpa_supplicant.conf file.

    Args:
        ssid (str): The SSID of the Wi-Fi network.
        password (str): The password for the Wi-Fi network.
    """
    try:
        # Define the wpa_supplicant configuration
        wpa_supplicant_conf = f"""
        country=US
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1

        network={{
            ssid="{ssid}"
            psk="{password}"
            key_mgmt=WPA-PSK
        }}
        """

        # Write the configuration to wpa_supplicant.conf
        wpa_supplicant_path = Path('/etc/wpa_supplicant/wpa_supplicant.conf')
        with wpa_supplicant_path.open('w') as file:
            file.write(wpa_supplicant_conf.strip())
        logger.info('Wi-Fi configuration updated successfully.')

        # Restart the dhcpcd service to apply changes
        os.system('sudo systemctl restart dhcpcd')
        logger.info('DHCPCD service restarted successfully.')

    except Exception as e:
        logger.error(f'Failed to configure Wi-Fi: {e}')

if __name__ == '__main__':
    configure_wifi(WIFI_SSID, WIFI_PASSWORD)
