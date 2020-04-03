## See https://matplotlib.org/3.2.1/gallery/widgets/slider_demo.html
import cv2
import numpy as np
from numpy.random import poisson
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

## A simple emulation of Poisson-governed image generation
# GUI event handlers
def poissonimg(val):
    global img
    λ = 2**val
    imp = np.clip(poisson(img * λ)/λ, 0, 0xff).astype(int)
    plt.subplot(1, 1 ,1); plt.title('{0}EV'.format(val))
    plt.imshow(imp, cmap = 'gray')

def scotophotopic(label):
    global img, fig
    img = cv2.imread("GrassHopper.PNG")
    cvt = cv2.COLOR_BGR2RGB if label == 'RGB' else cv2.COLOR_BGR2GRAY
    img = cv2.cvtColor(img, cvt)
    plt.subplot(1, 1, 1); plt.imshow(img, cmap = 'gray'); fig.canvas.draw_idle() 

# GUI elements
fig, _ = plt.subplots()
axEV, axc = plt.axes([.25, .1, .65, .03]), plt.axes([.025, .5, .15, .15])
slEV = Slider(axEV, 'EV', -10.0, 10.0, valinit = 0, valstep = .5)
radio = RadioButtons(axc, ('RGB', 'B&W'), active = 0)
slEV.on_changed(poissonimg); radio.on_clicked(scotophotopic)
plt.subplots_adjust(left = .25, bottom = .25); plt.subplot(1, 1, 1)

# Image re/de-generation
img = cv2.cvtColor(cv2.imread("GrassHopper.PNG"), cv2.COLOR_BGR2RGB)
plt.title('0EV'); plt.imshow(img); plt.show()