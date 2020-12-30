## Auxiliary routines for image processing algorithms
import numpy as np; import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm

#Image presentation
def displayImages(images, titles = '', cmp = 'gray', show = True):
    if type(images) is tuple or type(images) is list: 
        number = len(images)
        fig = plt.figure(figsize = (number * 3, 3)); fig.tight_layout()
        for p, image, title in zip(range(number), images, titles):
            sb = plt.subplot(1, number, p + 1)
            sb.set_xticks([]); sb.set_yticks([])
            plt.title(title); plt.imshow(image, cmap = cmp)
    else:
        sb = plt.subplot(1, 1, 1)
        sb.set_xticks([]); sb.set_yticks([])
        plt.title(titles); plt.imshow(images, cmap = cmp)
    if show: plt.show()

def displayPlots(plots, titles):
    number = len(plots)
    for p, pl, title in zip(range(number), plots, titles):
        plt.subplot(1, number, p + 1)
        plt.title(title); plt.plot(pl)
    plt.show()

# Image dissection presentation (the channels and the resulting image)
def displayChannels(images, channels, positions, rows = 1, cols = 4):
    for image in images:
        for p, c in zip(positions, channels):
            sb = plt.subplot(rows, cols, p + 1)
            sb.set_xticks([]); sb.set_yticks([])
            cmp = lscm.from_list('_', ['black', c])
            plt.title(c); plt.imshow(image[..., p], cmp)
        sb = plt.subplot(rows, cols, rows * cols)
        sb.set_xticks([]); sb.set_yticks([])
        plt.title("RGB"); plt.imshow(image)
        plt.show()

# CFA filter mask (replication of a single CFA segment into a whole sensor mask)
def CFA(masks, X):
    return np.dstack([np.tile(mask, X) for mask in masks])

JPG_QT_Y = [[16, 11, 10, 16,  24,  40,  51,  61],
            [12, 12, 14, 19,  26,  58,  60,  55],
            [14, 13, 16, 24,  40,  57,  69,  56],
            [14, 17, 22, 29,  51,  87,  80,  62],
            [18, 22, 37, 56,  68, 109, 103,  77],
            [24, 35, 55, 64,  81, 104, 113,  92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103,  99]]

JPG_QT_CbCr =  [[17, 18, 24, 47, 99, 99, 99, 99], 
                [18, 21, 26, 66, 99, 99, 99, 99], 
                [24, 26, 56, 99, 99, 99, 99, 99], 
                [47, 66, 99, 99, 99, 99, 99, 99], 
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99], 
                [99, 99, 99, 99, 99, 99, 99, 99], 
                [99, 99, 99, 99, 99, 99, 99, 99]]

## A decorative fun... See: https://www.geeksforgeeks.org/decorators-in-python/
from time import time as TT
def ITT(f):
	def time_warper_wrapper(*args, **kwargs): 
		begin = TT() # from time import time as TT
		r = f(*args, **kwargs) 
		end = TT()
		print('{0} evaluated in {1}s'.format(f.__name__, round(end - begin)))
		return r
	return time_warper_wrapper
