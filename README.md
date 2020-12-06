# rpi-smartmeter-logger

This repo contains a python script for connecting to and reading telegrams from the ISKRA AM550 smart meter. For this purpose I have setup a Raspberry Pi 4 which is connected to the smart meter by a P1 cable.

This script may also work for other smart meters but I have not yet been able to test this. In the future I will try and wright up the issues I ran into.

- Setting up Raspberry Pi (fixed IP / wifi)
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
