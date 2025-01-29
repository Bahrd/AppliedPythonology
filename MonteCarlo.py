from cv2 import imread
from numpy import count_nonzero, any

## Parameters
f = 'Tesla-M3'
img = imread(f'./images/vehicles/{f}.png')
gnd_bgr = 0x0, 0x0, 0xff # Change if background isn't pure red

### A pixel-counting method
h, w, _ = img.shape; hxw = h * w    # No. of all pixels
##Pseudo-Python:
#pixels = 0                         # No. of frontal area pixels
#for x in range (h):
#    for y in range (w):
#        bgr = tuple(img[x, y])
#        pixels += bgr != gnd_bgr

## ... and a code:
pixels = count_nonzero(any(img != gnd_bgr, axis = 2))

## Area computation/conversion
# Image size in meters (matches the car's dimensions when tightly cropped)
HxW = 1.443 * 2.089     # Model 3's H and W ([mm], unfolded mirrors)

a_m = HxW/hxw * pixels  # Area in m²
a_ft = a_m * 10.76      # m² to ft² conversion (1m ~ 3.28ft)
print(f'Pixel counted {f}\'s frontal area = {a_m:2.2f}m² ({a_ft:2.2f}ft²)')

### A Monte Carlo approach (random sampling)
from numpy.random import default_rng as drng
samples = 1_000         # No. of all samples
rng = drng()            # Random samples with Numpy 1.17+
##Pseudo-Python:
#pixels = 0             # No. of pixels inside the frontal area
#for _ in range(samples):
#    x, y = RR(h), RR(w)
#    bgr = tuple(img[x, y])
#    pixels += bgr != gnd_bgr

## ... and a code
x, y = rng.integers([h, w], size = [samples, 2]).T
pixels = count_nonzero(any(img[x, y] != gnd_bgr, axis = 1))

a_m = HxW/samples * pixels; a_ft = a_m * 10.76
print(f'Monte Carlo {f}\'s frontal area = {a_m:2.2f}m² ({a_ft:2.2f}ft²)')

'''
## In case your image is not a rectangle but a circle (from a fisheye, say),
#  you should find this piece rather useful:
# https://g.co/bard/share/3a07f8ffc86b # Don't trust AI... ;)
# https://math.stackexchange.com/questions/927347/uniform-distribution-over-disk#:~:text=This%20is%20the%20uniform%20distribution%20on%20the%20unit,Y%29%20%3D%20%28A%20cos%20B%2C%20A%20sin%20B%29.
# https://www.youtube.com/watch?v=hhFzJvaY__U

from matplotlib.pyplot import gca, scatter, title, show
from numpy import sqrt, sin, cos, pi as π
from numpy.random import uniform as U

N = 10_000
## Generate N random points in the polar coordinates
R, θ = U(0, 1, N), U(0, 2*π, N)

# Display the motley points
gca().set_aspect('equal'); title('X = √R⋅cosθ and Y = √R⋅sinθ')
#  Note that to maintain uniformity of the distribution we need
#  the Jacobian of the map (from polar to Cartesian coordinates) constant
#
#         ⌈ ∂X/∂R  ∂X/∂θ ⌉
#      det|              | = const.
#         ⌊ ∂Y/∂R  ∂Y/∂θ ⌋
#
# Indeed for the mapping
X, Y = sqrt(R) * cos(θ), sqrt(R) * sin(θ)
# we get
#
#         ⌈ (1/2√R⋅cosθ  -√R⋅sinθ ⌉
#      det|                       | = 2⁻¹(cos²θ + sin²θ),
#         ⌊ (1/2√R⋅sinθ   √R⋅cosθ ⌋
#
# which is constant by virtue of a quite famous identity... ;)
scatter(X, Y, marker = '.', color = 'r'); show()
'''