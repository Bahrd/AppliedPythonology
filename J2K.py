#%% Vanilla JPEG 2000 algorithm (more like a vanillin one, in fact:
#   neither EBCOT nor BAC is implemented whatsoever)
import cv2 as openCV; import numpy as np
import sys
from numpy.random import poisson
from itertools import repeat
from pywt import dwt2, idwt2
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from auxiliary import (displayImages as di,displayAnyChannels as dac,
                       YCbCr_ext_channels as YCbCr,
                       YCoCg_ext_channels as YCoCg,
                       RGB_ext_channels as RGB,
                       RGB2YCbCr, YCbCr2RGB, RGB2YCoCg)
from histogramXYZ import channelGradientHistogram as cgh

#   Wavelet transform coefficients operation palindrome
def wtotw(c, wn, lvl, Q, op = lambda x, Q: x, channel = 'Y'):
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
art = 'GrassHopper' # pseud. Philip [gr. "friend of horses"]!... ;)

#%% JPEG 2000 main 'codec'
qntz = lambda x, Q: np.floor(x*2**Q + .5)/2**Q
#   Interactive-aware wavelet transform parameters setting
#   https://en.wikipedia.org/wiki/Cohen-Daubechies-Feauveau_wavelet#Numbering
#   'bior1.1', 'bior2.2', 'bior4.4' = 'Haar', 'LGT 5/3', 'CDF 9/7'
wn, λ, L, Q = 'bior2.2', 0, 0b100, -0b111
if hasattr(sys, 'ps1'):
    wn, λ, L, Q = 'bior4.4', float(0o10), 0b101, -0b101
elif len(sys.argv) > 1:
    wn, λ, L, Q = eval(sys.argv[1])
#   Pick your own (floating) poison...  (for instance λ = 4.0).
#   And then spice it up with e.g. λ = 0x4 ;D)
img = openCV.cvtColor(openCV.imread(f'./images/{art}.png'), openCV.COLOR_BGR2RGB)
if λ > 0: img = np.clip(poisson(img * 2**λ)/2**λ, 0x0, 0xff)
#   A native RGB color space channels
dac(img, RGB); cgh(img, art, 'RGB', RGB)

#%% An irréversible color transform (ICT)†
#   An original image in the YCbCr color space before...
img = img@RGB2YCbCr
dac(img, YCbCr); cgh(img, art, 'YCbCr (before)', YCbCr)
#%% ... the wavelet transform and quantization...
Y, Cb, Cr = [wtotw(img[..., n], wn, L, Q, qntz, ('Y', 'Cr', 'Cb')[n]) for n in (0, 2, 1)]
img = np.array(np.clip(np.dstack((Y, Cr, Cb)), 0, 0xff))
# ... and after
dac(img, YCbCr); cgh(img, art, 'YCbCr (after)', YCbCr, DC = False)

#%% Grand finale!
#   ... with the inverse ICT...
img = np.clip(img@YCbCr2RGB, 0, 0xff).astype(np.uint8)
di(img, f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})', grid = False)

#%% Digressions within digressions...
#   A YCoCg color space - a réversible color transform
#   cf. e.g. https://en.wikipedia.org/wiki/YCoCg
img = openCV.cvtColor(openCV.imread(f'./images/{art}.png'), openCV.COLOR_BGR2RGB)
if λ > 0: img = np.clip(poisson(img * 2**λ)/2**λ, 0x0, 0xff)
ycocg = img@RGB2YCoCg
dac(ycocg,  YCoCg); cgh(ycocg, art, 'YCoCg', YCoCg)

#%% Wavelet multiresolution analysis (MRA) visualization
#   See https://pywavelets.readthedocs.io/en/latest/
#   Illustrated here for the luminance ('Y', grayscale) channel
#   from the YCoCg space and the "grandpas" of all wavelets: the Haar family!
A, wn = lambda x, a = 0x40, l = -0xff, h = 0xff: np.clip(a*x, l, h), 'Haar'
titles = [f'{wn} approximation (LL)', 'Horizontal details (HL)',
           'Vertical details (LH)',   'Diagonal details (HH)']
Y = ycocg[..., 0]
LL, (HL, LH, HH) = dwt2(Y, wn)
#   Note that the details are (slightly) exaggerated...
di([LL, A(HL), A(LH), A(HH)], titles, grid = False)
Y = idwt2((LL, (HL, LH, HH)), wn)
di(Y, 'DWT⁻¹(DWT(Y)) → ⌊…⌋ ?', grid = False)
# %%
'''
————————————————————————————————————————————————————————————————————————
† That the J2K's RCT (réversible) algorithm ('⌊x⌋' stands for 'floor(x)'):
    Y = ⌊(R + 2G + B)/4⌋,  Cr = R  - G, Cb = B  - G  :RCT
    G = Y - ⌊(Cr + Cb)/4⌋,  R = Cr + G,  B = Cb + G  :RCT⁻¹
  is indeed réversible, is remarkable if not simply stunning...
  See: https://en.wikipedia.org/wiki/JPEG_2000#Color_components_transformation
  and cf. https://en.wikipedia.org/wiki/YCoCg
  Proof: [♪♫ inch by inch, step by step, mile by mile...♫♪ https://youtu.be/uMTPXen99n0?t=126]:
  R,G,B are integers, and hence:
    G = Y - ⌊(Cr + Cb)/4⌋
      = Y - ⌊(R - G + B - G)/4⌋
      = Y - ⌊(R - G + B - G + (4G - 4G))/4⌋
      = Y - ⌊(R - G + B - G + 4G)/4⌋ + G
      = Y - ⌊(R + 2G + B)/4⌋ + G = Y - Y + G
      = G ■
————————————————————————————————————————————————————————————————————————
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