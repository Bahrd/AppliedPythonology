from cv2 import imread
from numpy import count_nonzero, any, all

## Parameters
f = 'Tesla-M3'
img = imread('./{0}.png'.format(f))
bckgrnd_bgr = 0x0, 0x0, 0xff # If the background is red 

### A pixel-counting method
h, w = img.shape[0], img.shape[1]
all = h * w           # No. of all pixels
##Pseudo-Python:
#area = 0             # No. of frontal area pixels
#for x in range (h):
#    for y in range (w):
#        bgr = tuple(img[x, y])
#        area += bgr != bckgrnd_bgr
## ... and a code:
area = count_nonzero(any(img != bckgrnd_bgr, axis = 2))

## Area computation/conversion
# Image size in meters (matches the car's dimensions when tightly cropped)
HxW = 1.443 * 2.089     # Model 3's H and W ([mm], unfolded mirrors)
a_m = HxW/all * area    # Area in m²
a_ft = a_m * 10.76      # m² to ft² conversion (1m ~ 3.28ft)
print('Pixel counted {0}\'s frontal area = {1}m² ({2}ft²)'.format(f, 
                                                    round(a_m, 2), 
                                                    round(a_ft, 2)))

### A Monte Carlo approach (random sampling)
from numpy.random import rand
from numpy import array
all = 1000           # No. of all samples 
##Pseudo-Python:
#area = 0            # No. of pixels inside the frontal area
#for _ in range(all):
#    x, y = RR(h), RR(w)
#    bgr = tuple(img[x, y])
#    area += bgr != bckgrnd_bgr
## ... and a code:
x, y = array([rand(all) * h, rand(all) * w]).astype(int)
area = count_nonzero(any(img[x, y] != bckgrnd_bgr, axis = 1))

a_m = HxW/all * area; a_ft = a_m * 10.76
print('Monte Carlo {0}\'s frontal area = {1}m² ({2}ft²)'.format(f, 
                                                    round(a_m, 2), 
                                                    round(a_ft, 2)))