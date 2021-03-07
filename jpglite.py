import cv2; import numpy as np; import auxiliary as aux
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct

#%% JPG Lite - a (pretty much) simplified version of the standard 
#   still image transform coding compression algorithm

##  Useful routines
#   Tile DCT 2D transform
def dct2(img, nrm = 'ortho'):
    return dct(dct(img.T, norm = nrm).T, norm = nrm) 
#   Tile Inverse DCT 2D transform
def idct2(img, nrm = 'ortho'):
    return idct(idct(img.T, norm = nrm).T, norm = nrm) 

##  Quantization of the DCT 2D coefficients 
#   When 'block_size == 8', then the standard JPG luminance channel (Y)
#   quantization matrix is applied with a 'quality factor' Q.
#   Otherwise the scalar quantization, 'x = Q⁻¹⌊Q⋅x + .5⌋', is performed
def quantize(X, Q = 1):
    if X.shape[0] == 8:
        QT = np.array(aux.JPG_QT_Y)/Q
        X /= QT; X = np.floor(X + .5); X *= QT; X = X.astype(int)
    else:
        X = np.floor(Q*X + .5)/Q
    return X

## Image loading (if 'B == 8' then by default a JPG quantization scheme is 
#   applied (note we assume for simplicity the fixed image size [being a power of two])
org = cv2.cvtColor(cv2.imread('GrassHopper.PNG'), cv2.COLOR_BGR2YCrCb)
N = 1024; org = cv2.resize(org[..., 0], (N, N))
B = 32;  tiles, blocks = range(0, N, B), range(int(N/B))

## Transforming each tile/block using DCT 2D
trns = [[dct2(org[n:n + B, m:m + B]) for m in tiles] for n in tiles]

## Compression vs. image quality 
#  If B ≠ 8, then the standard scalar quantization is applied and 'Q == 1'
#  means no scalar quantization (other than conversion to the 'int' type). 
#  For B == 8 the JPG quatization matrix is applied. Then 'Q == 0.1' results 
#  usually in a poor quality image while 'Q == 10' yields a visually indistinguishable image.
Q = 1/64 
## Coefficients quantization and inverse transformation
qntz = [[quantize(trns[n][m], Q)          for n in blocks] for m in blocks]
img  = [[idct2(qntz[n][m]).astype(np.int) for n in blocks] for m in blocks]
#  Note that the 'trns' argument is not deep-copied when passed to 
#  'quantize' function and thus is modified there!

## Presentation
img, qntz = np.block(img), np.block(qntz)
nz  = sum((qntz != 0).flat)
aux.displayImages([org, qntz, img, org - img], 
                  ['original', 'DCT 2D', f'Q = {Q}', f'{nz} non-zeros'])