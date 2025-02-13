import logging
import time
from config import settings

logger = logging.getLogger(__name__)

try:
    import network
except ImportError:
    logger.warning("El módulo 'network' no está disponible. Usando un mock para pruebas.")
    from unittest import mock
    network = mock.Mock()

class NetworkManager:
    def __init__(self) -> None:
        self.ssid: str = settings.WIFI_SSID
        self.password: str = settings.WIFI_PASSWORD
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self) -> None:
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        logger.info(f'Conectando a Wi-Fi SSID: {self.ssid}')
        attempt: int = 0
        while not self.wlan.isconnected():
            attempt += 1
            logger.debug(f'Intento {attempt}: Conexión en progreso...')
            time.sleep(1)
            if attempt >= 10:
                logger.error('No se pudo conectar a Wi-Fi después de múltiples intentos.')
                raise ConnectionError('No se pudo conectar a Wi-Fi.')
        logger.info(f'Conectado a Wi-Fi: {self.wlan.ifconfig()}')


    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
            self.wlan.active(False)
            logger.info(f'Wi-Fi Desconectado')
