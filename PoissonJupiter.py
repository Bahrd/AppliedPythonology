from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as GRAY, resize
## https://matplotlib.org/3.2.1/gallery/widgets/slider_demo.html
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

## An animation part
val = 8
# A callback function
def animate(_):
    global val, img
    
    λ = 2**(val - 8.0)        
    imp = clip(poisson(img * λ)/λ, 0x0, 0xff).astype(int)
    im.set_array(imp)
    return im,

# An infinite loop provider
def dummies():
    yield 1

## A GUI part
# A pair of event handlers
def poissonimg(_val):
    global val
    val = _val
        
def scotophotopic(label):
    global img, jovi
    img = cvtColor(jovi, RGB if label == 'RGB' else GRAY)


## The main content: Jupiter and Io, Europa, Ganymede & Callisto... 
#                    [and the remaining (~0.003%) plankton]
fig, _ = plt.subplots(num = "Nihil novi sub Jovi... [3.12.23 at 21:16:18]"); plt.subplots_adjust(bottom = .25)
jovi = resize(imread('Jovi et consortes.JPG'), (0x140, 0o310)) # Good' ol' CGA...
img = cvtColor(jovi, GRAY)
im = plt.imshow(img, cmap = 'gray', interpolation = 'none')

# And an associated couple of elements
axEV, axc = plt.axes([.25, .1, .65, .03]), plt.axes([.025, .01, .15, .15])
slEV = Slider(axEV, 'EV', 0.0, 16.0, valinit = 8.0, valstep = 1.0); slEV.on_changed(poissonimg)
radio = RadioButtons(axc, ('RGB', 'B&W'), active = 1); radio.on_clicked(scotophotopic)

## "Lights, Camera, Action" https://en.wikipedia.org/wiki/Clapperboard#Construction
anim = animation.FuncAnimation(fig, animate, frames = dummies, cache_frame_data = False, blit = True)
plt.show(block = True)
