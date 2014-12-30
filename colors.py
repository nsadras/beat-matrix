from bibliopixel.drivers.network import DriverNetwork
from bibliopixel.led import LEDStrip
from bibliopixel.animation import *

class StripTest(BaseStripAnim):
    def __init__(self, led, start=0, end=-1):
        #The base class MUST be initialized by calling super like this
        super(StripTest, self).__init__(led, start, end)
        #Create a color array to use in the animation
        christmas = [colors.Red, colors.Green, colors.White]
        rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo, colors.Violet]
        ocean = [colors.DarkBlue, colors.Blue, colors.Teal, colors.Turquoise]
        fire = [colors.Red, colors.Orange, colors.DarkOrange, colors.OrangeRed, colors.DarkRed]
        forest = [colors.DarkOliveGreen, colors.Green, colors.LightGreen, colors.DarkGreen, colors.LawnGreen]
        cool = [colors.Blue, colors.Green, colors.DarkBlue, colors.DarkViolet, colors.Indigo, colors.Teal, colors.DarkTurquoise]
        tron = [(0xDF, 0x74, 0xC), (0x6F, 0xC3, 0xDF), (0x0C, 0x14, 0x1F)]
        dark = [colors.DarkCyan, colors.DarkBlue, colors.DarkGreen]
        periwinkle = [colors.SlateBlue]
        test = [colors.DarkBlue]
        sparse = [colors.Black, colors.Black, colors.Black, colors.Black, colors.Black, colors.Black, colors.Black, colors.Black, colors.Black, colors.DarkBlue]
        purple = [colors.Purple, colors.Violet, colors.DarkViolet]
        off = [colors.Black]
        self._colors = fire 

    def step(self, amt = 1):
        #Fill the strip, with each sucessive color 
        for i in range(self._led.numLEDs):
            self._led.set(i, self._colors[(self._step + i) % len(self._colors)])
        #Increment the internal step by the given amount
        self._step += amt


#must init with same number of pixels as receiver
driver = DriverNetwork(45, host = "192.168.1.15")
led = LEDStrip(driver)

anim = StripTest(led)
while True:
    try:
        anim.run(sleep=500)
    except KeyboardInterrupt:
        break
    except:
        pass
