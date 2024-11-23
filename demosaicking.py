import cv2; import numpy as np; import auxiliary as aux

#### Image 'framing'
# Note - the example works only for square images (N x N) and for even N
# (the filter segments are 2 x 2)
img = cv2.cvtColor(cv2.imread('./images/GrassHopper.PNG'), cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (128, 128), interpolation = cv2.INTER_LINEAR_EXACT)
N = img.shape[0]; X = [N >> 1]; X *= 2

## Bayer CFA (Kodak Research Laboratory)
#  Peter Dillon and Albert Brault, 1974 & Bryce E. Bayer, 1976
#  http://image-sensors-world.blogspot.com/2019/03/technology-emmy-awards-for-color-filter.html
#  A segment mask definition (type 'uint8' required by OpenCV's filters)
BayerMask = np.array([[[0, 1], [0, 0]],             #R
                      [[1, 0], [0, 1]],             #G'n'G
                      [[0, 0], [1, 0]]], np.uint8)  #B
#  Making an image size CFA
BayerFilter = aux.CFA(BayerMask, X)

# deBayer filter definition (an example)
deBayerMask = np.ones((2, 2))
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]

## Demosaicking 100
## Capturing an image with a CFA sensor
#  Mosaicking, i.e. filtering the image through the CFA
raw = img * BayerFilter
# Evaluating the lacking pixels (in a straightforward/naïve approach)
R, G, B = [cv2.filter2D(raw[..., n], -1, deBayerFilter[n]) for n in range(3)]
rgb = np.dstack((R, G, B))
## Presentation
channels = ('red', 'green', 'blue')
# The Bayer CFA mosaic (aka 'RAW') and the de-mosaicked image
aux.displayChannels((raw, rgb), channels)
# Input vs. output image
aux.displayImages((img, rgb, img - rgb), ('scene', 'image', 'diff'), grid = False)

'''
A bit more directly interpolation-based demosaicking routines:
- the lazy one (with no educational value what.so.ever...)
- the illustrative one (with a bit of educational value)
'''
## An interpolation scheme derived from Open CV
scheme = cv2.INTER_LINEAR_EXACT
img = cv2.resize(cv2.cvtColor(cv2.imread('./images/GrassHopper.png'), cv2.COLOR_BGR2RGB),
                 (512, 512),
                 interpolation = scheme)
N, M, _ = img.shape
# Moisaicking (Bayer CFA): take every other pixel in row/column as R (even) and B (odd)
# and the remaining ones as GI and GII, respectively
raws = img[0:N:2, 0:M:2, 0], img[1:N:2, 1:M:2, 2], img[1:N:2, 0:M:2, 1], img[0:N:2, 1:M:2, 1]
## De-mosaicking (de-Bayering by interpolation)
#  R   G     R   0     0   G     0   0     0   0
#         =         +         +         +
#  G   B     0   0     0   0     G   0     0   B
#  where we can exploit linearity/superposition to restore the green channel from GI and GII
#  using the same scheme as for R and B channels
R, B, GI, GII = [cv2.resize(channel,  (M, N), interpolation = scheme) for channel in raws]
G = GI//2 + GII//2  # Note integer averaging... (without normalization the resulting image
                    #                            would've been greenish (or else...))
channels = ('Original', 'R', 'B', 'GI', 'GII', 'G')
aux.displayImages((img, R, B, GI, GII, G), channels, grid = False)

rgb = np.dstack((R, G, B))
channels = ('red', 'green', 'blue')
aux.displayChannels((img, rgb), channels)

images = ('Original', 'Demo\'ed', 'Little diff\'s...') # https://youtu.be/ab7eVVG3I8s?t=43
aux.displayImages((img, rgb, img - rgb), images, grid = False)

# Here we reuse one of our implementation of interpolation schemes
# in order to demonstrate that our good ol' friend works exactly (if little more majestic) like the one based on OpenCV
from interpolation import interpolate as Σ, Λ #ϕ, ξ
from matplotlib.colors import LinearSegmentedColormap as lscm

# An old school 2D interpolation from a 1D one...
ψ = Λ; name = ψ.__name__

reds = lscm.from_list('_', ['black', 'red'])
red_raw, red = raws[0], np.zeros((N, N))
# Rows first...
for m in range(M >> 1):
   red[m, ...] = np.array(Σ(red_raw[m, ...], N, φ = ψ)).flat
aux.displayImages((img, red), ('Original', f'{name}-demo\'ed red rows'), cmp = reds, grid = False)
# ...then columns:
for n in range(N):
   red[:, n] = np.array(Σ(red[:M >> 1, n], N, φ = ψ)).flat
aux.displayImages((img, red), ('Original', f'{name}-demo\'ed red rows & columns'), cmp = reds, grid = False)