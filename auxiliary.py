## Auxiliary routines for image processing algorithms
import numpy as np; import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lscm

#Image presentation
def displayImages(images, titles, cmp = 'gray'):
    number = len(images)
    for p, image, title in zip(range(number), images, titles):
        plt.subplot(1, number, p + 1)
        plt.title(title); plt.imshow(image, cmap = cmp)
    plt.show()

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
            plt.subplot(rows, cols, p + 1)
            cmp = lscm.from_list("_", ["black", c])
            plt.title(c); plt.imshow(image[..., p], cmp)
        plt.subplot(rows, cols, rows * cols)
        plt.title("RGB"); plt.imshow(image)
        plt.show()

# CFA filter mask (replication of a single CFA segment into a whole sensor mask)
def CFA(masks, X):
    return np.dstack(np.tile(mask, X) for mask in masks)

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


## Some interpolating functions, Π(x), ψ(x) and ϕ(x) or... 
#  whatchamacallit this thingamajig...

# The window/rectangular and the hat/tent/triangular (yet anonymous!) function
Π, ψ =  lambda x, l = 0, r = 1: (x >= l) * (x < r), lambda x: (1 - abs(x)) * (abs(x) < 1)
# The Keys' cubic interpolating function (b'cause: https://realpython.com/python-lambda/#syntax)
def ϕ(x):                       
    x, a = abs(x), -0.5
    return (((a + 2) * x**3 - (a + 3) * x**2 + 1)             * Π(x, 0, 1) 
           + (     a * x**3 -     5*a * x**2 + 8*a * x - 4*a) * Π(x, 0, 2) * (1 - Π(x, 0, 1)))

# An interpolation routine Λ: f(n) ➞ f(x) using ϕ, ψ or Π, 
def Φ(x, f, λ):
    n = np.arange(len(f))
    Λ = λ(x - n)                         
    return Λ @ f

# An actual interpolation Φ: Fn ➞ Fx 
def interpolate(fn, N, Λ = [Π, ψ, ϕ]):
    X = np.linspace(0, len(fn), N)
    return [[Φ(x, fn, λ) for λ in Λ] for x in X] 
