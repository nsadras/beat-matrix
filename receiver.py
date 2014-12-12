from bibliopixel.drivers.network_receiver import NetworkReceiver
from bibliopixel.drivers.WS2801 import *
from bibliopixel.led import LEDStrip
from time import sleep
#must init with same number of pixels as sender
driver = DriverWS2801(45)
led = LEDStrip(driver)

receiver = NetworkReceiver(led)
receiver.start() #returns immediately, must loop or do other work 

while True:
    sleep(1)
