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
        cmp = lscm.from_list('cmp', ['black', c])
        plt.imshow(image[..., p], cmp)
    plt.subplot(rows, cols, rows * cols)
    plt.imshow(image)
    plt.show()

## Bayer CFA (Bryce E. Bayer@Eastman Kodak, 1976)
# A segment mask definition (type 'uint8' required by OpenCV's filters)
BayerMask = np.array([[[0, 1], [0, 0]],             #R
                      [[1, 0], [0, 1]],             #G
                      [[0, 0], [1, 0]]], np.uint8)  #B
# deBayer filter definition (an example)
deBayerMask = np.ones((2, 2))

## Image 'capturing'
# Note - the example works only for square images (N x N, and where N is even)
img = cv2.imread("GrassHopper.PNG"); N = img.shape[0]; X = [int(N/2), int(N/2)]
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

## Mosaicking (capturing an image with a CFA sensor)
# The Bayer color filter array
BayerFilter = CFA(BayerMask, X)
# Processing
raw = img * BayerFilter

## Demosaicking 
# A simple averaging filter
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]
# Processing
R, G, B = [cv2.filter2D(raw[..., n], -1, deBayerFilter[n]) for n in range(3)]

## Presentation
# A Bayer CFA mosaic (aka 'RAW')
colors = ["red", "green", "blue"] 
displayChannels(raw, range(3), colors)
# A Bayer CFA de-mosaicked image (aka 'JPG' - I know, I know... )
rgb = np.dstack((R, G, B))
displayChannels(rgb, range(3), colors)
# Input vs. output image
plt.subplot(131); plt.imshow(img); plt.subplot(132); plt.imshow(rgb)
plt.subplot(133); plt.imshow(img - rgb); plt.show()