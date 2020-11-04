#!/usr/bin/env python

############################################################
# This code uses the Beebotte API, you must have an account.
# You can register here: http://beebotte.com/register
############################################################

import time
import board
import adafruit_dht
from beebotte import *

### Replace API_KEY and SECRET_KEY with those of your account
with open("../Private/apikeys.txt", "rt") as fin:
    API_KEY = fin.readline().strip()
    SECRET_KEY = fin.readline().strip()
bbt = BBT(API_KEY, SECRET_KEY)

period = 60 ## Sensor data reporting period (1 minute)
pin = 4 ## Assuming the DHT11 sensor is connected to GPIO pin number 4

### Change channel name and resource names as suits you
temp_resource   = Resource(bbt, 'RaspberryPi', 'temperature')
humid_resource  = Resource(bbt, 'RaspberryPi', 'humidity')

dhtDevice = adafruit_dht.DHT22(board.D4)

def run():
  while True:
    ### Assume
    humidity, temperature = dhtDevice.temperature, dhtDevice.humidity
    if humidity is not None and temperature is not None:
        print("Temp={0:f}*C  Humidity={1:f}%").format(temperature, humidity)
        try:
          #Send temperature to Beebotte
          temp_resource.write(temperature)
          #Send humidity to Beebotte
          humid_resource.write(humidity)
        except Exception:
          ## Process exception here
          print("Error while writing to Beebotte")
    else:
        print("Failed to get reading. Try again!")

    #Sleep some time
    time.sleep( period )

run()