## Auxiliary routines for image processing algorithms
import numpy as np; from numpy.linalg import inv
import matplotlib.pyplot as plt; from matplotlib.colors import LinearSegmentedColormap as lscm

#Image presentation
def displayImages(images, titles = '', cmp = 'gray', show = True, grid = True, title = 'Applied Pythonology [Of] Course'):
#    if type(images) is tuple or type(images) is list:
    if isinstance(images, (tuple, list)):
        number = len(images)
        fig = plt.figure(figsize = (number * 3, 3), num = title); fig.tight_layout()
        for p, (image, title) in enumerate(zip(images, titles)):
            sb = plt.subplot(1, number, p + 1)

            sb.set_xticks([]); sb.set_yticks([])
            if grid:
                # Ticks... https://stackoverflow.com/questions/38973868/adjusting-gridlines-and-ticks-in-matplotlib-imshow
                sb.set_xticks(np.arange(-.5, len(image), 1), minor = True)
                sb.set_yticks(np.arange(-.5, len(image), 1), minor = True)
                sb.grid(which = 'minor', color = 'w', linestyle = '-', linewidth = 1)

            plt.title(title); plt.imshow(image, cmap = cmp)
    else:
        sb = plt.subplot(1, 1, 1)

        sb.set_xticks([]); sb.set_yticks([])
        if grid:
            sb.set_xticks(np.arange(-.5, len(images), 1), minor = True)
            sb.set_yticks(np.arange(-.5, len(images), 1), minor = True)
            sb.grid(which = 'minor', color = 'w', linestyle = '-', linewidth = 1)

        plt.title(titles); plt.imshow(images, cmap = cmp)
    if show: plt.show()

def displayPlots(plots, titles):
    for p, (pl, ttl) in enumerate(zip(plots, titles)):
        plt.subplot(1, len(plots), p + 1)
        plt.title(ttl); plt.plot(pl)
    plt.show()

def displayPlotsXY(plots, titles):
    for p, ((x, y), ttl) in enumerate(zip(plots, titles)):
        plt.subplot(1, len(plots), p + 1)
        plt.title(ttl); plt.plot(x, y)
    plt.show()

# Image dissection presentation (the channels and the resulting image)
# Note it is assumed that the images are in the RGB (or other additive) color space
def displayChannels(images, channels, rows = 1, cols = 4, title = 'RGB'):
    for image in images:
        for p, c in enumerate(channels):
            sb = plt.subplot(rows, cols, p + 1)
            sb.set_xticks([]); sb.set_yticks([])
            cmp = lscm.from_list('_', ['black', c])
            plt.title(c); plt.imshow(image[..., p], cmp)
        sb = plt.subplot(rows, cols, rows * cols)
        sb.set_xticks([]); sb.set_yticks([])
        plt.title(title); plt.imshow(image)
        plt.show()

# Color channels for channel and histogram visualizations
RGB_channels = (('R', 'k', 'r'),
                ('G','k', 'g'),
                ('B','k', 'b'))
YCbCr_channels = (('Y', 'k', 'w'),
                  ('Cb','y', 'b'),
                  ('Cr','cyan', 'r'))
YCoCg_channels = (('Y', 'k', 'grey'),
                  ('Co', 'b', 'r'),
                  ('Cg', 'xkcd:pink', 'xkcd:green'))

# Enhanced color channels (Because not only ♪♫ https://youtu.be/PIb6AZdTr-A ♫♪)
RGB_ext_channels = (('R', 'k', 'xkcd:dark red', 'r', 'xkcd:light red'),
                    ('G','k', 'xkcd:dark green', 'g', 'xkcd:light green'),
                    ('B','k', 'xkcd:dark blue', 'b', 'xkcd:light blue'))
YCbCr_ext_channels = (('Y', 'k', 'xkcd:light grey'),
                      ('Cb','y', 'k', 'b'),
                      ('Cr','cyan', 'k', 'r'))
YCoCg_ext_channels = (('Y', 'k', 'xkcd:dark grey', 'grey', 'xkcd:light grey'),
                      ('Co', 'b', 'k', 'r', 'xkcd:light red'),
                      ('Cg', 'xkcd:pink', 'k', 'xkcd:army green', 'xkcd:light green'))

# Image channel dissection
# (this routine works with any number of channels, but with a single image)
def displayAnyChannels(image, channels, rows = 1, cols = 3):
    for p, cn in enumerate(channels):
        sb = plt.subplot(rows, cols, p + 1)
        sb.set_xticks([]); sb.set_yticks([])
        cmp = lscm.from_list('_', cn[1:])
        plt.title(cn[0]); plt.imshow(image[..., p], cmp)
    plt.show()

def channelHistogram(img, art, color_space, colors):
    redux = lambda x: x[0]
    a, b, c = [redux(np.histogram(img[..., cn], bins = 0x100)) for cn in range(0b11)]
    plt.xticks(np.arange(0, 0x101, 0x20)); plt.yticks([])
    plt.plot(a, colors[0], b, colors[1], c, colors[2])
    plt.title(f'{art} in {color_space}'); plt.show()

# Sometimes you just don't care about the return value
def splot(*args, scalex = True, scaley = True, data = None, **kwargs):
    _ = plt.plot(*args, scalex = scalex, scaley = scaley, data = data, **kwargs)

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

## Irréversible Color Transform (ICT)
RGB2YCbCr = [[ .299,     .587,     .114],
             [-.168736, -.331264,  .5],
             [ .5,      -.418688, -.081312]]
YCbCr2RGB = inv(np.array(RGB2YCbCr))

## Reversible Color Transform (RCT)
def RCT(R, G, B):
    Y, Cb, Cr = int(np.floor((R + 2*G + B)/4)), B - G, R - G
    return (Y, Cb, Cr)

def invRCT(Y, Cb, Cr):
    G = Y - int(np.floor((Cb + Cr)/4))
    R, B = Cr + G, Cb + G
    return (R, G, B)

## Reversible Color Transform (YCoCg)
def rgb2ycocg(img, YCoCg = np.array([[1, 2, 1], [2, 0, -2], [-1, 2, -1]])/4):
    return img@YCoCg.T

def ycocg2rgb(img, YCoCg = np.array([[1, 1, -1], [1, 0, 1], [1, -1, -1]])):
    return img@YCoCg.T

## A decorative fun... See: https://www.geeksforgeeks.org/decorators-in-python/
from time import time as TT
def ITT(f):
	def time_warper_wrapper(*args, **kwargs):
		begin = TT() # from time import time as TT
		r = f(*args, **kwargs)
		end = TT()
		print(f'{f.__name__} evaluated in {end - begin:2.4}s')
		return r
	return time_warper_wrapper


