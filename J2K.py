## Vanila JPEG 2000 algorithm 
# (the vanilin one, in fact: neither EBCOT nor BAC whatsoever)
import cv2; import numpy as np
from itertools import repeat
from matplotlib.pyplot import figure, show, imshow, title, gcf
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from pywt import dwt2, idwt2
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2, threshold as thrsd, 
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
from auxiliary import displayImages as DI

## Wavelet transform coefficients operation wrapper
def wc_op(c, wn, lvl, Q, op = lambda x, Q: x):
    # Applying a wavelet transform
    C = fwt2(c, wn, level = lvl)
    # Performing operation (quantization in JPEG 2000)
    # on 'de-tupled' wavelet coefficients 'C' 
    C, S = c2a(C); C = list(map(op, C, repeat(Q)))    
    ## In the real JPEG 2000 the coefficients are here encoded, 
    #  bit layers after bit layers (for instance).

    # Displaying percentage of remaining coefficients
    CC = np.block(C).flat; CCC, CV = sum((CC)!= 0), len(CC)
    print('Non-zeros: {} of {} = {:,.2f}%'.format(CCC, CV, 100 * CCC/CV))
    
    # Re-tupling the wavelet coefficients
    C = a2c(C, S, output_format = 'wavedec2')
    # Inversing the wavelet transform
    return ifwt2(C, wn)

art = 'GrassHopper'   # pseud. 'Filip'... ;)
#art = 'Pollock No. 5' # https://blogs.uoregon.edu/richardtaylor/2016/02/08/fractal-analysis-of-jackson-pollocks-poured-paintings/
#art = 'Malewicz I'    # a.k.a. 'Negroes Fighting in a Cellar at Night' by Allais 1897
#art = 'Malewicz II'   # or 'Bociany albinosy w środku śnieżnej zamieci' by OT.TO 1997
#art = 'Rothko'        # vel 'Orange, Red, Yellow' 1961

## JPEG 2000 main 'codec' 
# Wavelet transforms' (hiper-)parameters
# https://en.wikipedia.org/wiki/Cohen-Daubechies-Feauveau_wavelet#Numbering
# 'bior1.1', 'bior2.2', 'bior4.4' = 'Haar', 'LGT 5/3', 'CDF 9/7' 
#  Hard thresholding:             'lambda x, T: thrsd(x, T, mode = 'hard')' 
L, wn, Q, qntz = 6, 'bior1.1', -6, lambda x, Q: np.floor(x*2**Q + .5)/2**Q

# Irréversible color transform (ICT)*
img = cv2.cvtColor(cv2.imread(f'./{art}.png'), cv2.COLOR_BGR2YCrCb)
#img = cv2.cvtColor(cv2.imread('./{}.png'.format(art)), cv2.COLOR_BGR2RGB)

###
## YCbCr color space (a digression)
DI([img[..., n] for n in range(3)], ['Y', 'Cb', 'Cr'])
#DI([img[..., n] for n in range(3)], ['R', 'G', 'B'])
## Wavelet multiresolution analysis (MRA) visualization (yet another digression)
#  See https://pywavelets.readthedocs.io/en/latest/
titles = [f'{wn} approximation (LL)', 'Horizontal details (HL)', 
          'Vertical details (LH)',    'Diagonal details (HH)']
Y = img[..., 0] # A luminance (grayscale) channel only
LL, (HL, LH, HH) = dwt2(Y, wn);    DI([LL, HL, LH, HH], titles)
Y = idwt2((LL, (HL, LH, HH)), wn); DI(Y, 'DWT⁻¹(DWT(Y)) → ⌊…⌋ ?')
###

## Back to the JPEG 2000(-ish)...
Y, Cb, Cr = [wc_op(img[..., n], wn, L, Q, qntz) for n in range(3)]
DI([Y, Cb, Cr], ['Y', 'Cb', 'Cr'])
# Housekeeping... 
img = np.array(np.clip(np.dstack((Y, Cb, Cr)), 0, 0xff), np.uint8)
# ... the inverse ICT...
img = cv2.cvtColor(img, cv2.COLOR_YCrCb2RGB)
# ... and the final presentation
DI(img, f'{art} {wn}\'ed@level {L} (step size = {2**(-Q)})')
##* That the J2K's RCT (réversible) algorithm ('⌊x⌋' stands for 'floor(x)'):
#   RCT:   Y = (R + 2G + B)/4⌋,  Cr = R  - G, Cb = B  - G
#   RCT⁻¹: G = Y - ⌊(Cr + Cb)/4⌋, R = Cr + G,  B = Cb + G
#   is indeed réversible, is remarkable and a bit stunning...
### Proof: R,G,B are integers. Hence:
#   Y - ⌊(Cr + Cb)/4⌋ = Y - ⌊(R - G + B - G)/4⌋
#                     = Y - ⌊(R - G + B - G + (4G - 4G))/4⌋
#                     = Y - ⌊(R - G + B - G + 4G)/4⌋ + G
#                     = Y - ⌊(R + 2G + B)/4⌋ + G = Y - Y + G = G ■