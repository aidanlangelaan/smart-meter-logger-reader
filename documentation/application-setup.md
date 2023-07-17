# Setting up the smart meter logger

Now we have the RPi setup we want to get the logger application to work. This application will read the telegrams from the smart meter and send them to the backend to be processed.

The script itself is purely for reading the raw telegram and parsing it to JSON, ready to be posted.

## Step 1: Get the code

I'm hosting this code (where you're probably reading this) in Github, but you can use any type of hosting that you want.

Again, out-of-the-box the Raspberry Pi OS is shipped with Git installed. If not, install using `sudo apt-get install git`. We now can directly download the application to the RPi:

```
cd /bin
sudo mkdir rpi-smartmeter-logger
cd rpi-smartmeter-logger
sudo git clone https://github.com/aidanlangelaan/rpi-smartmeter-logger.git .
```

## Step 2: Install the required packages

The script uses 2 packages to run. To install these run the following command:

`pip install -r requirements.txt`

## Step 3: Run the application

We must first decide on how to run the application, this can be done in 2 different ways:

1. Continuous loop

   Depending on the sleep and telegram-count parameters, the script will retrieve x telegrams to post, after which it will sleep for x seconds. It will continue this loop endlessly untill it is manually stopped or killed by the RPi being turned off. After restart you will manually need to restart the process to continue recieving logs. This method is usefull for testing purposes.

2. Cronjob (using crontab)

   Use a cronjob to execute the script, based on a cron schedule. With this method a telegram-count can also be added to include x telegrams before posting. The advantage is that should the RPi restart, the cronjob will automatically continue to trigger the application without any manual intervention.

### Continuous loop

TODO

### Cronjob

TODO
