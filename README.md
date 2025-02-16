# Alarm Control System

The Alarm Control System is a network-based solution designed to remotely manage an alarm system over a TCP/IP network. It features a server-client architecture where the server listens for incoming connections and processes commands to activate or deactivate the alarm, while the client connects to the server to send these commands.

## Features

- **Remote Alarm Activation/Deactivation**: Control the alarm system from a remote client over the network.
- **Authentication Mechanism**: Ensures that only authorized clients can send commands to the server.
- **Logging**: Records all activities, including connections, commands received, and alarm status changes.

## Prerequisites

Before setting up the project, ensure that the following software and tools are installed on your system:

- **Python 3.12**: [Download and install Python](https://www.python.org/downloads/).
- **pip**: Python package installer (usually included with Python).

## Installation

Follow these steps to set up the project on your local machine:

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

- **Logging Configuration**: Ensure that the logging configuration points to a valid directory on your system. Modify the `LOG_FILE` path in `config_logging.py` if necessary.

- **Server Details**: Update `settings.SERVER_IP` and `settings.SERVER_PORT` in your configuration files to match your server's IP address and port.

## Usage

To start the server and client components:

1. **Start the Server**:

   ```bash
   python server.py
   ```

   This will initiate the server, which listens for incoming connections on the specified port.

2. **Run the Client (Watchdog)**:

   ```bash
   python watchdog.py
   ```

   The watchdog will attempt to connect to the server at regular intervals to verify connectivity.

## Testing

To test the functionality:

1. **Simulate Server Unavailability**: Stop the server process to mimic a server outage.

2. **Observe Client Behavior**: The watchdog should log an error and trigger the alarm mechanism upon failing to connect to the server.

3. **Restore Server Functionality**: Restart the server and observe that the watchdog successfully re-establishes the connection.

## Troubleshooting

- **Permission Issues on Port 80**: Binding to port 80 may require administrative privileges. Consider using a higher-numbered port (e.g., 8080) during development and update your configuration accordingly.

- **Firewall Settings**: Ensure that your firewall allows traffic on the chosen port to facilitate communication between the client and server.

- **SSH Connectivity**: If you're developing on a Windows machine and deploying to a Raspberry Pi (RPI), ensure that SSH is enabled on the RPI. Use an SSH client like PuTTY or configure Visual Studio Code with the Remote - SSH extension for seamless development.

## Contributing

We welcome contributions from the community. To contribute:

1. **Fork the Repository**: Click on the 'Fork' button at the top right of the repository page.

2. **Create a New Branch**: Use a descriptive name for your branch.

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**: Implement your feature or fix.

4. **Commit and Push**:

   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**: Navigate to the original repository and click on 'New Pull Request'.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Credit to all contributors and inspirations that have made this project possible. 