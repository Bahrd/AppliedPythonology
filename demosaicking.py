import cv2; import numpy as np; import matplotlib.pyplot as plt

## Auxiliary functions
# CFA filter mask
def CFA(X, masks):
    return np.dstack(np.tile(mask, X) for mask in masks)
# Channels presentation
def displayChannels(image, position, color, sizeX = 2, sizeY = 2):
    plt.subplot(sizeX, sizeY, position + 1)
    plt.imshow(image[..., position], color)
# Bayer CFA mask segment definition
BayerMask = [[[0, 1], [0, 0]],  #B
             [[1, 0], [0, 1]],  #G
             [[0, 0], [1, 0]]]  #R
# deBayer filter definition
deBayerMask = np.ones((2, 2)); 

## Image 'capturing'
# Note - the example works for the square images of even size only
img = cv2.imread("Grasshopper.PNG"); N = img.shape[0]; X = [int(N/2), int(N/2)]

## Mosaicking (simulating the RAW sensor capture)
# The Bayer CFA sensor
BayerFilter = np.array(CFA(X, BayerMask), dtype = np.uint8)
# Processing
img = img * BayerFilter

## Demosaicking 
#  The simplest one - based on averaging
deBayerFilter = [deBayerMask * n for n in [1, 1/2, 1]]

# Processing
B, G, R = [cv2.filter2D(img[..., n], -1, deBayerFilter[n]) for n in range(3)]
bgr = np.dstack((B, G, R))

## Presentation
# A Bayer CFA mosaic (aka 'RAW')
colors = ["Blues_r", "Greens_r", "Reds_r"] 
[displayChannels(img, p, c) for p, c in zip(range(3), colors)]
plt.subplot(2, 2, 4); plt.imshow(img)
plt.show()

# A Bayer CFA de-mosaicked image (aka 'JPG')
[displayChannels(bgr, p, c) for p, c in zip(range(3), colors)]
rgb = np.dstack((R, G, B))
plt.subplot(2, 2, 4); plt.imshow(rgb)
plt.show()