#%%
import cv2 as openCV, numpy as np, sys
from auxiliary import displayImages as di, JPG_QT_Y
from skimage.util import view_as_blocks as vab
from scipy.fftpack import dctn, idctn
from numpy.random import poisson

## JP[E]G Lite - a (pretty much) simplified version of the standard
#  still image transform coding compression algorithm

#%%  Quantization of the DCT 2D coefficients
def quantize(X, Q = 1):
    if X.shape[0] == 8:
        QT = np.array(JPG_QT_Y)/Q
        X /= QT; X = np.floor(X + .5); X *= QT
    else:
        X = np.floor(Q*X + .5)/Q
    return X

art, B, Q, λ = 'insects/GrassHopper', 8, 1, 0
##  Forward & inverse DCT 2D transform shortcuts
dct2, idct2 = (lambda img, norm = 'ortho': dctn(img, norm = norm),
               lambda img, norm = 'ortho': idctn(img, norm = norm))

if hasattr(sys, 'ps1'):
    art, B, Q, λ = 'insects/Wassup, wasp!', 32, 0.1, 1.0
elif len(sys.argv) > 1:
    art, B, Q, λ = eval(sys.argv[1])

#%% ♪♫ It's loading, re-loading! ♫♪
org = openCV.cvtColor(openCV.imread(f'./images/{art}.PNG'), openCV.COLOR_BGR2YCrCb)
N = 0x1 << 10; org = openCV.resize(org[..., 0], (N, N))


# Pick your (floating) poison...
if λ > 0:
    p = poisson(org * λ)/λ
    org = np.clip(p, 0x0, 0xff)

#%% Tilin'quantization vs. image quality
r'''
  If e size of the block, B ≠ 8, then the standard scalar quantization is applied 
  and then 'Q == 1' means no scalar quantization (other than conversion to the 'int' type)
  is performed.
  
  For B == 8 the JP[E]G quantization matrix is applied (for 'Y' channel).
  Then 'Q == 0.1' results (usually) in a poor quality image while
  'Q == 10' yields a (seemingly) indistinguishable image.
  When 'B != 8', then the scalar quantization, 'x = Q⁻¹⌊Q⋅x + .5⌋', is performed
'''
blck, bn  = vab(org, (B, B)), range(int(N/B))
#  Transformation, quantization and...
qntz = [[quantize(dct2(blck[n, m]), Q) for m in bn] for n in bn]
#  ... the inverse transformation (via implicit block views...)
img  = [[idct2(qntz[n][m])          for m in bn] for n in bn]

#%% Presentation
img, qntz = np.block(img), np.block(qntz)
nz  = sum((qntz != 0).flat)
di([org, qntz, img, org - img],
    [f'original\n{N}×{N} = {N*N} pixels',
     f'DCT 2D\n{N/B:.0f}×{N/B:.0f} = {N**2/B**2:.0f} of {B}×{B} blocks',
     f'Reconstruction\nQ = {Q}',
     f'Difference\n{nz} ({nz/(N*N):,.1%}) non-zeros'], grid = False, clip = True)

exit()
#%% Is this a new normal?
from matplotlib.pyplot import hist, show
from matplotlib.colors import Normalize, LinearSegmentedColormap as lscm
from auxiliary import YCbCr_ext_channels as YCbCr
N, bins, patches = hist((org - img).flat, bins = 0x100, density = True)

# See: https://matplotlib.org/stable/gallery/statistics/hist.html
fracs = N/N.max(); norm = Normalize(fracs.min(), fracs.max())

# The higher bar the lighter color
cm = lscm.from_list(YCbCr[0][0], YCbCr[0][1:-1], N = 0x100)
for thisfrac, thispatch in zip(fracs, patches):
    thispatch.set_facecolor(cm(norm(thisfrac)))
show()
# %%
'''
Scrapyard and parking lot (see e.g.: 
+ https://maps.app.goo.gl/Y2xsDhVSk51mjC3KA 
+ https://maps.app.goo.gl/qD9qW3ypFafsbHdK6
+ https://maps.app.goo.gl/BpsS7N7PhxF1HXUs8 - they are much more interesting! 
And definitely less pretentious...)
art = 'Mustang GTD'         # Kiger?
art = 'Malewicz I'          # a.k.a. 'Negroes Fighting in a Cellar at Night' by Allais 1897
art = 'Malewicz II'         # or 'Bociany albinosy pośród śnieżnej zamieci' by OT.TO 1997
art = 'Rothko'              # vel 'Orange, Red, Yellow' 1961
art = 'BayerLCD'            # Color channel test pattern (Rothko & Malewicz would surely
                            # have been proud of me! ;)
art = 'Isotoxal octagons'   # "Study in RGB, CMYK and S"... A more colorful version of the C. Doyle's novel
art = 'Pollock No. 5' # https://blogs.uoregon.edu/richardtaylor/2016/02/08/fractal-analysis-of-jackson-pollocks-poured-paintings/
'''