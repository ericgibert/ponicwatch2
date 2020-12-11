###  # ! /usr/bin/env python

############################################################
# This code uses the Beebotte API, you must have an account.
# You can register here: http://beebotte.com/register
############################################################

import time
try:
    import board
    import adafruit_dht
except NotImplementedError:
    pass
from beebotte import *
from config import Config

### Replace API_KEY and SECRET_KEY with those of your account
# with open("../Private/apikeys.txt", "rt") as fin:
#     API_KEY = fin.readline().strip()
#     SECRET_KEY = fin.readline().strip()
cfg =Config("../Private/config.txt")
bbt = BBT(cfg["API_KEY"], cfg["SECRET_KEY"])

period = 60 ## Sensor data reporting period (1 minute)
pin = 4 ## Assuming the DHT11 sensor is connected to GPIO pin number 4

### Change channel name and resource names as suits you
pilot = cfg["SYSTEMS"]["Pilot"]
print(pilot)
dht22 = pilot["DHT22"]
print(board.D18)
temp_resource   = Resource(bbt, 'Pilot', 'Air_Temperature')
humid_resource  = Resource(bbt, 'Pilot', 'Air_Humidity')

dhtDevice = adafruit_dht.DHT22(board.D18)

def run():
  while True:
    ### Assume
    temperature, humidity  = dhtDevice.temperature, dhtDevice.humidity
    if humidity is not None and temperature is not None:
        print("Temp={0:f}*C  Humidity={1:f}%".format(temperature, humidity))
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
