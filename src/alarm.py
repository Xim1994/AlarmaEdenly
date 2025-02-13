import logging

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warning("RPi.GPIO no está disponible. Usando un mock para pruebas.")
    from unittest import mock
    GPIO = mock.Mock()

class Alarm:
    def __init__(self, pin: int) -> None:
        self.pin: int = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        logger.info(f'Alarma inicializada en el pin {self.pin}')

    def on(self) -> None:
        GPIO.output(self.pin, GPIO.HIGH)
        logger.info('Alarma activada')

    def off(self) -> None:
        GPIO.output(self.pin, GPIO.LOW)
        logger.info('Alarma desactivada')

    def cleanup(self) -> None:
        GPIO.cleanup(self.pin)
        logger.info(f'GPIO limpiado para el pin {self.pin}')
