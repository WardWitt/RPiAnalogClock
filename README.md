Python3 Clock
==============

## Use Raspberry Pi Imager to install Raspian.
Raspberry Pi OS (other) > Raspberry Pi OS Lite 64-bit
Attach a keyboard before first boot, select “Other” when presented with the keyboard configuration and choose the US layout. Enter user and password (admin is suggested).

## Fixed IP address if needed
    sudo nano /etc/dhcpcd.conf
Edit and uncomment the “Example static IP configuration” to suit your environment.

## Upgrade to latest OS
    sudo apt-get update
    sudo apt-get upgrade

## Enable SSH
    sudo rasp-config > 3 > I2 Enable SSH

## Set timezone
    sudo raspi-config > 5 > L2 Timezone

## Install pygame
    sudo apt-get install python3-pygame

## Install chrony
    sudo apt-get install chrony

## Configure systemd
    sudo cp /home/admin/rpi-clock/RPiclock.service /lib/systemd/system
    sudo systemctl enable RPiclock.service
    sudo systemctl start RPiclock.service
    
