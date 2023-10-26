# smart-meter-logger-reader

This repo contains a python script for connecting to and reading telegrams from the ISKRA AM550 smart meter (ESMR 5.0). For this purpose I have setup a Raspberry Pi 4B which is connected to the smart meter by a P1 cable.

This script may also work for other smart meters but I have not yet been able to test this. I have tried to document the steps I took to setup the whole system, both for myself (for when I mess up my current setup) and for others trying to do the same thing.

The purpose of this project is to read all telegrams from the smart meter and to send this to a backend service. This will then be saved to a database after which I can create reports to track my energy usage. Please see [smart-meter-logger-backend](https://github.com/aidanlangelaan/smart-meter-logger-backend) for the backend part of the project.

Feel free to use my code (a mention or star is appreciated) as it's based on other examples found online and you may want to tweak it for your own use.

## Documentation

[P1 cable](./documentation/p1-cable.md)

[1. Setting up the Raspberry Pi](./documentation/raspberry-pi-setup.md)

[2. Get the logger script running](./documentation/application-setup.md)

## Sources

For making the script I made use of the various sources listed bellow.

- [Tweakers.net - Slimme meter uitlezen via P1-poort](https://gathering.tweakers.net/forum/list_messages/1578510)
- [Ge Janssen - Slimme meter uitlezen met Raspberry Pi](http://gejanssen.com/howto/Slimme-meter-uitlezen/)
- [www.kapper.com - P1 energy meter reader using python in Docker](https://www.kaper.com/software/p1-energy-meter-reader-using-python-in-docker/)
- [domoticx.com - P1 poort slimme meter (hardware)](https://domoticx.com/p1-poort-slimme-meter-hardware/)
- [www.fluvius.be - Digitale Meters in
  Vlaanderen](https://www.fluvius.be/sites/fluvius/files/2020-01/dmk-demo-v2.1-rtc.pdf)
- [Vives Connected Digital Energy Meter - Communication protocol](https://www.cdem.be/13_technical/#communication-protocol)
