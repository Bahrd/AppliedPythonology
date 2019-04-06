import cv2; import numpy as np; import auxiliary as aux; 
import matplotlib.pyplot as plt

### JPG Lite - a (pretty much) simplified version of the standard 
#   still image transform coding compression algorithm

## Useful routines
#  Tile DCT 2D transform
def dct2(img, nrm = 'ortho'):
    from scipy.fftpack import dct
    return dct(dct(img.T, norm = nrm).T, norm = nrm) 
#  Tile Inverse DCT 2D transform
def idct2(img, nrm = 'ortho'):
    from scipy.fftpack import idct
    return idct(idct(img.T, norm = nrm).T, norm = nrm) 

## Quantization of the DCT 2D coefficients 
#  When 'block_size == 8' the standard JPG luminance channel quantization 
#  matrix is applied with Q being a 'quality factor' (the larger Q 
#  the better quality). 
#  Otherwise the scalar quantization, 'x = Q⁻¹⌊Q⋅x + .5⌋', is performed
def quantize(X, Q = 1):
    if X.shape[0] == 8:
        QT = np.array(aux.JPG_QT_Y)/Q
        X /= QT; img = np.floor(X + .5); X *= QT
    else:
        X = np.floor(Q*X + .5)/Q
    return X

## Image loading (if 'B == 8' then by default a JPG quantization scheme is 
#  applied
img = cv2.cvtColor(cv2.imread("GrassHopper.PNG"), cv2.COLOR_BGR2GRAY); org = img
N = 512; img, org = cv2.resize(img, (N, N)), cv2.resize(org, (N, N))
B = 16;  tiles, blocks = range(0, N, B), range(int(N/B))

## Transforming each tile/block using DCT 2D
trns = [[dct2(org[n:n + B, m:m + B]) for m in tiles] for n in tiles]

## Compression quality ('Q == 1' means no scalar quantization (other 
#  than 'int' conversion) or a standard JPG quatization matrix application)
#  For instance, 'Q == 0.1' usually results in a poor quality image while
#  For a JPG, 'Q == 10' yields a visually indistinguishable image
Q = 1/4
## Coefficients quantization and inverse transformation
qntz = [[quantize(trns[n][m], Q = Q) for n in blocks] for m in blocks]
img  = [[   idct2(qntz[n][m])        for n in blocks] for m in blocks]

## Presentation
img, qntz = np.block(img).astype(np.int), np.block(qntz)
nonzeros = sum((qntz != 0).flat)
aux.displayImages([org, qntz, img, org - img], 
                  ['original', 'DCT 2D', 'Q = {}'.format(Q),
                                         '{} non-zeros'.format(nonzeros)])