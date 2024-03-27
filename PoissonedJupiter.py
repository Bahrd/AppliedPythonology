from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as GRAY, resize
from matplotlib.widgets import Slider, RadioButtons
from matplotlib import pyplot as plt, animation
from numpy.random import poisson
from numpy import clip
'''
A simple animation demonstrating Poisson distribution of faint images...
 https://stackoverflow.com/questions/33193696/matplotlib-animation-in-for-loop/41648966#41648966
 
 https://en.wikipedia.org/wiki/90482_Orcus#/media/File:Orcus-Vanth_orbit.gif
 https://en.wikipedia.org/wiki/Orbital_resonance
'''

## A (vanila) animation
#  A.k.a. alone callback function
def animate(_):
    global intensity, im, img, brightness
    
    λ = 2**(intensity - 8.0)        
    imp = clip(2**brightness * poisson(img * λ)/λ, 0x0, 0xff)
    im.set_array(imp.astype(int))

## A GUI part
#  A couple of event handlers
def poissonimg(_i):
    global intensity
    intensity = _i
   
def brightnimg(_b):
    global brightness
    brightness = _b
    
''' 
People vs frogs (vs machines) - the world-famous single-photon detection contest
1. https://www.sciencedaily.com/releases/2015/01/150120084545.htm
2. https://www.scientificamerican.com/article/the-human-eye-could-help-test-quantum-mechanics/
3. https://global.canon/en/technology/spad-sensor-2023.html
4. https://www.youtube.com/watch?v=o5qXCzknxn8 [PG]
'''
def photoscotopic(label):
    global img, jovi
    img = cvtColor(jovi, RGB if label == 'RGB' else GRAY)

## The main content: Jupiter and Io, Europa, Ganymede & Callisto... 
#                    [sans the remaining (~0.003%) plankton]
intensity, brightness = 8, 0

fig, _ = plt.subplots(num = 'Nihil novi sub Jovi... [3.12.23 at 21:16:18]')
plt.subplots_adjust(bottom = .25)

jovi = resize(imread('Jovi et consortes.JPG'), (0x140, 0o310)) # Good' ol' CGA...
img = cvtColor(jovi, GRAY)
im = plt.imshow(img, cmap = 'gray', interpolation = 'none')

## And a handful of elements
#  A pair of sliders...
axEV, axB, axc = (plt.axes(dims) for dims in ((.25, .1, .65, .03), (.92, .25, .03, .65), (.025, .01, .15, .15)))
slEV, slB = (Slider(axEV, 'EV', 0, 16, valinit = intensity, valstep = 1), 
             Slider(axB, 'Brightness', -4, 1, valinit = brightness, valstep = 0.25, orientation = 'vertical'))
slEV.on_changed(poissonimg), slB.on_changed(brightnimg)
# ... and a switch
radio = RadioButtons(axc, ('RGB', 'B&W'), active = 1)
radio.on_clicked(photoscotopic)


## "Lights, Camera, Action!" https://en.wikipedia.org/wiki/Clapperboard#Construction
anim = animation.FuncAnimation(fig, animate, cache_frame_data = False)
plt.show()