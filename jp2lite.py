#%% Vanilla JPEG 2000 algorithm (more like a vanillin one, in fact:
#   neither EBCOT nor BAC is implemented whatsoever)
import numpy as np
import sys
import matplotlib.pyplot as plt
from numpy.random import poisson
from itertools import repeat
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from auxiliary import (displayImages as di,displayAnyChannels as dac,
                       YCbCr_ext_channels as YCbCr,
                       RGB_ext_channels as RGB,
                       RGB2YCbCr, YCbCr2RGB)
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
if λ > 0: img = np.clip(poisson(img * 2**λ)/2**λ, 0x0, 0xff)
di(img.astype(np.uint8), f'{art}', grid = False)

#   A native RGB color space channels
dac(img, RGB); cgh(img, art, 'RGB', RGB)

#%% An irréversible color transform (ICT)
img = img@RGB2YCbCr.T
dac(img, YCbCr); cgh(img, art, 'YCbCr (before)', YCbCr)

#%% ... the wavelet transform and quantization...
Y, Cb, Cr = [wt4tw(img[..., n], wn, L, Q, qntz, ('Y', 'Cb', 'Cr')[n]) for n in range(3)]
img = np.array(np.dstack((Y, Cb, Cr)))

# ... and after
dac(img, YCbCr); cgh(img, art, 'YCbCr (after)', YCbCr, DC = False)

#%% Grand finale!
#   ... with the inverse ICT...
img = img@YCbCr2RGB.T; img = np.clip(img, 0x0, 0xff)
di(img.astype(np.uint8), f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})', grid = False)

### Let us digress a bit... (edge detection)
#   Wavelet multiresolution analysis (MRA) visualization
#   See https://pywavelets.readthedocs.io/en/latest/
#   Illustrated here for the luminance ('Y', grayscale) channel
#   from the YCoCg space and the "grandpas" of all wavelets: the Haar family!
from pywt import dwt2, idwt2
import matplotlib.pyplot as plt
A, wn = lambda x, a = 0x40, l = -0xff, h = 0xff: np.clip(a*x, l, h), 'Haar'
titles = [f'{wn} approximation (LL)', 'Horizontal details (HL)',
           'Vertical details (LH)',   'Diagonal details (HH)']
img = plt.imread(f'./images/{art}.png')[..., :3]
img = img@RGB2YCbCr.T
Y = img[..., 0]
LL, (HL, LH, HH) = dwt2(Y, wn)
di([LL, A(HL), A(LH), A(HH)], titles, grid = False)
Y = idwt2((LL, (HL, LH, HH)), wn)
di([Y, Y - img[..., 0]], ['DWT⁻¹(DWT(Y)) → ⌊…⌋ ?', 'Zero, zip, zilch, nada?'], grid = False)

'''
Scrapyard:
art = 'Pollock No. 5' # https://blogs.uoregon.edu/richardtaylor/2016/02/08/fractal-analysis-of-jackson-pollocks-poured-paintings/
art = 'Malewicz I'    # a.k.a. 'Negroes Fighting in a Cellar at Night' by Allais 1897
art = 'Malewicz II'   # or 'Bociany albinosy pośród śnieżnej zamieci' by OT.TO 1997
art = 'Rothko'        # vel 'Orange, Red, Yellow' 1961
art = 'BayerLCD'      # Color channel test pattern (Rothko & Malewicz would surely
                      # have been proud of me! ;)
#  Hard thresholding:
from pywt import threshold as thrsd; qntz = lambda x, T: thrsd(x, T, mode = 'hard')
'''