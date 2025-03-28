import logging
from alarm_config import settings

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warning("RPi.GPIO is not available. Using a mock for testing purposes.")
    from unittest import mock
    GPIO = mock.Mock()

class Alarm:
    def __init__(self, pin: int) -> None:
        self.pin: int = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        logger.info(f'Alarm initialized on pin {self.pin}')

    def on(self) -> None:
        if settings.ALARM_ACTIVATED:
            GPIO.output(self.pin, GPIO.HIGH)
        logger.info('Alarm activated')

    def off(self) -> None:
        GPIO.output(self.pin, GPIO.LOW)
        logger.info('Alarm deactivated')

    def cleanup(self) -> None:
        GPIO.cleanup(self.pin)
        logger.info(f'GPIO cleaned up for pin {self.pin}')
