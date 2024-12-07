## A simple emulation of Poisson-governed image generation
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

# GUI event handlers' definitions
def poissonimg(val):
    global fig, rgbw, imrgb, imbw, bctrl
    λ = 2**(val - 8.0); β = 1 if bctrl else λ

    img = imrgb if rgbw == RGB else imbw
    imp = clip(poisson(img * λ)/β, 0, 0xff).astype(int)

    # Presentation stuff...
    # https://stackoverflow.com/questions/2265319/how-to-make-an-axes-occupy-multiple-subplots-with-pyplot
    gs = GridSpec(0b1100, 0b1100, figure = fig)
    ai, ah = fig.add_subplot(gs[:, :]), fig.add_subplot(gs[0b1:0b11, 0b1:0b110])
    ai.axis('off'); ah.axis('off'); ah.patch.set_alpha(1/0b10)

    data, colors = (imp.flatten(), 'black') if rgbw == BW else ([imp[:, :, _].flatten() for _ in range(0b11)], ('red', 'green', 'blue'))
    # we ignore both boundary values, 0 and 255, for a reason... So you don't have to...
    ah.hist(data, 0x100 - 0b10, (0x1, 0xfe), color = colors, stacked = True, histtype = 'bar', alpha = 1/0b100)
    ai.imshow(imp, cmap = 'gray' if rgbw == BW else None)
    # https://stackabuse.com/how-to-change-plot-background-in-matplotlib/
    show()

def scotophotopic(label):
    global slev, rgbw

    rgbw = RGB if label == 'RGB' else BW
    poissonimg(slev.val)

def bctrl(label):
    global slev, bctrl

    bctrl = label == 'Raw'
    poissonimg(slev.val)

# GUI elements...
fig, ax = subplots(num = "Nihil novi sub stella..."); subplots_adjust(left = .25, bottom = .25)
axev, axc, axb = axes([.25, .1, .65, .03]), axes([.025, .5, .20, .15]), axes([.025, .70, .20, .15])
# ... and their settings
for _ in (axev, axc, axb, ax): _.axis('off')
slev, slsp, slbr = (Slider(axev, 'EV', 0o0, 0x10, valinit = 0o10, valstep = 0b1),
                    RadioButtons(axc, ('RGB', 'B&W'), active = 0),
                    RadioButtons(axb, ('Adjusted', 'Raw'), active = 0))
slev.on_changed(poissonimg); slsp.on_clicked(scotophotopic); slbr.on_clicked(bctrl)

# Image re/de-generation
rgbw, mb, bctrl = RGB, f'./images/MB{choice("ABCD")}.png', False
imrgb, imbw = cvtColor(imread(mb), RGB), cvtColor(imread(mb), BW)
poissonimg(0o10)