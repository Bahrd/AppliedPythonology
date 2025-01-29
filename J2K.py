### J2K (a.k.a. a skeleton of the JPEG 2000 algorithm: merely its color and wavelet transforms.
#   But... with a twist: the wavelet transform is applied to the YCoCg color space channels
import numpy as np, sys, matplotlib.pyplot as plt
from numpy.random import poisson, choice
from itertools import repeat
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2,
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from auxiliary import (displayImages as di,displayAllChannels as dac,
                       RGB_ext_channels as RGB,
                       YCoCg_ext_channels as YCoCg,
                       RGB2YCoCg, YCoCg2RGB)
#   No gradient, no gain! ;)
from histogramXYZ import channelGradientHistogram as cgh
#   No tabs, no pain! ;)
from imports.plotWindow import plotWindow as mtw

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

#   JPEG 2000 main 'codec'
qntz = lambda x, Q: np.floor(x*2**Q + .5)/2**Q
#   Wavelet transform parameters setting ('bior1.1', 'bior2.2', 'bior4.4' = 'Haar', 'LGT 5/3', 'CDF 9/7')
#   https://en.wikipedia.org/wiki/Cohen-Daubechies-Feauveau_wavelet#Numbering
#   Ɑ: Hold your horse! "Spirit [Stallion of the Cimarron]" :D
art, wn, λ, L, Q = choice(['mammals/Mustang GTD', 'mammals/Mustang RTR']), 'bior2.2', 0, 0b110, -0b110
if len(sys.argv) > 1:
#   Pick your own λ-poison...
    art, wn, λ, L, Q = eval(sys.argv[1]) # "'Haar', 0o10, 0b101, -0b101"

tabs = mtw(title = f'{art}@J2K[e]lite')
# Handmade shortcuts for tabbed figures 
# ♪♫ Lumpy bumpity bee! ♫♪
tbdac, tbcgh, tbdi = (lambda ch, tabs = tabs: dac(img, ch, tabs = tabs), 
                      lambda art, ch, chn, DC = True, tabs = tabs: cgh(img, art, ch, chn, DC = DC, tabs = tabs),
                      lambda art, title: di(img, art, grid = False, title = title, tabs = tabs))
# ♪♫ Lumpy dumpity dee! ♫♪

img = np.array(plt.imread(f'./images/{art}.png')[..., :3] * 0xff)
if λ != 0: img = poisson(img * 2**λ)/2**λ

#   Here we go!
tbdi(f'{art}', title = 'Pretty original...')

#   A native RGB color space channels
tbdac(RGB)
tbcgh(art, 'RGB', RGB)

#   A réversible color transform (RCT)†
img = img@RGB2YCoCg.T
tbdac(YCoCg)
tbcgh(art, 'YCoCg (before)', YCoCg)

#   ... the wavelet transform and quantization...
Y, Co, Cg = [wtftw(img[..., n], wn, L, Q, qntz, ('Y', 'Co', 'Cg')[n]) for n in range(3)]

# ... and after
img = np.array(np.dstack((Y, Co, Cg)))
tbdac(YCoCg)
tbcgh(art, 'YCoCg (after)', YCoCg)

#   ♪♫ Final countdown! ♫♪ https://youtu.be/9jK-NcRmVcw
#   ... with the inverse réversible CT...
img = img@YCoCg2RGB.T
tbdi(f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})', title = '... and pretty compressed')
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