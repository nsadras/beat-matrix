from bibliopixel.drivers.network import DriverNetwork
from bibliopixel.led import LEDStrip
from bibliopixel.animation import *

import numpy as np
import pyaudio
import struct

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i)+'. '+dev['name']
            print dev
        i += 1
 
def analyze(data, width, sample_rate, bins):
    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = np.array(data2, dtype='h')
 
    # FFT black magic
    fourier = np.fft.fft(data2)
    ffty = np.abs(fourier[0:len(fourier)/2])/1000
    ffty1=ffty[:len(ffty)/2]
    ffty2=ffty[len(ffty)/2::]+2
    ffty2=ffty2[::-1]
    ffty=ffty1+ffty2
    ffty=np.log(ffty)-2
    
    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier)/2]
    
    size = len(fourier)
 
    # Split into desired number of frequency bins
    levels = [sum(fourier[i:(i+size/bins)]) for i in xrange(0, size, size/bins)][:bins]
    
    return levels


class StripTest(BaseStripAnim):
    def __init__(self, led, start=0, end=-1):
        #The base class MUST be initialized by calling super like this
        super(StripTest, self).__init__(led, start, end)
        
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
        
        self.chunk    = 2048 # Change if too fast/slow, never less than 1024
        self.scale    = 200   # Change if too dim/bright
        self.exponent = .5    # Change if too little/too much difference between loud and quiet sounds
        self.sample_rate = 44100 
        self.bins = 8 
        device   = 2  # Change to correct input device; use list_devices()
        
         
        p = pyaudio.PyAudio()
        self.stream = p.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = self.sample_rate,
                        input = True,
                        frames_per_buffer = self.chunk,
                        input_device_index = device)
        print "initialized"

    def step(self, amt = 1):
        data = self.stream.read(self.chunk)
        levels = analyze(data, self.chunk, self.sample_rate, self.bins)
        # scale to [0,100]
        for i in range(self.bins):
            levels[i] = max(min((levels[i]*1.0)/self.scale, 1.0), 0.0)
            levels[i] = levels[i]**self.exponent
            levels[i] = int(levels[i]*255)
        print levels 
        for i in range(self._led.numLEDs):
            self._led.set(i, (levels[0], levels[0], levels[0])) 

        #Increment the internal step by the given amount
        self._step += amt

list_devices()
#must init with same number of pixels as receiver
driver = DriverNetwork(45, host = "192.168.1.15")
led = LEDStrip(driver)
anim = StripTest(led)

while True:
    try:
        anim.run(sleep=50)
    except KeyboardInterrupt:
        break
    except:
        pass
