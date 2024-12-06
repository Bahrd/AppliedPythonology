## Cite as: https://link.springer.com/chapter/10.1007/978-3-030-12450-2_29
from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as BW
from matplotlib.pyplot import subplots, subplots_adjust, axes, show
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.gridspec import GridSpec
## https://matplotlib.org/3.2.1/gallery/widgets/slider_demo.html
from numpy.random import poisson
from numpy import clip
from random import choice

''' Warning: Never ignore warnings... ;) '''
import warnings; warnings.filterwarnings('ignore')

## A simple emulation of Poisson-governed image generation
# GUI event handlers
def poissonimg(val):
    global fig, rgbw, img_rgb, img_bw, brightness
    λ = 2**(val - 8.0); β = λ if brightness else 1

    img = img_rgb if rgbw == RGB else img_bw
    imp = clip(poisson(img * λ)/β, 0, 0xff).astype(int)

    # Presentation stuff...
    # https://stackoverflow.com/questions/2265319/how-to-make-an-axes-occupy-multiple-subplots-with-pyplot
    gs = GridSpec(12, 12, figure = fig)
    ai, ah = fig.add_subplot(gs[:, :]), fig.add_subplot(gs[1, 8:11])
    ai.axis('off'); ah.axis('off'); ah.patch.set_alpha(0.5)

    data, colors = (imp.flatten(), 'gray') if rgbw == BW else ([imp[:, :, _].flatten() for _ in range(3)], ('red', 'green', 'blue'))
    # we ignore the boundary values, 0 and 255, for a reason... So you don't have to...
    ah.hist(data, 254, (1, 254), color = colors, stacked = True, histtype = 'bar', density = True, alpha = .8)
    ai.imshow(imp, cmap = 'gray' if rgbw == BW else None)
    # https://stackabuse.com/how-to-change-plot-background-in-matplotlib/
    show()

def scotophotopic(label):
    global slEV, rgbw
    rgbw = RGB if label == 'RGB' else BW
    poissonimg(slEV.val)

def brightness(label):
    global slEV, brightness
    brightness = label == 'Normalize ON'
    poissonimg(slEV.val)

# GUI elements
fig, ax = subplots(num = "Nihil novi sub stella..."); subplots_adjust(left = .25, bottom = .25)
axEV, axc, axb = axes([.25, .1, .65, .03]), axes([.025, .5, .20, .15]), axes([.025, .70, .20, .15])

for _ in (axEV, axc, axb, ax): _.axis('off')
slEV, slsp, slbr = (Slider(axEV, 'EV', 0.0, 16.0, valinit = 8.0, valstep = 1.0),
                    RadioButtons(axc, ('RGB', 'B&W'), active = 0),
                    RadioButtons(axb, ('Normalize ON', 'Normalize OFF'), active = 1))
slEV.on_changed(poissonimg); slsp.on_clicked(scotophotopic); slbr.on_clicked(brightness)

# Image re/de-generation
rgbw, mb, brightness = RGB, f'./images/MB{choice("ABCD")}.png', False
img_rgb, img_bw = cvtColor(imread(mb), RGB), cvtColor(imread(mb), BW)
poissonimg(8)