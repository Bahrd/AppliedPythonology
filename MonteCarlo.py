from cv2 import imread
from numpy import count_nonzero, any

## Parameters
f = 'Tesla-M3'
img = imread('./{0}.png'.format(f))
bgnd_bgr = 0x0, 0x0, 0xff # Change if background isn't pure red 

### A pixel-counting method
h, w, _ = img.shape; hxw = h * w    # No. of all pixels
##Pseudo-Python:
#pixels = 0                         # No. of frontal area pixels
#for x in range (h):
#    for y in range (w):
#        bgr = tuple(img[x, y])
#        pixels += bgr != bckgrnd_bgr

## ... and a code:
pixels = count_nonzero(any(img != bgnd_bgr, axis = 2))

## Area computation/conversion
# Image size in meters (matches the car's dimensions when tightly cropped)
HxW = 1.443 * 2.089     # Model 3's H and W ([mm], unfolded mirrors)

a_m = HxW/hxw * pixels  # Area in m²
a_ft = a_m * 10.76      # m² to ft² conversion (1m ~ 3.28ft)
print('Pixel counted {0}\'s frontal area = {1}m² ({2}ft²)'.format(f, 
                                                    round(a_m, 2), 
                                                    round(a_ft, 2)))

### A Monte Carlo approach (random sampling)
from numpy.random import default_rng as drng
samples = 1000          # No. of all samples 
rng = drng()            # Random samples with Numpy 1.17+
##Pseudo-Python:
#pixels = 0             # No. of pixels inside the frontal area
#for _ in range(all):
#    x, y = RR(h), RR(w)
#    bgr = tuple(img[x, y])
#    pixels += bgr != bckgrnd_bgr

## ... and a code 
x, y = rng.integers([h, w], size = [samples, 2]).T 
pixels = count_nonzero(any(img[x, y] != bgnd_bgr, axis = 1))

a_m = HxW/samples * pixels; a_ft = a_m * 10.76
print('Monte Carlo {0}\'s frontal area = {1}m² ({2}ft²)'.format(f, 
                                                    round(a_m, 2), 
                                                    round(a_ft, 2)))