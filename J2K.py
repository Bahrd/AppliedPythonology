## Vanila JPEG 2000 algorithm 
# (the vanilin one, in fact: neither EBCOT nor BAC whatsoever)
import cv2; import numpy as np
from itertools import repeat
from matplotlib.pyplot import figure, show, imshow, title, gcf
# https://pywavelets.readthedocs.io/en/latest/ref/dwt-coefficient-handling.html
from pywt import (wavedec2 as fwt2, waverec2 as ifwt2, threshold as thrsd, 
                  array_to_coeffs as a2c, coeffs_to_array as c2a)
## Figure's stickers remover
def dersticker(): gcf().gca().set_xticks([]); gcf().gca().set_yticks([])

## Wavelet transform coefficients operation (here quantization)
#  thresholding: 'lambda x, T: thrsd(x, T, mode = 'hard')' 
def wc_op(c, wn, lvl, Q, op = lambda x, Q: x):
    # Applying a wavelet transform
    C = fwt2(c, wn, level = lvl)
    # Performing operation on 'de-tupled' wavelet coefficients 'C' 
    C, S = c2a(C); C = list(map(op, C, repeat(Q)))    
    ## In the real JPEG 2000 the coefficients are here encoded, 
    #  bit layers after bit layers (for instance).

    # Displaying percentage of remaining coefficients
    CC = np.block(C).flat; print('Non-zeros: {:,.2f}%'.format(100 * sum((CC)!= 0)/len(CC)))
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
# Irréversible color transform (ICT)*
img = cv2.cvtColor(cv2.imread('./{}.png'.format(art)), cv2.COLOR_BGR2YCrCb)
# Wavelet transforms' (hiper-)parameters
# 'bior1.1' == Haar wavelets, 'bior2.2' == LeGal 5/3, 'bior4.4' == CDF 9/7 
L, wn, Q, qntz = 8, 'bior1.1', -6, lambda x, Q: np.floor(x*2**Q + .5)/2**Q

### #######################################################################
## Wavelet multiresolution analysis (MRA) visualization (a digression)
#  See https://pywavelets.readthedocs.io/en/latest/
from pywt import dwt2, idwt2
Y = img[..., 0] # A luminance (grayscale) channel only
LL, (HL, HL, HH) = dwt2(Y, wn)

fig = figure(figsize = (6, 6)); fig.tight_layout()
titles = ['{} approximation'.format(wn),    
          'Horizontal details', 'Vertical details', 'Diagonal details']

for i, (a, t) in enumerate(zip([LL, HL, HL, HH], titles)):
    ax = fig.add_subplot(2, 2, i + 1)
    ax.set_title(t); ax.set_xticks([]); ax.set_yticks([])
    ax.imshow(a, cmap = 'gray')    
show()
Y = idwt2((LL, (HL, HL, HH)), wn); dersticker(); imshow(Y, cmap = 'gray'); show()
### #######################################################################

## Back to the JPEG 2000...
Y, Cb, Cr = [wc_op(img[..., n], wn, L, Q, qntz) for n in range(3)]
# Housekeeping... 
img = np.array(np.clip(np.dstack((Y, Cb, Cr)), 0, 255), np.uint8)
# ... and the inverse ICT
img = cv2.cvtColor(img, cv2.COLOR_YCrCb2RGB)

# Presentation
dersticker(); title('{} {}\'ed@level {} (step size = {})'.format(art, wn, L, 2**(-Q)))
imshow(img); show() 

##* That the J2K's RCT (réversible) algorithm ('⌊x⌋' stands for 'floor(x)'):
#   RCT:   Y = (R + 2G + B)/4⌋,  Cr = R  - G, Cb = B  - G
#   RCT⁻¹: G = Y - ⌊(Cr + Cb)/4⌋, R = Cr + G,  B = Cb + G
#   is indeed réversible, is remarkable and a bit stunning...
### Proof:
#   Y - ⌊(Cr + Cb)/4⌋ = Y - ⌊(R - G + B - G)/4⌋
#                     = Y - ⌊(R - G + B - G + (4G - 4G))/4⌋
#                     = Y - ⌊(R - G + B - G + 4G)/4⌋ + G
#                     = Y - ⌊(R + 2G + B)/4⌋ + G = Y - Y + G = G ■