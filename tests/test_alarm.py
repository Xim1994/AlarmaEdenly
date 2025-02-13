import unittest
from unittest.mock import patch
from src.alarm import Alarm

class TestAlarm(unittest.TestCase):
    @patch('src.alarm.GPIO')
    def test_alarm_on(self, mock_gpio):
        alarm = Alarm(pin=15)
        alarm.on()
        mock_gpio.output.assert_called_with(15, mock_gpio.HIGH)

    @patch('src.alarm.GPIO')
    def test_alarm_off(self, mock_gpio):
        alarm = Alarm(pin=15)
        alarm.off()
        mock_gpio.output.assert_called_with(15, mock_gpio.LOW)

    @patch('src.alarm.GPIO')
    def test_alarm_cleanup(self, mock_gpio):
        alarm = Alarm(pin=15)
        alarm.cleanup()
        mock_gpio.cleanup.assert_called_with(15)

if __name__ == '__main__':
    unittest.main()
