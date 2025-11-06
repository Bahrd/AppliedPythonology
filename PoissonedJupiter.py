from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as GRAY, resize
from matplotlib.widgets import Slider, RadioButtons
from matplotlib import pyplot as plt, animation
from numpy.random import poisson
from numpy import clip
from exif import Image as exifImage
'''
A simple animation demonstrating Poisson distribution of the faint images...
 https://stackoverflow.com/questions/33193696/matplotlib-animation-in-for-loop/41648966#41648966

 https://en.wikipedia.org/wiki/90482_Orcus#/media/File:Orcus-Vanth_orbit.gif
 https://en.wikipedia.org/wiki/Orbital_resonance
'''

## A (vanilla) animation, a.k.a. a callback function
def animate(_):
    global intensity, photo, image, brightness

    λ = 2**(intensity - 8.0)
    imp = clip(2**brightness * poisson(image * λ)/λ, 0x0, 0xff)
    photo.set_array(imp.astype(int))

## A GUI part
#  A couple of event handlers
def image_in_poisson(_):
    global intensity
    intensity = _

def image_in_brightness(_):
    global brightness
    brightness = _

'''
People vs frogs (vs machines) - the world-famous single-photon detection contest
1. https://www.sciencedaily.com/releases/2015/01/150120084545.htm
2. https://www.scientificamerican.com/article/the-human-eye-could-help-test-quantum-mechanics/
3. https://global.canon/en/technology/spad-sensor-2023.html
4. https://www.youtube.com/watch?v=o5qXCzknxn8 [PG]
'''
def photomesoscotopic(_):
    global image, yuppie
    image = cvtColor(yuppie, RGB if _ == 'RGB' else GRAY)

## The main content: Jupiter and Io, Europa, Ganymede & Callisto...
#                    [sans the remaining (~0.003%) plankton]
intensity, brightness = 8, 0

JoviEtConsortes =  './images/cosmos/Jovi, Io, Europa, Ganymede & Callisto.JPEG' #'./images/cosmos/Jovi et consortes.PNG'
with open(JoviEtConsortes, 'rb') as _: exf = exifImage(_)
# One should check if the GPS data are present (exf.list_all()), and the corresponding attributes exist, but let's
# make it an exercise for the reader... https://readthedocs.org/projects/exif/downloads/pdf/latest/
fig, _ = plt.subplots(num = f'Nihil novi sub Jovi... at [{exf.gps_longitude[0]:.0f}°, {exf.gps_latitude[0]:.0f}°]')
plt.subplots_adjust(bottom = .15, left = .05, top = .95)
_.xaxis.set_visible(False), _.yaxis.set_visible(False)


yuppie = resize(imread(JoviEtConsortes), (0x140, 0o310)) # Good' ol' CGA...
image = cvtColor(yuppie, GRAY)
photo = plt.imshow(image, cmap = 'gray', interpolation = 'none')


## And a handful of GUI elements
#  A pair of sliders...
axEV, axB, axc = (plt.axes(dims) for dims in ((.25, .1, .65, .03), (.92, .25, .03, .65), (.025, .01, .10, .10)))
slEV, slB = (Slider(axEV, 'EV', 0, 16, valinit = intensity, valstep = 1),
             Slider(axB, 'Brightness', -2.0, .5, valinit = brightness, valstep = 0.125, orientation = 'vertical'))
slEV.on_changed(image_in_poisson), slB.on_changed(image_in_brightness)
# ... and a switch
radio = RadioButtons(axc, ('RGB', 'B&W'), active = 1)
radio.on_clicked(photomesoscotopic)


## "Lights, Camera, Action!" https://en.wikipedia.org/wiki/Clapperboard#Construction
anim = animation.FuncAnimation(fig, animate, cache_frame_data = False)
plt.show()