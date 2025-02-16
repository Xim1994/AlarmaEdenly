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
  SERVER_IP: Final[str] = '192.168.1.100'  # Replace with your server's IP
  SERVER_PORT: Final[int] = 8080           # Replace with your server's port

  # Alarm
  ALARM_PIN: Final[int] = 15
  ALARM_IP: Final[str] = '192.168.1.101'   # Replace with your alarm's IP

  # TCP Server
  TCP_HOST: Final[str] = '0.0.0.0'
  TCP_PORT: Final[int] = 12345
  AUTH_TOKEN: Final[str] = 'your_secure_token'  # Token for authentication

  # Logging
  LOG_FILE: Final[str] = '../logs/app.log'
  LOG_LEVEL: Final[str] = 'INFO'

  # Watchdog
  WATCHDOG_INTERVAL: Final[int] = 10  # Interval in seconds
  ```

- **Logging Configuration**: Ensure that the logging configuration points to a valid directory on your system. Modify the `LOG_FILE` path in `settings.py` if necessary.

- **Create Logs Directory**: Ensure a `logs` directory exists in the project's root directory to store log files.

  ```bash
  mkdir logs
  ```

## Usage

To start the server and client components:

1. **Start the Server**:

   ```bash
   python host.py
   ```

   This will initiate the server, which listens for incoming connections on the specified port.

2. **Run the Watchdog Client & the TCP Server**:

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

## Over-The-Air (OTA) Updates

Automate the deployment of updates using GitHub Actions:

1. **GitHub Actions Workflow**: A `deploy.yml` file is included in the `.github/workflows/` directory. This workflow automates the deployment process whenever changes are pushed to the repository.

2. **Self-Hosted Runner**: Set up a self-hosted GitHub Actions runner on your Raspberry Pi to execute the deployment workflow. This allows the Raspberry Pi to pull updates directly from the repository.

   - **Setup Instructions**: Follow GitHub's official documentation to configure a self-hosted runner on your Raspberry Pi.

3. **Automated Deployment**: Upon pushing changes to the repository, the GitHub Actions workflow will trigger, and the self-hosted runner on the Raspberry Pi will execute the deployment steps, updating the application automatically.

## Testing

To test the functionality:

1. **Unit Tests**: The project includes unit tests to verify the core functionalities. Run the tests using:

   ```bash
   pytest
   ```

2. **Integration Tests**: Simulate server unavailability by stopping the server process and observing the watchdog's behavior. The alarm should activate upon detecting a loss of connection.

## Power Consumption Optimization

To achieve a minimum battery life of one month between charges, consider the following optimizations:

- **Disable Unnecessary Components**: Turn off HDMI, onboard LEDs, and unused USB peripherals to reduce power consumption.

- **CPU Core Management**: Limit the number of active CPU cores if full processing power is not required. This can significantly reduce energy usage.

- **Sleep Modes**: Implement sleep modes during periods of inactivity to conserve battery life.

For detailed guidance on power optimization techniques, refer to [Optimizing Raspberry Pi Power Consumption](https://blues.com/blog/tips-tricks-optimizing-raspberry-pi-power/).

## Deployment

The project includes a `deploy.yml` 