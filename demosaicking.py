import cv2; import numpy as np; import auxiliary as aux

#### Image 'framing'
# Note - the example works only for square images (N x N) and for even N 
# (the filter segments are 2 x 2)
img = cv2.cvtColor(cv2.imread('./images/GrassHopper.PNG'), cv2.COLOR_BGR2RGB) 
N = img.shape[0]; X = [N >> 1]; X *= 2 


## Bayer CFA (Kodak Research Laboratory)
#  Peter Dillon and Albert Brault, 1974 & Bryce E. Bayer, 1976
#  http://image-sensors-world.blogspot.com/2019/03/technology-emmy-awards-for-color-filter.html
#  A segment mask definition (type 'uint8' required by OpenCV's filters)
BayerMask = np.array([[[0, 1], [0, 0]],             #R
                      [[1, 0], [0, 1]],             #G
                      [[0, 0], [1, 0]]], np.uint8)  #B
#  Making an image size CFA
BayerFilter = aux.CFA(BayerMask, X)

# deBayer filter definition (an example)
deBayerMask = np.ones((2, 2))
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]


## Capturing an image with a CFA sensor
#  Mosaicking, i.e. filtering the image through the CFA
raw = img * BayerFilter

## Demosaicking 
# Evaluating the lacking pixels (in a straightforward/naïve approach)
R, G, B = [cv2.filter2D(raw[..., n], -1, deBayerFilter[n]) for n in range(3)]
rgb = np.dstack((R, G, B))

## Presentation
channels = ('red', 'green', 'blue')
# The Bayer CFA mosaic (aka 'RAW') and the de-mosaicked image
aux.displayChannels((raw, rgb), channels)
# Input vs. output image
aux.displayImages((img, rgb, img - rgb), ('scene', 'image', 'diff'))