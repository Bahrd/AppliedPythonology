#%%
import cv2 as openCV; import numpy as np; import auxiliary as aux
from scipy.fftpack import dctn, idctn

## JP[E]G Lite - a (pretty much) simplified version of the standard
#  still image transform coding compression algorithm

##  Forward & inverse DCT2 transform shortcuts
dct2, idct2 = lambda img, norm = 'ortho': dctn(img, norm = norm), lambda img, norm = 'ortho': idctn(img, norm = norm)

#%%  Quantization of the DCT 2D coefficients
#   When 'block_size == 8', then the standard JP[E]G luminance channel (Y)
#   quantization matrix is applied with a 'quality factor' Q.
#   Otherwise the scalar quantization, 'x = Q⁻¹⌊Q⋅x + .5⌋', is performed
def quantize(X, Q = 1):
    if X.shape[0] == 8:
        QT = np.array(aux.JPG_QT_Y)/Q
        X /= QT; X = np.floor(X + .5); X *= QT; X = X.astype(int)
    else:
        X = np.floor(Q*X + .5)/Q
    return X

#%% Image loading (if 'B == 8' then by default a JP[E]G quantization scheme
#   is applied (note we assume for simplicity the fixed image size
#   [that happens to be a power of two])
org = openCV.cvtColor(openCV.imread('./images/GrassHopper.PNG'), openCV.COLOR_BGR2YCrCb)
N = 512; org = openCV.resize(org[..., 0], (N, N))
B = 8;  tiles, blocks = range(0, N, B), range(int(N/B))

#%% Transforming each tile/block using DCT 2D
trns = [[dct2(org[n:n + B, m:m + B]) for n in tiles] for m in tiles]

#%% Quantization vs. image quality
#  If B ≠ 8, then the standard scalar quantization is applied and 'Q == 1'
#  means no scalar quantization (other than conversion to the 'int' type).
#  For B == 8 the JP[E]G quantization matrix is applied.
#  Then 'Q == 0.1' results (usually) in a poor quality image while
#  'Q == 10' yields a visually indistinguishable image.
Q = 0.1
## Coefficients quantization and inverse transformation
qntz = [[quantize(trns[n][m], Q)    for n in blocks] for m in blocks]
img  = [[idct2(qntz[m][n])          for n in blocks] for m in blocks]

#%% Presentation
img, qntz = np.block(img), np.block(qntz)
nz  = sum((qntz != 0).flat)
aux.displayImages([org, qntz, img, org - img],
                  [f'original\n{N}×{N} = {N*N} pixels',
                   f'DCT 2D\n{N/B:.0f}×{N/B:.0f} = {N**2/B**2:.0f} of {B}×{B} blocks',
                   f'Reconstruction\nQ = {Q}',
                   f'Difference\n{nz} ({nz/(N*N):,.1%}) non-zeros'],
                  grid = False)

#%% Is this normal?
from matplotlib.pyplot import hist, show
hist((org - img).flat, density = True); show()

# %%
