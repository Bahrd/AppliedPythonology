## See https://matplotlib.org/3.2.1/gallery/widgets/slider_demo.html
from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as GRAY
from numpy import clip
from numpy.random import poisson, randint as RI
from matplotlib.pyplot import subplots, subplots_adjust, axes
from matplotlib.widgets import Slider, RadioButtons
from auxiliary import displayImages as DI

## A simple emulation of Poisson-governed image generation
# GUI event handlers
def poissonimg(val):
    global img
    λ = 2**(val - 8.0); imp = clip(poisson(img * λ)/λ, 0, 0xff).astype(int)
    DI(imp, '{0}EV'.format(val))

def scotophotopic(label):
    global img, fig, mb, slEV
    img = cvtColor(imread(mb), RGB if label == 'RGB' else GRAY)
    DI(img); slEV.reset(); fig.canvas.draw_idle() # Forces image refresh

# GUI elements
fig, _ = subplots(); subplots_adjust(left = .25, bottom = .25)

axEV, axc = axes([.25, .1, .65, .03]), axes([.025, .5, .15, .15])
slEV = Slider(axEV, 'EV', 0.0, 16.0, valinit = 8.0, valstep = 1.0)
radio = RadioButtons(axc, ('RGB', 'B&W'), active = 0)
slEV.on_changed(poissonimg); radio.on_clicked(scotophotopic)

# Image re/de-generation
mb = 'MB{0}.png'.format(['A', 'B', 'C', 'D'][RI(4)])
img = cvtColor(imread(mb), RGB); DI(img, '8EV')