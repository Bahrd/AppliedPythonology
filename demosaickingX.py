import cv2; import numpy as np; import auxiliary as aux

#### Image 'framing'
# Note - the example works only for square images (N x N) and 
# for 6 x 6 filter segments (and hence for N such that N % 6 = 0
img = cv2.cvtColor(cv2.imread("GrassHopperX.PNG"), cv2.COLOR_BGR2RGB) 
N = img.shape[0]; X = [int(N/6)]; X *= 2


## X-Trans (Fuji, 2012)
# A segment mask definition (type 'uint8' required by OpenCV's filters)
XTransMask = np.array([[[0, 0, 0, 0, 1, 0], 
                        [1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 1],
                        [0, 1, 0, 0, 0, 0]],            #R
                       [[1, 0, 1, 1, 0, 1],
                        [0, 1, 0, 0, 1, 0],
                        [1, 0, 1, 1, 0, 1],
                        [1, 0, 1, 1, 0, 1],
                        [0, 1, 0, 0, 1, 0],
                        [1, 0, 1, 1, 0, 1]],            #G
                       [[0, 1, 0, 0, 0, 0], 
                        [0, 0, 0, 1, 0, 1],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0]]], np.uint8) #B
# Making an image size CFA
XTransFilter = aux.CFA(XTransMask, X)

# An example of the deXTrans filter (far from Fuji... )
# Note that the weights' values result from the mosaic and demosaic filters' 
# shapes: the weighted filters' coefficients (per segment) need to sum-up to 1.
deXTransMask = np.array([[0.  , 0.  , 0.  , 0.  , 0.  , 0.  ],
                         [0.  , 0.25, 0.5 , 0.5 , 0.25, 0.  ],
                         [0.  , 0.5 , 1.  , 1.  , 0.5 , 0.  ],
                         [0.  , 0.5 , 1.  , 1.  , 0.5 , 0.  ],
                         [0.  , 0.25, 0.5 , 0.5 , 0.25, 0.  ],
                         [0.  , 0.  , 0.  , 0.  , 0.  , 0.  ]])
deXTransFilter = np.array([deXTransMask * w for w in [1/2, 1/5, 1/2]])


## Capturing an image with a CFA sensor
#  Mosaicking, i.e. filtering the image through the CFA
raw = img * XTransFilter

## Demosaicking
# Evaluating the lacking pixels (an utterly naive approach)
R, G, B = [cv2.filter2D(raw[..., n], -1, deXTransFilter[n]) for n in range(3)]
rgb = np.dstack((R, G, B))

## Presentation
channels = ("red", "green", "blue")
# An X-Trans CFA mosaic (aka 'RAW') and the de-mosaicked image (aka 'JPG')
aux.displayChannels((raw, rgb), channels, range(len(channels)))
# Input vs. output image
aux.displayImages((img, rgb, img - rgb), ("scene", "image", "diff"))