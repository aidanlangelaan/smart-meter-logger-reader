# P1 cable

I bought the P1 cable from [SOS Solutions](https://www.sossolutions.nl/slimme-meter-kabel) (I believe [ROBBshop](https://www.robbshop.nl/slimme-meter-kabel) also sells it). I know a lot of people try creating the cable themselves or buy it from e-bay/marktplaats or various China stores but this has both advantages and disadvantages.

## Self made

The issue with self made cabels is that you need the required knowledge of the schemas to properly route the wires inside the cable to the RJ12 connector. Also you will probably need to add extra resistors depending on the smart meter you want to read from (DSMR 4.2 or ESMR 5.0). Various websites contain the correct schema's to help you such as this [Tweakers forum](https://gathering.tweakers.net/forum/list_messages/1578510). This is quite error prone to be honest and as I don't have the required tools or exact knowledge this wasn't an option for me.

## China stores

Buying from China (or drop-ship) stores may be cheaper, but while doing my research into the right cable I read plenty of stories of people recieving cables that didn't work. Therefore this option is a risk as you don't know whether you will recieve a good cable or a useless bit of wire.

## Ready to use from previously mentioned webshops

Using the cable from SOS Solutions doesn't require any hardware changes as the cable contains a PCB with all the required resistors for reading DSMR 4.2 and ESMR 5.0 meters. I just plugged in the cable to both the Raspberry Pi and the smart meter and was ready to go!
