import cv2; import numpy as np; import matplotlib.pyplot as plt

## Auxiliary functions
# CFA filter mask
def CFA(masks, X):
    return np.dstack(np.tile(mask, X) for mask in masks)
# Channels presentation
def displayChannels(image, positions, colors, sizeX = 2, sizeY = 2):
    for p, c in zip(positions, colors):
        plt.subplot(sizeX, sizeY, p + 1)
        plt.imshow(image[..., p], c)
# Bayer CFA mask segment definition
BayerMask = np.array([[[0, 1], [0, 0]],             #B
                      [[1, 0], [0, 1]],             #G
                      [[0, 0], [1, 0]]], np.uint8)  #R uint8 required by OpenCV
# deBayer filter definition
deBayerMask = np.ones((2, 2)); 

## Image 'capturing'
# Note - the example works for the square images of even size only
img = cv2.imread("Grasshopper.PNG"); N = img.shape[0]; X = [int(N/2), int(N/2)]

## Mosaicking (simulating the RAW sensor capture)
# The Bayer color filter array
BayerFilter = np.array(CFA(BayerMask, X))
# Processing
img = img * BayerFilter

## Demosaicking 
# A simple averaging filter
deBayerFilter = [deBayerMask * w for w in [1, 1/2, 1]]
# Processing
B, G, R = [cv2.filter2D(img[..., n], -1, deBayerFilter[n]) for n in range(3)]

## Presentation
# A Bayer CFA mosaic (aka 'RAW')
colors = ["Blues_r", "Greens_r", "Reds_r"] 
displayChannels(img, range(3), colors)
plt.subplot(2, 2, 4); plt.imshow(img)
plt.show()

# A Bayer CFA de-mosaicked image (aka 'JPG')
bgr = np.dstack((B, G, R))
displayChannels(bgr, range(3), colors)
rgb = np.dstack((R, G, B))
plt.subplot(2, 2, 4); plt.imshow(rgb)
plt.show()
