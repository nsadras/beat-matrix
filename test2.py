from bibliopixel.led import *
from bibliopixel.animation import *
from bibliopixel.drivers.WS2801 import *
import bibliopixel.colors as colors
from time import sleep
class StripTest(BaseStripAnim):
    def __init__(self, led, start=0, end=-1):
        #The base class MUST be initialized by calling super like this
        super(StripTest, self).__init__(led, start, end)
        #Create a color array to use in the animation
        #self._colors = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo]
        self._colors = [colors.DarkBlue]

    def step(self, amt = 1):
        #Fill the strip, with each sucessive color 
        for i in range(self._led.numLEDs):
            self._led.set(i, self._colors[(self._step + i) % len(self._colors)])
        #Increment the internal step by the given amount
        self._step += amt

#create driver for a 12 pixels
driver = DriverWS2801(44)
led = LEDStrip(driver)
sleep(3)
led.fill(colors.Orange)
sleep(3)
#anim = StripChannelTest(led)
#anim = StripTest(led)
#anim.run(sleep=500)
