# Alarm Control System

The Alarm Control System is a network-based solution designed to remotely manage an alarm system using a Raspberry Pi Zero 2 W. This system offers remote activation and deactivation of the alarm, continuous monitoring of connectivity, and automated updates to ensure optimal performance.


## Features

- **Remote Alarm Activation/Deactivation**: Control the alarm system over a TCP/IP network using predefined commands.
- **Authentication Mechanism**: Ensures that only authorized clients can send commands to the server.
- **Watchdog Functionality**: Monitors connectivity with a central server; the alarm activates if the connection is lost.
- **Over-The-Air (OTA) Updates**: Automates deployment of updates using GitHub Actions.
- **Logging**: Records all activities, including connections, commands received, and alarm status changes, in a dedicated logs directory.

## Prerequisites

Ensure the following components are available before setting up the project:

- **Hardware**:
  - Raspberry Pi Zero 2 W
  - Rechargeable battery pack with USB-C charging
  - External alarm module capable of producing >100 dB at one meter
  - Protective enclosure suitable for outdoor use, shielding from direct rain
  - Button or switch for manual shutdown

- **Software**:
  - Python 3.12: [Download and install Python](https://www.python.org/downloads/)
  - `pip`: Python package installer (usually included with Python)
  - GitHub account for repository management and Actions


## Assembly Guidelines
Mount the Raspberry Pi Zero 2 W inside the IP67 enclosure.
Connect the alarm module to the GPIO pin defined in settings.py.
Connect the power source via USB-C (ensure at least 2A supply).
Add an optional switch or button to GPIO or inline on power.
Drill custom holes if needed to expose ports or access diagnostics LEDs.


## Installation

Follow these steps to set up the project on your Raspberry Pi Zero 2 W:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/alarm-control-system.git
   cd alarm-control-system
   ```

2. **Create a Virtual Environment (optional but recommended)**:

   ```bash
   python -m venv venv
   # On Unix or MacOS
   source venv/bin/activate
   # On Windows
   venv\Scripts\activate
   ```

3. **Install Required Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   *Note*: If you encounter a `ModuleNotFoundError` for `typing_extensions`, install it separately:

   ```bash
   pip install typing_extensions
   ```


## Configuration

Configure the project settings as needed:

- **Network Settings**: Update the `settings.py` file with your network credentials and server details.

  ```python
  from typing import Final

  # Wi-Fi
  WIFI_SSID: Final[str] = 'Your_SSID'
  WIFI_PASSWORD: Final[str] = 'Your_Password'

  # Central Server
  SERVER_IP: Final[str] = '192.168.1.100'  # Replace with your alarm's IP
  SERVER_PORT: Final[int] = 8080           # Replace with your alarm's port

  # Alarm
  ALARM_PIN: Final[int] = 15
  ALARM_IP: Final[str] = '192.168.1.101'   # Replace with your alarm's IP

  # TCP Server
  TCP_HOST: Final[str] = '0.0.0.0'         # Replace with your host IP
  TCP_PORT: Final[int] = 12345             # Replace with your host port
  AUTH_TOKEN: Final[str] = 'your_secure_token'  # Token for authentication

  # Logging
  LOG_FILE: Final[str] = '../logs/app.log'
  LOG_LEVEL: Final[str] = 'INFO'

  # Watchdog
  WATCHDOG_INTERVAL: Final[int] = 10  # Interval in seconds

  # Alarm functionality
  ALARM_ACTIVATED: Final[bool] = True  # If the alarm functionality should be activated (set to False for testing)
  ```

- **Logging Configuration**: Ensure that the logging configuration points to a valid directory on your system. Modify the `LOG_FILE` path in `settings.py` if necessary.

- **Create Logs Directory**: Ensure a `logs` directory exists in the project's root directory to store log files.

  ```bash
  mkdir logs
  ```


## Usage

To start the server and client components:

1. **From your Server Machine, start the Server**:

   ```bash
   python host.py
   ```

   This will initiate the server, which listens for incoming connections on the specified port.

2. **From your alarm device, run the Watchdog Client & the TCP Server**:

   ```bash
   python main.py
   ```

   The watchdog will attempt to connect to the central server at regular intervals to verify connectivity.

3. **Sending Commands to the Raspberry Pi**:

   Use the `alarm_send_command.py` script to send commands to the Raspberry Pi. This script requires the Raspberry Pi IP address, port, authentication token, and the command (`ACTIVATE` or `DEACTIVATE`).

   ```bash
   python alarm_send_command.py
   ```

   Use your server's IP address, the server's port, and the authentication token defined in your `settings.py`.


## Watchdog Functionality

The watchdog monitors the connection to the central server by sending periodic `PING` messages. If a `PONG` response is not received within the specified interval, the alarm is activated. This ensures that any loss of connectivity triggers the alarm, providing a fail-safe mechanism.


## Testing

To test the functionality:

1. **Unit Tests**: The project includes unit tests to verify the core functionalities. Run the tests using:

   ```bash
   pytest tests
   ```

2. **Integration Tests**: Simulate server unavailability by stopping the server process and observing the watchdog's behavior. The alarm should activate upon detecting a loss of connection.

## Power Consumption Optimization

To achieve a minimum battery life of one month between charges, we have implemented a script power_optimization.sh to optimize power consumption:

- **Disable Unnecessary Components**: Turns off HDMI, Bluetooth, onboard LEDs, and unused USB peripherals to reduce power consumption.

- **CPU Core Management**: Limit the number of active CPU cores to one if full processing power is not required. This can significantly reduce energy usage. Also, reducing the CPU's clock speed decreases power usage, which is beneficial for applications that don't require maximum processing power.

- **Sleep Modes**: Introducing sleep modes in the python code during periods of inactivity to substantially lower energy consumption.

For detailed guidance on power optimization techniques, refer to [Optimizing Raspberry Pi Power Consumption](https://blues.com/blog/tips-tricks-optimizing-raspberry-pi-power/).

- **Power Optimization Script**: You can run the power_optimization.sh script to lower the power consumption of the device, it includes the following actions:

Bluetooth Disabled: Prevents the Pi from powering and initializing Bluetooth hardware.
HDMI Disabled: If no screen is needed, the HDMI output is turned off completely.
LEDs Disabled: Turns off the onboard status LEDs to prevent constant current draw.
USB Unbound: Disconnects USB hubs not in use (especially useful when running headless).
CPU Throttled: Reduces maximum clock speed and disables additional CPU cores for energy efficiency.

Note: After running this script, a reboot is required to apply all changes.

- **Lightweight Operating System**: Raspbian Lite OS (32-bit) is the minimal version of the official Raspberry Pi OS, designed without a graphical desktop environment. It provides a command-line interface, making it lightweight and efficient, suitable for headless operations and systems where resources are limited. 


## Running the Alarm Control System as a Service

To ensure the Alarm Control System starts automatically upon boot, a `systemd` service file named `alarm.service` is included in this repository. This service file allows the `main.py` script to run as a background service on your Raspberry Pi.

**Setting Up the `alarm.service`**: Here you can find the instructions on how to set up a script to run when the raspberry pi starts https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all



