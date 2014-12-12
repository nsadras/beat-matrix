from bibliopixel.drivers.network import DriverNetwork
from bibliopixel.led import LEDStrip

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


#must init with same number of pixels as receiver
driver = DriverNetwork(45, host = "192.168.0.105")
led = LEDStrip(driver)

anim = StripTest(led)
anim.run(sleep=500)
