## Auxiliary functions for image processing algorithms
import numpy as np; import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm

#Image presentation
def displayImages(images, titles):
    number = len(images)
    for p, image, title in zip(range(number), images, titles):
        plt.subplot(1, number, p + 1)
        plt.title(title); plt.imshow(image)
    plt.show()

# Image dissection presentation (the channels and the resulting image)
def displayChannels(images, channels, positions, rows = 1, cols = 4):
    for image in images:
        for p, c in zip(positions, channels):
            plt.subplot(rows, cols, p + 1)
            cmp = lscm.from_list("_", ["black", c])
            plt.title(c); plt.imshow(image[..., p], cmp)
        plt.subplot(rows, cols, rows * cols)
        plt.title("RGB"); plt.imshow(image)
        plt.show()

# CFA filter mask (replication of a single CFA segment into a whole sensor mask)
def CFA(masks, X):
    return np.dstack(np.tile(mask, X) for mask in masks)

