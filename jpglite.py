#%%
from turtle import width
import cv2 as openCV; import numpy as np
from auxiliary import displayImages as DI, JPG_QT_Y
from scipy.fftpack import dctn, idctn
from numpy.random import poisson

## JP[E]G Lite - a (pretty much) simplified version of the standard
#  still image transform coding compression algorithm

##  Forward & inverse DCT 2D transform shortcuts
dct2, idct2 = (lambda img, norm = 'ortho': dctn(img, norm = norm),
               lambda img, norm = 'ortho': idctn(img, norm = norm))

#%%  Quantization of the DCT 2D coefficients
def quantize(X, Q = 1):
    if X.shape[0] == 8:
        QT = np.array(JPG_QT_Y)/Q
        X /= QT; X = np.floor(X + .5); X *= QT; X = X.astype(int)
    else:
        X = np.floor(Q*X + .5)/Q
    return X

#%% Image loading....
org = openCV.cvtColor(openCV.imread('./images/GrassHopper.PNG'), openCV.COLOR_BGR2YCrCb)
N = 512; org = openCV.resize(org[..., 0], (N, N))
# ... and tiling (if 'B == 8' then, by default, the JP[E]G quantization scheme
#     is applied (note we assume for simplicity the fixed image size
#     [that happens to be a power of two])
B, Q, λ = 8, 1, 0

import sys;
if hasattr(sys, 'ps1'):
    B, Q, λ = 32, 0.1, 1.0
elif len(sys.argv) > 1:
    B, Q, λ = eval(sys.argv[1])

tiles, blocks = range(0, N, B), range(int(N/B))
# Pick your poison... (be sure to make λ floating... ;)
if λ > 0:
    org = np.clip(poisson(org * λ)/λ, 0x0, 0xff)

#%% Transforming (separately/in a parallel way (supposedly!)) each tile/block by DCT 2D
trns = [[dct2(org[n:n + B, m:m + B]) for n in tiles] for m in tiles]

#%% Quantization vs. image quality
r'''
If B ≠ 8, then the standard scalar quantization is applied and 'Q == 1'
  means no scalar quantization (other than conversion to the 'int' type).
  For B == 8 the JP[E]G quantization matrix is applied (for 'Y' channel).
  Then 'Q == 0.1' results (usually) in a poor quality image while
  'Q == 10' yields a (seemingly) indistinguishable image.
  When 'B != 8', then the scalar quantization, 'x = Q⁻¹⌊Q⋅x + .5⌋', is performed
'''
## Coefficients quantization and inverse transformation
qntz = [[quantize(trns[n][m], Q)    for n in blocks] for m in blocks]
img  = [[idct2(qntz[m][n])          for n in blocks] for m in blocks]

#%% Presentation
img, qntz = np.block(img), np.block(qntz)
nz  = sum((qntz != 0).flat)
DI([org, qntz, img, org - img],
    [f'original\n{N}×{N} = {N*N} pixels',
     f'DCT 2D\n{N/B:.0f}×{N/B:.0f} = {N**2/B**2:.0f} of {B}×{B} blocks',
     f'Reconstruction\nQ = {Q}',
     f'Difference\n{nz} ({nz/(N*N):,.1%}) non-zeros'], grid = False)

#%% Is this a new normal?
from matplotlib.pyplot import hist, show
from matplotlib.colors import Normalize, LinearSegmentedColormap as lscm
from auxiliary import YCbCr_ext_channels as YCbCr
N, bins, patches = hist((org - img).flat, bins = 0x100, density = True)

# See: https://matplotlib.org/stable/gallery/statistics/hist.html
fracs = N / N.max(); norm = Normalize(fracs.min(), fracs.max())

# The higher bar the lighter color
cm = lscm.from_list(YCbCr[0][0], YCbCr[0][1:-1], N = 0x100)
for thisfrac, thispatch in zip(fracs, patches):
    thispatch.set_facecolor(cm(norm(thisfrac)))

show()
# %%
