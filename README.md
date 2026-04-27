Python3 Clock
==============

## Use Raspberry Pi Imager to install Raspian.
Raspberry Pi OS (other) > Raspberry Pi OS Lite 64-bit
Attach a keyboard before first boot, select “Other” when presented with the keyboard configuration and choose the US layout. Enter user and password (User admin is suggested, if you want to use something else you will have to edit RPiAClock.service and RPiAClock.ini to get the path and user set correctly).

## Upgrade to latest OS
    sudo apt-get update
    sudo apt-get upgrade

## Enable SSH
    sudo rasp-config > 3 > I2 Enable SSH

## Set timezone
    sudo raspi-config > 5 > L2 Timezone

## Install pygame
    sudo apt-get install python3-pygame
    sudo apt-get install libegl-dev

## Install chrony
    sudo apt-get install chrony

## Configure systemd
    sudo cp /home/admin/RPiAnalogClock/RPiAClock.service /lib/systemd/system
    sudo systemctl enable RPiAClock.service
    sudo systemctl start RPiAClock.service
    
