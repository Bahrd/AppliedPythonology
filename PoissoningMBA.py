## A simple emulation of Poisson-governed image generation
## Cite as: https://link.springer.com/chapter/10.1007/978-3-030-12450-2_29
from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as BW
from matplotlib.pyplot import subplots, subplots_adjust, axes, show
from matplotlib.widgets import Slider, RadioButtons as RadioB
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

    img = imrgb if rgbw == RGB else imbw
    λ = 2**(val - 8.0)
    β = λ**bctrl        # Note how "β-smart" we are! ;)

    imp = clip(poisson(img * λ)/β, 0, 0x100 - 0o1).astype(int)

    # Presentation stuff...
    # https://stackoverflow.com/questions/2265319/how-to-make-an-axes-occupy-multiple-subplots-with-pyplot
    gs = GridSpec(0x10, 0x10, figure = fig)
    oh, ah = fig.add_subplot(gs[:, :]), fig.add_subplot(gs[0b10:0b100, 0b1:0b111])
    oh.axis('off'); ah.axis('off')

    data, colors = (imp.flatten(), 'lightgray') if rgbw == BW else ([imp[:, :, _].flatten() for _ in range(0b11)], ('red', 'green', 'blue'))
    # we ignore both boundary values, 0 and 255, for a reason... So you don't have to...
    ah.hist(data, 0x100 - 0b10, (0x1, 0x100 - 0b10), color = colors, stacked = True, histtype = 'bar', alpha = 1/0b11)
    oh.imshow(imp, cmap = 'gray' if rgbw == BW else None)
    # https://stackabuse.com/how-to-change-plot-background-in-matplotlib/
    show()

def scotophotopic(label):
    global slev, rgbw

    rgbw = eval(label)
    poissonimg(slev.val)

def bctrl(label):
    global slev, bctrl

    bctrl = label == 'Adjusted'
    poissonimg(slev.val)

# GUI elements...
fig, ax = subplots(num = "Nihil novi sub stella..."); subplots_adjust(left = .2, bottom = .15, top = .95, right = .9)
axs = [axes(_) for _ in ([.2, .1, .7, .03], [.025, .4, .20, .1], [.025, .5, .20, .1])]
# ... and their settings
for _ in (*axs, ax): _.axis('off')
slev, slsp, slbr = (Slider(axs[0], 'EV', 0o0, 0x10, valinit = 0o10, valstep = 0b1),
                    RadioB(axs[1], ('RGB', 'BW'), active = 0),
                    RadioB(axs[2], ('Adjusted', 'Raw'), active = 0))
slev.on_changed(poissonimg); slsp.on_clicked(scotophotopic); slbr.on_clicked(bctrl)

# Global variables
bctrl:bool = True # Unnecessary pedantry...
rgbw, mb = RGB, f'./images/MB{choice("ABCD")}.png'
imrgb, imbw = cvtColor(imread(mb), RGB), cvtColor(imread(mb), BW)

# Image re/de-generation
poissonimg(0o10)