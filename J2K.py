#%% J2K (a.k.a. a skeleton of the JPEG 2000 algorithm: merely its color and wavelet transforms.
#   But... with a twist: the wavelet transform is applied to the YCoCg color space channels
import numpy as np
import sys
import matplotlib.pyplot as plt
from numpy.random import poisson
from itertools import repeat
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from auxiliary import (displayImages as di,displayAnyChannels as dac,
                       YCoCg_ext_channels as YCoCg,
                       RGB_ext_channels as RGB,
                       RGB2YCoCg, YCoCg2RGB)
from histogramXYZ import channelGradientHistogram as cgh
#   Tabbed windows
from imports.plotWindow import plotWindow as pw

#   Wavelet transform (for the win!) coefficients operation palindrome
def wtftw(c, wn, lvl, Q, op = lambda x, Q: x, channel = 'Y'):
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
art = 'Mustang GTD' # a.k.a. "Spirit [Stallion of the Cimarron]"!... Kiger?
tabs = pw(title = 'JPEG 2000[e]lite')

#   JPEG 2000 main 'codec'
qntz = lambda x, Q: np.floor(x*2**Q + .5)/2**Q
#   Interactive-aware wavelet transform parameters setting
#   https://en.wikipedia.org/wiki/Cohen-Daubechies-Feauveau_wavelet#Numbering
#   'bior1.1', 'bior2.2', 'bior4.4' = 'Haar', 'LGT 5/3', 'CDF 9/7'
wn, λ, L, Q = 'bior2.2', 0, 0b100, 0b11
if hasattr(sys, 'ps1'):
    wn, λ, L, Q = 'bior4.4', float(0o10), 0b101, 0b10
elif len(sys.argv) > 1:
#   Pick your own (floating) poison...  (for instance λ = 4.0).
#   And then spice it up with e.g. λ = 0x4 ;D)
    wn, λ, L, Q = eval(sys.argv[1])

img = plt.imread(f'./images/{art}.png')[..., :3]
di(img, f'{art} (original)', grid = False, show = False, tabbed = tabs)

if λ > 0: img = np.clip(poisson(img * 2**λ)/2**λ, 0x0, 0xff)
#   A native RGB color space channels
dac(img, RGB, tabbed = tabs); cgh(img, art, 'RGB', RGB, tabbed = tabs)
#   A réversible color transform (RCT)†
img = img@RGB2YCoCg.T
dac(img, YCoCg, tabbed = tabs); cgh(img, art, 'YCoCg (before)', YCoCg, tabbed = tabs)
#   ... the wavelet transform and quantization...
Y, Co, Cg = [wtftw(img[..., n], wn, L, Q, qntz, ('Y', 'Co', 'Cg')[n]) for n in range(3)]
# ... and after
img = np.array(np.dstack((Y, Co, Cg)))
dac(img, YCoCg, tabbed = tabs); cgh(img, art, 'YCoCg (after)', YCoCg, DC = False, tabbed = tabs)
#   Grand finale!
#   ... with the inverse réversible CT...
img = img@YCoCg2RGB.T
di(img, f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})', 
   grid = False, show = False, tabbed = tabs)

# Et voilà!
tabs.show()
'''
————————————————————————————————————————————————————————————————————————
† That the original J2K's RCT (Réversible Color Transform) algorithm
    Y = ⌊(R + 2G + B)/4⌋,  Cr = R  - G, Cb = B  - G  :RCT
    G = Y - ⌊(Cr + Cb)/4⌋,  R = Cr + G,  B = Cb + G  :RCT⁻¹
  where '⌊x⌋' stands for 'floor(x)', is also réversible, is equally remarkable 
  if not even more stunning...
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
'''

