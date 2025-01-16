#%% Vanilla JPEG 2000 algorithm
# (more like a vanillin one, in fact: neither EBCOT nor BAC is implemented whatsoever)
import cv2 as openCV; import numpy as np
from numpy.random import poisson
from itertools import repeat
#%% https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from pywt import dwt2, idwt2
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
from matplotlib.pyplot import plot, show, xticks, yticks, title
from auxiliary import displayImages as DI, displayChannels as DC

#%% Wavelet transform coefficients operation wrapper
def wc_op(c, wn, lvl, Q, op = lambda x, Q: x, channel = 'Y'):
    # Applying a wavelet transform
    C = fwt2(c, wn, level = lvl)
    # Performing operation (quantization in JPEG 2000)
    # on 'de-tupled' wavelet coefficients 'C'
    C, S = c2a(C); C = list(map(op, C, repeat(Q)))
    # In the real JPEG 2000 the coefficients are here encoded,
    # bit layer after bit layer (for instance).

    # Displaying percentage of remaining coefficients
    CC = np.block(C).flat; CCC, CV = sum((CC)!= 0), len(CC)
    print(f'Non-zeros in {channel}: {CCC} of {CV} → {CV/CCC:.0f}x')

    # Re-tupling the wavelet coefficients
    C = a2c(C, S, output_format = 'wavedec2')
    # Inversing the wavelet transform
    return ifwt2(C, wn)

art = 'GrassHopper'    # pseud. Philip [gr. "friend of horses"]!... ;)
#art = 'BayerLCD'      # Color channel test pattern
#art = 'Pollock No. 5' # https://blogs.uoregon.edu/richardtaylor/2016/02/08/fractal-analysis-of-jackson-pollocks-poured-paintings/
#art = 'Malewicz I'    # a.k.a. 'Negroes Fighting in a Cellar at Night' by Allais 1897
#art = 'Malewicz II'   # or 'Bociany albinosy pośród śnieżnej zamieci' by OT.TO 1997
#art = 'Rothko'        # vel 'Orange, Red, Yellow' 1961

#%% JPEG 2000 main 'codec'
#  Hard thresholding:
#  from pywt import threshold as thrsd; qntz = lambda x, T: thrsd(x, T, mode = 'hard')
qntz = lambda x, Q: np.floor(x*2**Q + .5)/2**Q
wn, λ, L, Q = 'bior2.2', 0, 4, -6
# Interactive-aware wavelet transform parameters setting
# https://en.wikipedia.org/wiki/Cohen-Daubechies-Feauveau_wavelet#Numbering
# 'bior1.1', 'bior2.2', 'bior4.4' = 'Haar', 'LGT 5/3', 'CDF 9/7'
import sys;
if hasattr(sys, 'ps1'):
    wn, λ, L, Q = 'bior4.4', float(0x10), 5, -4
elif len(sys.argv) > 1:
    wn, λ, L, Q = eval(sys.argv[1])

img = openCV.cvtColor(openCV.imread(f'./images/{art}.png'), openCV.COLOR_BGR2RGB)
# Pick your own (floating) poison...  (for instance λ = 16.0).
# And then spice it up with e.g. λ = 0x10 ;D)
if λ > 0: img = np.clip(poisson(img * λ)/λ, 0x0, 0xff)

#%% A native RGB color space channels
DC([img.astype(int)],  ('red', 'green', 'blue'))
# Let me digress a bit: A histogram of the original image
redux = lambda x: x[0]
hR, hG, hB = [redux(np.histogram(img[..., c], bins = 0x100)) for c in range(0b11)]
xticks(np.arange(0, 0x101, 0x20)); yticks([])
plot(hR, 'r', hG, 'g', hB, 'b'); title(art); show()

#%% Wavelet multiresolution analysis (MRA) visualization (yet another digression)...
# See https://pywavelets.readthedocs.io/en/latest/
titles = [f'{wn} approximation (LL)', 'Horizontal details (HL)',
           'Vertical details (LH)',   'Diagonal details (HH)']
Y = img[..., 0] # ... presented here for the luminance ('Y', grayscale) channel only
LL, (HL, LH, HH) = dwt2(Y, wn)
DI([LL, HL, LH, HH], titles, grid = False)
Y = idwt2((LL, (HL, LH, HH)), wn)
DI(Y, 'DWT⁻¹(DWT(Y)) → ⌊…⌋ ?', grid = False)

#%% But I digress again: A YCoCg color space - a réversible color transform
#   cf. e.g. https://en.wikipedia.org/wiki/YCoCg
def rgb2ycocg(img):  # R  G  B
    YCoCg = np.array([[1, 2, 1], [2, 0, -2], [-1, 2, -1]])/4
    return img@YCoCg.T
ycocg = rgb2ycocg(img)
DI([ycocg[..., n] for n in range(3)], ['Y', 'Co', 'Cg'], grid = False)

#%% Back to the JPEG 2000(-ish)...
# An irréversible color transform (ICT)†
img = openCV.cvtColor(img.astype(np.uint8), openCV.COLOR_RGB2YCrCb)
# An original image in the YCbCr color space before...
DI([img[..., n] for n in (0, 2, 1)], ['Y', 'Cb', 'Cr'], grid = False)
# ... and after the wavelet transform and quantization
Y, Cb, Cr = [wc_op(img[..., n], wn, L, Q, qntz, ('Y', 'Cr', 'Cb')[n]) for n in (0, 2, 1)]
DI([Y, Cb, Cr], ['Y', 'Cb', 'Cr'], grid = False)
#%% Final housekeeping...
img = np.array(np.clip(np.dstack((Y, Cr, Cb)), 0, 0xff), np.uint8)
# ... the inverse ICT...
img = openCV.cvtColor(img, openCV.COLOR_YCrCb2RGB)
# ... and the ultimate presentation
DI(img, f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})', grid = False)

# ————————————————————————————————————————————————————————————————————————
#† That the J2K's RCT (réversible) algorithm ('⌊x⌋' stands for 'floor(x)'):
#    Y = ⌊(R + 2G + B)/4⌋,  Cr = R  - G, Cb = B  - G  :RCT
#    G = Y - ⌊(Cr + Cb)/4⌋,  R = Cr + G,  B = Cb + G  :RCT⁻¹
#  is indeed réversible, is remarkable and a bit stunning...
#  See: https://en.wikipedia.org/wiki/JPEG_2000#Color_components_transformation
#  and cf. https://en.wikipedia.org/wiki/YCoCg
## Proof: R,G,B are integers. Hence:
#   Y - ⌊(Cr + Cb)/4⌋ = Y - ⌊(R - G + B - G)/4⌋
#                    = Y - ⌊(R - G + B - G + (4G - 4G))/4⌋
#                    = Y - ⌊(R - G + B - G + 4G)/4⌋ + G
#                    = Y - ⌊(R + 2G + B)/4⌋ + G = Y - Y + G = G ■
# %%
