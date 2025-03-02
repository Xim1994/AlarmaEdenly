#!/bin/bash

# Disable Bluetooth
sudo sed -i '$ a dtoverlay=disable-bt' /boot/config.txt

# Disable HDMI output
sudo /opt/vc/bin/tvservice -o

# Turn off the power (PWR) LED
sudo sed -i '$ a dtparam=pwr_led_trigger=none' /boot/config.txt
sudo sed -i '$ a dtparam=pwr_led_activelow=off' /boot/config.txt

# Turn off the activity (ACT) LED
sudo sed -i '$ a dtparam=act_led_trigger=none' /boot/config.txt
sudo sed -i '$ a dtparam=act_led_activelow=off' /boot/config.txt

# Disable USB and Ethernet (if not in use)
echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind

# Limit CPU frequency to reduce power consumption
sudo sed -i '$ a arm_freq=600' /boot/config.txt

# Disable specific CPU cores (retain core 0)
sudo sed -i '$ a maxcpus=1' /boot/cmdline.txt

echo "Power optimization completed. Please reboot the system to apply changes."
