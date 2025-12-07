''' Warning: Never ignore warnings... ;) '''
import warnings; warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from numpy import linspace as lp, random, size, sort, sqrt, cumsum, arange, argmin, ceil

#Live thresholding - with a bit of a rehearsal... ;)
from matplotlib.widgets import Slider, RadioButtons
from pywt import (wavedec as fwt, waverec as ifwt, threshold as thrsd,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
L, rng = 0o1000, random.default_rng()
rpt = 0b11
'''
## Signal (PPG-like, say) generation
from numpy import sqrt, sin
from itertools import repeat
from more_itertools import flatten
from math import pi as π
X, (f1, f2) = lp(-1.0, 1.0, L), (0b10, 0b100) #Hz

S, ε  = (3 + sqrt(2)*sin(f1 * π*X) + 2*sin(f2 * π*X),
         rng.standard_normal(L * rpt)/0b100)
s = list(flatten(repeat(S, rpt)))
'''

#'''
# A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
# https://www.youtube.com/watch?v=iphcyNWFD10 - Veritasium's take on it
# https://www.youtube.com/watch?v=B4XzLDM3Py8 - MIT
from numpy import sin
X = lp(0.05, 1.0, L * rpt)
s, ε = sin(1/X), rng.standard_normal(L * rpt)/0b100
#'''

S = s + ε

# ... and a real drama: Wavelet Thresholding!
# An FWT wrapper (transform → operation on coefficients → inverse transform)
def wc_op(c, wn, lvl, h, op = lambda x, h: x, dsply = False):
    # Applying a wavelet transform
    C = fwt(c, wn, level = lvl)

    # Thresholding I
    C, S = c2a(C); C = op(C, h)
    # Presentation
    if(dsply): plt.plot(C); plt.show()
    # Re-tupling the wavelet coefficients
    C = a2c(C, S, output_format = 'wavedec')
    # Inversing the wavelet transform
    return ifwt(C, wn)

# See the source https://github.com/holgern/pyyawt/ for the reference
def ValSUREThresh(X):
    n = size(X)
    a = sort(abs(X))**2

    c = lp(n - 1, 0, n)
    s = cumsum(a) + c * a
    risk = (n - (2 * arange(n)) + s)/n

    ibest = argmin(risk)
    THR = sqrt(a[ibest])
    return THR

''' Levels of transform, L, is arbitrary here. In general,
    L ≤ floor(log₂(len(X))
    or even less should a boundary effect be taken into account.
    Insert your own threshold values should you know it better, as well'''
L, sh = 10, ValSUREThresh(S); h = sh
Th = lambda x, h: thrsd(x, h, mode = 'hard')

''' A selection of wavelet filter names
https://pywavelets.readthedocs.io/en/latest/ref/wavelets.html for the entire family'''

wns, modes = (['sym8 [symlet]', 'coif8 [coiflet]', 'db8 [Daubechies]', 'bior4.4 [CDF]', 'bior2.2 [LeGall]', 'bior1.1 [Haar]'],
              ['hard', 'soft', 'garrote'])
wn, mode = wns[0].split()[0], modes[0]

# Shrinkage... Live!
def refresh():
    global S, wn, L, h, Th
    dft = wc_op(S, wn, L, h, Th)
    
    # Extravaganza... ;)
    for f, a in zip(('subplot', 'cla', 'xticks', 'yticks', 'title'), 
                    ('1, 1, 1', '', '[]', '[]', "f'{wn} @ λ = {h:,.2f}'")):
        eval(f'plt.{f}({a})')    
    
    plt.plot(dft, 'xkcd:black', s, 'xkcd:red', s - dft, 'xkcd:gray')
    plt.plot(S, color ='xkcd:light gray', marker = '.', markersize = 1, lw = 0)
    plt.show()

def threshold(_):
    global h; h = _
    refresh()

def wavelets(_):
    global wn; wn = _.split()[0] # "Separate the Wheat from the Chaff" - or just separate the standard wavelet family name
    refresh()                      # from the one that "gives credit where credit is due!"

def method(_):
    global Th, mode
    mode = _; Th = lambda x, h: thrsd(x, h, mode = mode)
    refresh()

# Presentation arrangement...
plt.subplots(num = 'Wavelets in their niche (natural habitat...?)'); plt.subplots_adjust(left = .2, bottom = .16)
plt.tight_layout()
axTh, axWn, axM  = plt.axes([.01, .15, .03, .7]), plt.axes([.1, .01, .3, .12]), plt.axes([.31, .01, .15, .12])
slTh = Slider(axTh, 'λ', 0.0, 2*ceil(sh), valinit = sh, valstep = 0.03125 * sh, orientation = 'vertical')
rbWn = RadioButtons(axWn, wns, active = 0); rbM = RadioButtons(axM, modes, active = 0)
slTh.on_changed(threshold); rbWn.on_clicked(wavelets); rbM.on_clicked(method)

threshold(h)