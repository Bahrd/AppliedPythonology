from matplotlib import pyplot as plt
from matplotlib import animation

from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as GRAY, resize
from matplotlib.widgets import Slider, RadioButtons
## https://matplotlib.org/3.2.1/gallery/widgets/slider_demo.html
from numpy.random import poisson
from numpy import clip

## An animation part
# https://stackoverflow.com/questions/33193696/matplotlib-animation-in-for-loop/41648966#41648966
val = 8
def animate(_):
    global val, img
    
    λ = 2**(val - 8.0)        
    imp = clip(poisson(img * λ)/λ, 0x0, 0xff).astype(int)
    im.set_array(imp)
    return im,

# An infinite loop
def dummies():
    yield 1

## A GUI part
# A pair of event handlers
def poissonimg(_val):
    global val
    val = _val
        
def scotophotopic(label):
    global img, jovi, slEV
    img = cvtColor(jovi, RGB if label == 'RGB' else GRAY)

# The main content
fig, _ = plt.subplots(num = "Nihil novi sub Jovi..."); plt.subplots_adjust(bottom = .25)
jovi = resize(imread('Jovi et consortes.JPG'), (0x140, 0o310)) # Good' ol' CGA...
img = cvtColor(jovi, GRAY)
im = plt.imshow(img, cmap = 'gray', interpolation = 'none')

# And an associated couple of elements
axEV, axc = plt.axes([.25, .1, .65, .03]), plt.axes([.025, .01, .15, .15])
slEV = Slider(axEV, 'EV', 0.0, 16.0, valinit = 8.0, valstep = 1.0); slEV.on_changed(poissonimg)
radio = RadioButtons(axc, ('RGB', 'B&W'), active = 1); radio.on_clicked(scotophotopic)

anim = animation.FuncAnimation(fig, animate, frames = dummies, cache_frame_data = False, blit = True)
plt.show(block = True)
