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
        cmap = lscm.from_list('mp', ['black', c])
        plt.imshow(image[..., p], cmap)
    plt.subplot(sizeX, sizeY, sizeX * sizeY)
    plt.imshow(image)
    plt.show()

# Bayer CFA mask segment definition (type 'uint8' required by OpenCV's filters)
BayerMask = np.array([[[0, 1], [0, 0]],             #R
                      [[1, 0], [0, 1]],             #G
                      [[0, 0], [1, 0]]], np.uint8)  #B
# deBayer filter definition
deBayerMask = np.ones((2, 2))

## Image 'capturing'
# Note - the example works for the square images of even size only
image = cv2.imread("Grasshopper.PNG"); N = image.shape[0]; X = [int(N/2), int(N/2)]
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

## Mosaicking (simulating the RAW sensor capture)
# The Bayer color filter array
BayerFilter = np.array(CFA(BayerMask, X))
# Processing
img = image * BayerFilter

## Demosaicking 
# A simple averaging filter
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]
# Processing
R, G, B = [cv2.filter2D(img[..., n], -1, deBayerFilter[n]) for n in range(3)]


## Presentation
# A Bayer CFA mosaic (aka 'RAW')
colors = ["red", "green", "blue"] 
displayChannels(img, range(3), colors)
# A Bayer CFA de-mosaicked image (aka 'JPG/PNG')
rgb = np.dstack((R, G, B))
displayChannels(rgb, range(3), colors)
# Input vs. output image
plt.subplot(121); plt.imshow(image); plt.subplot(122); plt.imshow(rgb)
plt.show()