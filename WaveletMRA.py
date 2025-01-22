### Wavelet multiresolution analysis (MRA) visualization
#   See https://pywavelets.readthedocs.io/en/latest/
#   Illustrated here for the luminance ('Y', grayscale) channel
#   from the YCoCg space and (be default) with the help of the "grandpas" of all wavelets:
#   the "International sensation!" Haar family! [ https://youtu.be/uMTPXen99n0 ]
#   Some say: "You can choose your friends, but you can't choose your family!"
#   Oh, really?! :D

import matplotlib.pyplot as plt; import sys
from numpy import array, concatenate as cnc, clip

from auxiliary import displayImages as di, RGB2YCoCg as RGB2YCxCy # RGB2YCbCr
from imports.plotWindow import plotWindow as mtw
from numpy.random import poisson
from pywt import dwt2, idwt2

##  The "GrassHopper" is a "friend of horses" (Philip) and a "spirit" (Mustang)...
art = 'GrassHopper'
img = array(plt.imread(f'./images/{art}.png')[..., :3] * 0xff)

#   'A' stands for signal amplification (used for presentation purposes only: to help'em shine!)
A = lambda x, a = 0x10, l = -0xff, h = 0xff: clip(a*x, l, h)
##  'λ' is - as always - a λevǝλ of poison (a.k.a an intensity in Poisson distribution)
wn, λ = eval(sys.argv[1]) if len(sys.argv) > 1 else ('bior1.1', 0) # 'Haar" will do too!

# Ready, set, go!
tabs, titles  = mtw(), [f'{wn} approximation (LL)', 'Horizontal details (HL)',
                         'Vertical details (LH)',   'Diagonal details (HH)']
# Open it...
img = array(plt.imread(f'./images/{art}.png')[..., :3] * 0xff)
# ... add some poison...
if λ != 0: img = poisson(img * 2**λ)/2**λ
# ... do the color transform...
img = img@RGB2YCxCy.T
# ... and pick the luminance channel only
Y = img[..., 0]

##  MRA quartet decomposition (a forward wavelet transform - analysis): one approximation (LL) 
#   and three details/differences quarters (HL, LH, HH). You can call it a "wavelet microscope".
LL, (HL, LH, HH) = dwt2(Y, wn)
di([A(LL, .5), A(HL), A(LH), A(HH)], titles, title = 'Haar MRA decomposition', grid = False, tabs = tabs)

##  They ♪♫ask no quarters♫♪ https://youtu.be/_vG_mTt6hCs,
#   so let's "integrate" (there is no single way to skin the cat - or is it?) them back
#   to help'em shine in all their glory
MRA = cnc([cnc([A(LL, .5), A(HL)], axis = 1),
           cnc([A(LH),     A(HH)], axis = 1)], axis = 0)
#   Reconstruction from MRA (an inverse wavelet transform - synthesis)
Y = idwt2((LL, (HL, LH, HH)), wn)
#   It looks like eventually "nothing [zero, zip, zilch, nada] happened here, move along people"!
di([Y, MRA, Y - img[..., 0]], ['DWT⁻¹(DWT(Y)) → ⌊…⌋ ?', 'MRA', 'Zero, zip, zilch, nada?'],
    title = 'The MRA, or There and Back Again...', grid = False, tabs = tabs)

# "That's all, folks!"
tabs.show()