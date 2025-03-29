from typing import Final

# Wi-Fi
WIFI_SSID: Final[str] = 'DIGIFIBRA-9fsY'
WIFI_PASSWORD: Final[str] = 'hYFUDexhFs9f'

# Central Server
SERVER_IP: Final[str] = '127.0.0.1'
SERVER_PORT: Final[int] = 80

# Alarm
ALARM_PIN: Final[int] = 15
ALARM_IP: Final[str] = '192.168.1.155'
ALARM_PORT: Final[int] = 12345

# TCP Server
AUTH_TOKEN: Final[str] = 'your_secure_token'  # Token para autenticación

# Logging
LOG_FILE: Final[str] = 'logs/app.log'
LOG_LEVEL: Final[str] = 'INFO'

# Watchdog
WATCHDOG_INTERVAL: Final[int] = 10  # Intervalo de comprobación en segundos

# Alarm functionality
ALARM_ACTIVATED: Final[bool] = True  # If the alarm functionality should be activated (set to False for testing)