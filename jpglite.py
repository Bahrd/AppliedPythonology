import cv2; import numpy as np; import auxiliary as aux; 
import matplotlib.pyplot as plt

### JPG Lite - a (pretty much) simplified version of the standard 
#   still image transform coding compression algorithm

## Useful routines
# Tile DCT 2D transform
def dct2(img, nrm = 'ortho'):
    from scipy.fftpack import dct
    return dct(dct(img.T, norm = nrm).T, norm = nrm) 
# Tile Inverse DCT 2D transform
def idct2(img, nrm = 'ortho'):
    from scipy.fftpack import idct
    return idct(idct(img.T, norm = nrm).T, norm = nrm) 
# Quantization of the DCT 2D coefficients 
#  When 'block_size == 8' the standard JPG luminance channel quantization 
#  matrix is applied with Q being a 'quality factor' (the larger Q 
#  the better quality). 
#  Otherwise, the scalar quantization: '⌊Q⋅x + .5⌋/Q' is performed
def quantize(img, Q = 1):
    if img.shape[0] == 8:
        QT = np.array(aux.JPG_QT_Y)
        img = (img / (QT / Q)).astype(np.int)
        img = (img * (QT / Q)).astype(np.int)
    else:
        img = (img * Q).astype(np.int)
        img = (img / Q).astype(np.int)
    return img

## Image loading
img = cv2.cvtColor(cv2.imread("GrassHopper.PNG"), cv2.COLOR_BGR2GRAY); org = img
N = 512; img, org = cv2.resize(img, (N, N)), cv2.resize(org, (N, N))
B = 16;  tiles, blocks = range(0, N, B), range(int(N/B))

# Compression quality ('Q == 1' means no scalar quantization (other 
# than 'int' conversion) or a standard JPG quatization matrix application)
# For instance, 'Q == 0.1' usually results in a poor quality image while
# For a JPG, 'Q == 10' yields a visually indistinguishable image

## Transforming each tile/block using DCT 2D
trns = [[dct2(org[n:n + B, m:m + B]) for m in tiles] for n in tiles]

## Coefficients quantization and inverse transformation
qntz = [[quantize(trns[n][m]) for n in blocks] for m in blocks]
img  = [[   idct2(qntz[n][m]) for n in blocks] for m in blocks]

## Presentation
img, qntz = np.block(img).astype(np.int), np.block(qntz)
nonzeros = sum((qntz != 0).flat)

aux.displayImages([org, qntz, img, org - img], 
                  ['original', 'DCT 2D', 
                   'Q = {}'.format(Q), '{} non-zeros'.format(nonzeros)])