''' Wavelet multiresolution analysis (MRA) visualization
    See https://pywavelets.readthedocs.io/en/latest/
    Illustrated here for the luminance ('Y', grayscale) channel
    from the YCoCg space and (be default) with the help of the "grandpas" of all wavelets:
    the "International sensation!", the Haar family! [ https://youtu.be/uMTPXen99n0 ]
    Some say: "You can choose your friends, but you can't choose your family!"
    Oh, really?! :D
'''
import matplotlib.pyplot as plt, sys

from auxiliary import displayImages as di, RGB2YCoCg as RGB2YCxCy # RGB2YCbCr
from imports.plotWindow import plotWindow as mtw
from numpy import array, concatenate as cnc
from numpy.random import poisson
from pywt import dwt2, idwt2

##  A test image (isotoxal, from Greek τόξον - 'arc') https://en.wikipedia.org/wiki/Isotoxal_figure
##  'λ' is - as always - a λevǝλ of poison (a.k.a an intensity in Poisson distribution)
art, wn, λ = eval(sys.argv[1]) if len(sys.argv) > 1 else ('Isotoxal octagons', 'bior1.1', 0) # 'Haar" will do too!

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

'''  MRA quartet decomposition|analysis (a forward wavelet transform): 
    + one approximation (LL), and 
    + three details/differences quarters (HL, LH, HH). 
    You can call it a "wavelet microscope" '''
LL, (HL, LH, HH) = dwt2(Y, wn)
''' ...
    Note that we do nothing like 
    + thresholding or
    + quantizing 
    the wavelet coefficients...
    ...
    Reconstruction|synthesis from MRA (an inverse wavelet transform)'''
Y = idwt2((LL, (HL, LH, HH)), wn)

##  MRA demonstration
A = 0x10; LL, (HL, LH, HH) = LL/2, (HL*A, LH*A, HH*A)
di([LL, HL, LH, HH], titles, title = 'Haar MRA decomposition', grid = False, tabs = tabs)
##  They ♪♫ask no quarters♫♪ https://youtu.be/_vG_mTt6hCs, so let's "integrate" 
#   (there is no single way to skin the cat - or is it?) them back to help'em shine in all their glory
MRA = cnc([cnc([LL, HL], axis = 1), 
           cnc([LH, HH], axis = 1)], axis = 0)
#   It looks like eventually "nothing [zero, zip, zilch, nada] happened here, move along people"!
di([Y, MRA, Y - img[..., 0]], ['DWT⁻¹(DWT(Y)) → ⌊…⌋ ?', 'MRA', 'Zero, zip, zilch, nada?'],
   title = 'The MRA, or There and Back Again...', grid = False, tabs = tabs)

# "That's all, folks!"
tabs.show()