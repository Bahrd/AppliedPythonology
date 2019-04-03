import cv2; import numpy as np; import auxiliary as aux; 
import matplotlib.pyplot as plt

## JPG Lite - a (pretty much) simplified version of the standard 
#  still image transform coding compression algorithm

## Tile DCT 2D transform
def dct2(img, nrm = 'ortho'):
    from scipy.fftpack import dct
    return dct(dct(img.T, norm = nrm).T, norm = nrm) 

## Tile Inverse DCT 2D transform
def idct2(img, nrm = 'ortho'):
    from scipy.fftpack import idct
    return idct(idct(img.T, norm = nrm).T, norm = nrm) 

## Quantization of the DCT 2D coefficients 
#  When 'block_size = 8' the standard JPG quantization is applied with Q 
#  being a quality factor (the larger Q the better quality)
#  Otherwise the scalar quantization: '⌊Q⋅x + .5⌋/Q' is performed
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
B = 32;  blocks, tiles = range(int(N/B)), range(0, N, B)

# Compression quality ('Q = 1' no quantization or standard JPG quatization)
Q = 1

## Transforming each tile/block using DCT 2D
trns = [[dct2(img[n:n + B, m:m + B]) for m in tiles] 
                                     for n in tiles]
## Coefficients quantization
trns = [[quantize(trns[n][m], Q) for m in blocks] 
                                 for n in blocks]
## Inverse tile transformation of quantized coefficients
img  = [[idct2(trns[n][m]) for m in blocks] 
                           for n in blocks]
## Presentation
img = np.block(img).astype(np.int); trns = np.block(trns); diff = img - org
aux.displayImages([org, trns, img, org - img], 
                  ['original', 
                   'DCT 2D', 
                   'Q = {0}'.format(Q),
                   'Max diff {0}'.format(max(diff.flat))])