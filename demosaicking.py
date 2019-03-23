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
# Note - the example works only for square images (N x N) and for even N 
# (the filter segments are 2 x 2)
img = cv2.imread("GrassHopper.PNG"); img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
N = img.shape[0]; X = [N >> 1]; X *= 2 


## Bayer CFA (Bryce E. Bayer@Eastman Kodak, 1976)
# A segment mask definition (type 'uint8' required by OpenCV's filters)
BayerMask = np.array([[[0, 1], [0, 0]],             #R
                      [[1, 0], [0, 1]],             #G
                      [[0, 0], [1, 0]]], np.uint8)  #B
#  Making a CFA
BayerFilter = CFA(BayerMask, X)

# deBayer filter definition (an example)
deBayerMask = np.ones((2, 2))
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]


## Capturing an image with a CFA sensor
#  Mosaicking, i.e. filtering the image through the CFA
raw = img * BayerFilter

## Demosaicking 
# Evaluating the lacking pixels 
R, G, B = [cv2.filter2D(raw[..., n], -1, deBayerFilter[n]) for n in range(3)]
rgb = np.dstack((R, G, B))

## Presentation
channels = ("red", "green", "blue")
# The Bayer CFA mosaic (aka 'RAW') and the de-mosaicked image
displayChannels((raw, rgb), channels, range(len(channels)))

# Input vs. output image
displayImages((img, rgb, img - rgb))