from typing import Final

# Configuración Wi-Fi
WIFI_SSID: Final[str] = 'tu_ssid'
WIFI_PASSWORD: Final[str] = 'tu_password'

# Configuración del servidor central
SERVER_IP: Final[str] = '192.168.1.100'
SERVER_PORT: Final[int] = 80

# Configuración del servidor TCP
TCP_HOST: Final[str] = '0.0.0.0'
TCP_PORT: Final[int] = 12345
AUTH_TOKEN: Final[str] = 'tu_token_seguro'  # Token para autenticación

# URL del repositorio para actualizaciones OTA
OTA_REPO_URL: Final[str] = 'https://github.com/usuario/repositorio'

# Configuración de logging
LOG_FILE: Final[str] = 'logs/app.log'
LOG_LEVEL: Final[str] = 'INFO'