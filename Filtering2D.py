## https://youtu.be/8unEo4tdVVQ - hardly a pumpkin field, but still...
from scipy.ndimage import convolve, correlate
from numpy.random import poisson
from random import randint

import matplotlib.pyplot as plt
import numpy as np

## Create an empty pumpkin field (a.k.a. a 2D image) and a pumpkin twin template (a.k.a. 2D filters)
image = np.zeros((128, 128))
pumpkin = lambda δ, ζ: np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                                [0, δ, 1, 0, 0, 1, δ, δ, 1, 0, 0],
                                [0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
                                [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
                                [0, 0, 1, ζ, 1, 1, 1, ζ, 1, 0, 0],
                                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 1, δ, δ, δ, 1, 0, 0, 0],
                                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

ri = lambda n: randint(0, n)

δ, ζ = 0, 1 # δ = 0, ζ = 1 for the grinning Freddy and the flabbergasted Eddie(s)
eddie, freddy = pumpkin(δ, ζ), pumpkin(ζ, δ)

w, u = eddie.shape; v, z = image.shape

## Eddies' random settlement locations...
for _ in range(0x10):
   x, y = ri(v - w), ri(z - u)
   image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + eddie, 0, 1)

# ... and a Freddy's random location
x, y = ri(v - w), ri(z - u)
image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + freddy, 0, 1)

## Make the image a bit more 'realistic' by inserting some "photon noise"
λ = 0x10 # The more the merrier (try λ = 0x1 if you really feel lucky... But "do you feel lucky, punk?").
        # If not (I don't!), set λ = 0x100 (or more) to rescue these guys from drowning in the sea of noise...
image = poisson(image * λ)/λ

## Finding the smiling Freddy! (a.k.a. filtering the image)
#  Observe that in the passing (the parameters) we have:
#  1. changed the range of the image and of the filter (from [0, 1] to [-1, 1]), and
#  2. normalized the filter (but not the image - that would've made the example even less realistic!)
#  These two tricks are known in any image processing kindergarten I have ever been to...

## To 'correlate' or to 'convolve' - pick your poison!
filtered_image = correlate(2*image - 1, (2*freddy - 1)/freddy.size, mode = 'constant', cval = -1)
## Pinpointing Freddy's location & the Ground truth location (the center of the pumpkin template)
pumpkin_location, gt_location = np.unravel_index(np.argmax(filtered_image, axis = None), filtered_image.shape), (x + w//2, y + u//2)

#  The scheme can fail from time to time - even in the noise-free conditions (D'ya know why?).
#  Thus, we are only kinda sure we have found a pumpkin(ish blot)...

# Pick (0o2, 0o4) to face a few poltergeists or (0o20, 0o40) to "Copperfield" them all
filtered_image[pumpkin_location], filtered_image[gt_location]  = 0o10, 0o20

## Display both images, the original and the filtered one
fig, axes = plt.subplots(1, 2, figsize = (10, 5))
fig.set_facecolor('black')
for a, t, im in zip(axes.ravel(), ('Where\'s Freddy?', f'There he is! [@{pumpkin_location} vs. @{gt_location}]'), (image, filtered_image)):
   a.axis('off')
   a.set_title(t, color = 'xkcd:pumpkin', fontsize = 0o10, loc = 'center', pad = 0b10)
   a.imshow(im, cmap = plt.cm.copper)
plt.tight_layout()
plt.show()
