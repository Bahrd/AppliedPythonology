#%% Vanilla JPEG 2000 algorithm (more like a vanillin one, in fact:
#   neither EBCOT nor BAC is implemented whatsoever)
import numpy as np, sys, matplotlib.pyplot as plt
from numpy.random import poisson
from itertools import repeat
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from auxiliary import (displayImages as di,displayAllChannels as dac,
                       YCbCr_ext_channels as YCbCr,
                       RGB_ext_channels as RGB,
                       RGB2YCbCr, YCbCr2RGB)
#   No gradient, no gain! ;)
from histogramXYZ import channelGradientHistogram as cgh

#   Wavelet transform coefficients operation palindrome
def wt4tw(c, wn, lvl, Q, op = lambda x, Q: x, channel = 'Y'):
    # Applying a wavelet transform
    C = fwt2(c, wn, level = lvl)
    # Performing operation (quantization in JPEG 2000)
    # on 'de-tupled' wavelet coefficients 'C'
    C, S = c2a(C); C = list(map(op, C, repeat(Q)))
    # In the real JPEG 2000 the coefficients are here encoded,
    # bit layer after bit layer (for instance).

    # Displaying percentage of remaining coefficients
    # (w.r.t. the image size)
    CC = np.block(C).flat; CCC, CV = sum((CC)!= 0), c.size
    print(f'Non-zeros in {channel}: {CCC} of {CV} → {CV/CCC:.0f}x')

    # Re-tupling the wavelet coefficients
    C = a2c(C, S, output_format = 'wavedec2')
    # Inversing the wavelet transform
    return ifwt2(C, wn)

# Still a somehow horse-related creature...
art = 'GrassHopper' # pseud. Philip [gr. "friend of horses"]!... ;)

#%% JPEG 2000 main 'codec'
qntz = lambda x, Q: np.floor(x*2**Q + .5)/2**Q
#   Interactive-aware wavelet transform parameters setting
#   https://en.wikipedia.org/wiki/Cohen-Daubechies-Feauveau_wavelet#Numbering
#   'bior1.1', 'bior2.2', 'bior4.4' = 'Haar', 'LGT 5/3', 'CDF 9/7'
wn, λ, L, Q = 'bior2.2', 0, 0b100, -0b111
if hasattr(sys, 'ps1'):
    wn, λ, L, Q = 'bior4.4', 0o10, 0b101, -0b101
elif len(sys.argv) > 1:
    wn, λ, L, Q = eval(sys.argv[1])
#   Pick your own (floating) poison...  (for instance λ = 4.0).
#   And then spice it up with e.g. λ = 0x4 ;D)
img = np.array(plt.imread(f'./images/{art}.png')[..., :3] * 0xff)
if λ > 0: img = poisson(img * 2**λ)/2**λ

#   There we go!
di(img.astype(np.uint8), f'{art}', grid = False)

#   A native RGB color space channels
dac(img, RGB)
cgh(img, art, 'RGB', RGB)

#%% An irréversible color transform (ICT) from RGB to YCbCr (ever heard of 4:2:0?)
img = img@RGB2YCbCr.T
dac(img, YCbCr)
cgh(img, art, 'YCbCr (before)', YCbCr)

#%% ... the wavelet transform and quantization...
Y, Cb, Cr = [wt4tw(img[..., n], wn, L, Q, qntz, ('Y', 'Cb', 'Cr')[n]) for n in range(3)]

# ... and after
img = np.array(np.dstack((Y, Cb, Cr)))
dac(img, YCbCr)
cgh(img, art, 'YCbCr (after)', YCbCr, DC = False)

#%% Grand finale!
#   ... with the inverse ICT...
img = img@YCbCr2RGB.T
di(img, f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})', grid = False)
#%% Et finis coronat opus...