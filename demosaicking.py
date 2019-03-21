import cv2; import numpy as np; import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm

## Auxiliary functions
# CFA filter mask
def CFA(masks, X):
    return np.dstack(np.tile(mask, X) for mask in masks)
# Channels presentation
def displayChannels(image, positions, colors, sizeX = 1, sizeY = 4):
    for p, c in zip(positions, colors):
        plt.subplot(sizeX, sizeY, p + 1)
        cmp = lscm.from_list('cmp', ['black', c])
        plt.imshow(image[..., p], cmp)
    plt.subplot(sizeX, sizeY, sizeX * sizeY)
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
# Note - the example works for the square images of even size only
raw = cv2.imread("GrassHopper.PNG"); N = raw.shape[0]; X = [int(N/2), int(N/2)]
raw = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB) 

## Mosaicking (simulating the RAW sensor capture)
# The Bayer color filter array
BayerFilter = np.array(CFA(BayerMask, X))
# Processing
img = raw * BayerFilter

## Demosaicking 
# A simple averaging filter
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]
# Processing
R, G, B = [cv2.filter2D(img[..., n], -1, deBayerFilter[n]) for n in range(3)]


## Presentation
# A Bayer CFA mosaic (aka 'RAW')
colors = ["red", "green", "blue"] 
displayChannels(img, range(3), colors)
# A Bayer CFA de-mosaicked image (aka 'JPG' - I know, I know... )
rgb = np.dstack((R, G, B))
displayChannels(rgb, range(3), colors)
# Input vs. output image
plt.subplot(131); plt.imshow(raw); plt.subplot(132); plt.imshow(rgb)
plt.subplot(133); plt.imshow(raw - rgb)
plt.show()