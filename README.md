# rpi-smartmeter-logger

This repo contains a python script for connecting to and reading telegrams from the ISKRA AM550 smart meter. For this purpose I have setup a Raspberry Pi 4 which is connected to the smart meter by a P1 cable.

This script may also work for other smart meters but I have not yet been able to test this. In the future I will try and wright up the issues I ran into.

- Setting up Raspberry Pi
- Connecting to smart meter (serial console)
- Connecting to my api (traffic)

## P1 cable

As for the P1 cable, I bought this from [SOS Solutions](https://www.sossolutions.nl/slimme-meter-kabel) (I believe [ROBBshop](https://www.robbshop.nl/slimme-meter-kabel) also sells it). I know a lot of people try creating the cable themselves or buy it from e-bay/marktplaats or various China stores but this has both advantages and disadvantages.

### Self made

The issue with self made cabels is that you need the required knowledge of the schema's to properly route the wires inside the cable to the RJ12 connector. Also you will probably need to add extra resistors depending on the smart meter you want to read from (DSMR 4 or 5). Various websites contain the correct schema's to help you such as this [Tweakers forum](https://gathering.tweakers.net/forum/list_messages/1578510). This is quite error prone to be honest and as I don't have the required tools or exact knowledge, this wasn't an option for me.

### China stores

Buying from China stores may be cheaper, but while doing my research into the right cable I read plenty of stories of people recieving cables that didn't work. Therefore this option is a risk as you don't know wether you will recieve a good cable or a useless bit of wire.

### Ready to use from previously mentioned stores

Using the cable from SOS Solutions doesn't require any hardware changes as the cable contains a PCB with all the required resistors for reading DSMR 4 and 5 meters. I just plugged in the cable to both the Raspberry Pi and the smart meter and was ready to go!

## Sources

For making the script I made use of the various sources listed bellow.

- [Tweakers.net - Slimme meter uitlezen via P1-poort](https://gathering.tweakers.net/forum/list_messages/1578510)
- [Ge Janssen - Slimme meter uitlezen met Raspberry Pi](http://gejanssen.com/howto/Slimme-meter-uitlezen/)
- [www.kapper.com - P1 energy meter reader using python in Docker](https://www.kaper.com/software/p1-energy-meter-reader-using-python-in-docker/)

# Setting up the Raspberry Pi

I had an initial setup (without POST to the backend) running on my RPi. However, the project lay dormant for a year and when I came back to it my internet network has changed significantly. Using various methodes I was not able to connect into the RPi. Therefore I decided to backup the existing image and startout anew. This also allowed me to document any issues I ran into while doing so.

## Step 1: Install the OS (using Windows)

For this I used the default software provided by Raspberry Pi themselves, Raspberry Pi Imager (v1.7.5). With this application I first formatted the SD-card. As I couldn't see if I was required to do so first or that the application would do that automatically, I decided to implicitly format the SD-card first. When selecting the Operation System you can select an option to format the SD-card to FAT32. 

After formatting I altered the advanced options and set the following:

- hostname (defaults to raspberrypi.local)
- Enable SSH with either password or key authentication (as I will be running it headless)
- Set a username and password
- Configured wireless LAN (yes wired would be better but where the RPi will be setup I don't currently have any cables running)
- Set locale settings to my timezone (EU/Amsterdam)

I then selected de recommended Raspberry Pi OS (32-bit) and the SD-card. The last time I set this up I went for an OS without desktop as the plan was to run headless. However this time I on perposely chose the OS including the desktop, so that if I run into the same network issues in the future I can simply connect the RPi to a screen and fix the issue without having to do another setup.

After selecting the SD-card I started writing the OS by clicking WRITE.

## Step 2: Connecting for the first time

After the software completed writing the OS to the SD-card, I took it out of my laptop, put it into the RPi and plugged in the power suply. After this I waited at least 15 minutes so that the RPi could do its thing and would have completed any setup before attempting to connect. 

While waiting, I used Advanced IP Scanner to check if I could already see it show up in my network. Here I ran into my first issue: no apparent network connection. Even though I did set it up correctly before writing the OS to the SD-card, the RPi wasn't showing up in my network. So after 30 minutes I connected it directly to my network by cable, after which I could connect over SSH. All other settings had been correctly configured so I'm not sure what went wrong.

## Step 3: Updating and preparing the OS

After I was able to connect, I first ran the following commands to make sure the OS was up-to-date:

```
sudo apt update
sudo apt upgrade
```

To make sure network-manager was already installed i ran:

`sudo apt install network-manager`

Then I ran `sudo raspi-config` to enter the RPi configuration. Here I changed the following settings:

```
# To update the config tool
8 Update      

# To allow network configuration using the newer NetworkManager instead of the old dhcpcd
6 Advanced Options -> AA Network Config -> 2 NetworkManager     

# To make full use of all available room on the SD-card
6 Advanced Options -> A1 Expand Filesystem
```

I then selected finish and rebooted the RPi.

## Step 4: Static IP address

I wanted the raspberry pi to be accessible using a static IP address, when connected through Wi-Fi. Partially due to not having a network cable available in the meter cupboard, but also so that I can connect the RPi by wire should I have any issues with the Wi-Fi connection. Because we selected to use the NetworkManager in the privious step and I'm settng the RPi up over SSH, I have to use the NetworkManager command line (mncli) to configure the network.

First I needed the name of the current Wi-Fi connection:
`nmcli dev status`

This shows me all network devices, the type, state and connection. As I'm altering the Wi-Fi connection I took note of the value in the CONNECTION column. I then checked my network to confirm what IP I could use and then used the following commands to set it up (yes you can also use a 1-liner but doing it this way makes sure I don't easily make a typo:

```
sudo nmcli con edit {CONNECTION_VALUE}
set ipv4.method manual
set ipv4.address 192.168.1.3/24
set ipv4.gateway 192.168.1.1
save
quit
```

To complete and activate the connection run:
`sudo nmcli con edit {CONNECTION_VALUE}`

At the same time I configured my router reserve the selected IP for the MAC-address of the RPi. To finish of and test if the connection was working, I ran the following command to restart the RPi and quikly disconnected the network cable:
`sudo shutdown -r now`

Within a minute the RPi showed back online over Wi-Fi, with the supplied static IP!

## Step 5: Enable Serial Port interface

You can't out-of-the-box read from the usb port, first you need to enable the serialisation interface using the following steps:. 

```
# Start by opening the Raspberry Pi configuration tool
sudo raspi-config

# Navigate to the serial port config
3 Interface Options -> I6 Serial Port

# Enable the options
Yes -> OK
```

The serial port is now enabled.

## Step 6: Validate setup

At this point I moved the RPi to het meter closet, reconnected the power and plugged in the USB cable that's connected to the smartmeter. All starts up without issues and is accesable through SSH. Now it's time to validate if the configuration so far has worked. 

First install cu to read the telegrams from the USB port: `sudo apt-get install cu`. Now we need to check if the RPi can see the connected USB. By running `ls -l /dev/ttyU*` you should see at least 1 row that results in the path of the connected port. If you get an error simular to `No such file or directory` it means the RPi hasn't properly detected the connected USB. Make sure the USB is plugged in securely and that you have followed step 5 to enable the Serial Port interface.

Depending on the E/D-SMR version you need different settings to read from the smart meter:

| Parameter | [DSMR 4.2](https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_7b581ff014.pdf) | [ESMR 5.0](https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf) |
|-----------|----------|----------|
| Baud rate | 115200   | 115200   |
| Data bits | 7        | 8        |
| Parity    | Even     | None     |
| Stop bits | 1        | 1        |

Check your smart meter to make sure you are using the right settings. If you can't find it on the smart meter itself, you will probably find what version it is by looking it up in Google.

In my case I have a ESMR 5.0 meter so will use the following command:

`cu -l /dev/ttyUSB0 -s 115200 --parity=none -E q`

You should now get a stream of telegrams from your smart meter. I believe most meters will return a telegram every 1 to 10 seconds. To exit the serial output hit `q`.
