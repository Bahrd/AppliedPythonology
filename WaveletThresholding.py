''' Warning: Never ignore warnings... ;) '''
import warnings; warnings.filterwarnings('ignore')

#Live thresholding
from matplotlib.widgets import Slider, RadioButtons
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from pywt import (wavedec as fwt, waverec as ifwt, threshold as thrsd, 
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
from itertools import repeat; from more_itertools import flatten
import numpy as np
import math

## Signal (PPG-like) generation 
L, rng = 0o2000, np.random.default_rng()
X, rpt, (f1, f2) = np.linspace(-1.0, 1.0, L), 0b11, (0b10, 0b100) #Hz

S, ε  = (3 + np.sqrt(2)*np.sin(f1 * math.pi * X) + 2*np.sin(f2 * math.pi * X), 
         rng.standard_normal(L * rpt)/0b100)
s = list(flatten(repeat(S, rpt)))

#'''
# A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
X = np.linspace(0.05, 1.0, L * rpt)
s, ε = np.sin(1/X), rng.standard_normal(L * rpt)/0b100
#'''
S = s + ε

# A FWT wrapper (transform → operation on coefficients → inverse transform)
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
    n = np.size(X)
    a = np.sort(np.abs(X))**2

    c = np.linspace(n - 1, 0, n)
    s = np.cumsum(a) + c * a
    risk = (n - (2 * np.arange(n)) + s)/n

    ibest = np.argmin(risk)
    THR = np.sqrt(a[ibest])
    return THR

''' Levels of transform, L, is arbitrary here. In general, 
    L ≤ floor(log₂(len(X)) 
    or even less should a boundary effect be taken into account. 
    Insert your own threshold values should you know it better, as well'''
L, sh = 10, ValSUREThresh(S); h = sh
Th = lambda x, h: thrsd(x, h, mode = 'hard')

''' A selection of wavelet filter names 
https://pywavelets.readthedocs.io/en/latest/ref/wavelets.html for the entire family'''

wns, modes = (['sym8', 'coif8', 'db8', 'bior4.4', 'bior2.2', 'bior1.1'], 
              ['hard', 'soft', 'garrote'])
wn, mode = wns[0], modes[0]

# Shrinkage... Live!
def display():
    global S, wn, L, h, Th
    dft = wc_op(S, wn, L, h, Th)
    plt.subplot(1, 1, 1)
    plt.cla()
    plt.xticks([]); plt.yticks([])
    plt.title(f'{wn} @ λ = {h:,.2f}')
    _ = (plt.plot(dft, 'k', s, 'r'), plt.plot(s - dft, color ='gray'),
         plt.plot(S, color ='lightgray', marker = '.', markersize = 1, linewidth = 0), plt.show())
def thresh_live(λ):
    global h; h = λ
    display()
def family_live(_wn):
    global wn; wn = _wn
    display()
def mode_live(_mode):
    global Th, mode; 
    mode = _mode; Th = lambda x, h: thrsd(x, h, mode = mode)
    display()

_ = plt.subplots(); plt.subplots_adjust(left = .1, bottom = .16)
axTh, axWn, axM  = plt.axes([.57, .01, .33, .03]), plt.axes([.1, .01, .3, .12]), plt.axes([.31, .01, .15, .12])
slTh = Slider(axTh, 'λ = ', 0.0, np.ceil(2*sh), valinit = sh, valstep = 0.03125 * sh)
rbWn = RadioButtons(axWn, wns, active = 0); rbM = RadioButtons(axM, modes, active = 0)
slTh.on_changed(thresh_live); rbWn.on_clicked(family_live); rbM.on_clicked(mode_live)

thresh_live(h)