import cv2; import numpy as np; import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm

## Auxiliary functions
#Images presentation
def displayImages(images):
    for index in range(len(images)):
        plt.subplot(1, len(images), index + 1)
        plt.imshow(images[index])
    plt.show()

# Image dissection presentation (the channels and the aggregated images)
def displayChannels(images, channels, positions, rows = 1, cols = 4):
    for image in images:
        for p, c in zip(positions, channels):
            plt.subplot(rows, cols, p + 1)
            cmp = lscm.from_list('_', ['black', c])
            plt.imshow(image[..., p], cmp)
        plt.subplot(rows, cols, rows * cols)
        plt.imshow(image)
        plt.show()

# CFA filter mask (replication of a single CFA segment into a whole sensor mask)
def CFA(masks, X):
    return np.dstack(np.tile(mask, X) for mask in masks)

#### Image 'framing'
# Note - the example works only for square images (N x N) and 
# for 6 x 6 filter segments (and hence for N such that N % 6 = 0
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
# Note that the weights' values result from the mosaic and demosaic filters' 
# shapes: the weighted filters' coefficients (per segment) need to sum-up to 1.
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
channels = ("red", "green", "blue")
# An X-Trans CFA mosaic (aka 'RAW') and the de-mosaicked image (aka 'JPG')
displayChannels((raw, rgb), channels, range(len(channels)))

# Input vs. output image
displayImages((img, rgb, img - rgb))