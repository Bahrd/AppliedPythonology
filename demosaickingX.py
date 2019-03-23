import cv2; import numpy as np; import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm

## Auxiliary functions
# CFA filter mask (replication of a single CFA segment into a whole sensor mask)
def CFA(masks, X):
    return np.dstack(np.tile(mask, X) for mask in masks)

# Image presentation (the channels and the aggregated image - all in a row)
def displayChannels(image, positions, colors, rows = 1, cols = 4):
    for p, c in zip(positions, colors):
        plt.subplot(rows, cols, p + 1)
        cmp = lscm.from_list('_', ['black', c])
        plt.imshow(image[..., p], cmp)
    plt.subplot(rows, cols, rows * cols)
    plt.imshow(image)
    plt.show()


#### Image 'capturing'
# Note - the example works only for square images (N x N) with N % 6 = 0, 
# and for 6 x 6 filter segments
img = cv2.imread("GrassHopperX.PNG"); img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
N = img.shape[0]; X = [int(N/6)]; X *= 2

## X-Trans (Fuji, 2012)
# A segment mask definition (type 'uint8' required by OpenCV's filters)
XTransMask = np.array([[[0, 0, 0, 0, 1, 0], 
                        [1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 1],
                        [0, 1, 0, 0, 0, 0]], 
                       [[1, 0, 1, 1, 0, 1],
                        [0, 1, 0, 0, 1, 0],
                        [1, 0, 1, 1, 0, 1],
                        [1, 0, 1, 1, 0, 1],
                        [0, 1, 0, 0, 1, 0],
                        [1, 0, 1, 1, 0, 1]],
                       [[0, 1, 0, 0, 0, 0], 
                        [0, 0, 0, 1, 0, 1],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0]]], np.uint8)
# Making an image size CFA
XTransFilter = CFA(XTransMask, X)

# An example of the deXTrans filter (far from Fuji... )
# Note that "secret" weights result from the mosaic and demosaic filters' 
# shapes: the weighted filter's coefficients (per segment) need to sum-up to 1.
deXTransMask = np.array([[0.  , 0.  , 0.  , 0.  , 0.  , 0.  ],
                         [0.  , 0.25, 0.5 , 0.5 , 0.25, 0.  ],
                         [0.  , 0.5 , 1.  , 1.  , 0.5 , 0.  ],
                         [0.  , 0.5 , 1.  , 1.  , 0.5 , 0.  ],
                         [0.  , 0.25, 0.5 , 0.5 , 0.25, 0.  ],
                         [0.  , 0.  , 0.  , 0.  , 0.  , 0.  ]])/9
deXTransFilter = np.array([deXTransMask * w for w in [1/8, 1/20, 1/8]]) * 36


## Capturing an image with a CFA sensor
#  Mosaicking, i.e. filtering the image through the CFA
raw = img * XTransFilter

## Demosaicking (a very naive approach)
# Evaluating the lacking pixels 
R, G, B = [cv2.filter2D(raw[..., n], -1, deXTransFilter[n]) for n in range(3)]
rgb = np.dstack((R, G, B))

## Presentation
# An X-Trans CFA mosaic (aka 'RAW') and the de-mosaicked image (aka 'JPG')
colors = ["red", "green", "blue"] 
displayChannels(raw, range(3), colors); displayChannels(rgb, range(3), colors)
# Input vs. output image
plt.subplot(131); plt.imshow(img); plt.subplot(132); plt.imshow(rgb)
plt.subplot(133); plt.imshow(img - rgb)
plt.show()