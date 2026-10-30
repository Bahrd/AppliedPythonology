from scipy.ndimage import convolve, correlate
from numpy.random import poisson
from random import randint

import matplotlib.pyplot as plt
import numpy as np

# Load an example image
image = np.zeros((128, 128))
_eddie = lambda δ, ζ: np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

ri = lambda x: randint(0, x)

δ, ζ = 0, 1 # δ = 0, ζ = 1 for the smiling Freddy and scared Eddie(s)
eddie, freddy = _eddie(δ, ζ), _eddie(ζ, δ)

w, u = eddie.shape; v, z = image.shape

## Eddies' random settlement locations
for _ in range(0x10):
   x, y = ri(v - w), ri(z - u)
   image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + eddie, 0, 1)

## Freddy's random location
x, y = ri(v - w), ri(z - u)
image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + freddy, 0, 1)

## Make the image a bit more 'realistic' by incurring some noise
λ = 0xffff # The more the merrier (try λ = 0x1 if you really feel lucky... But "do you feel lucky, punk?")
           # If not (I don't!), set λ = 0xffff
image = poisson(image * λ)/λ

## Applying the filter to the image (a.k.a. finding the smiling Freddy!)
#  Observe that we have:
#  1. Changed the range of the image and of the filter (from [0, 1] to [-1, 1])
#  2. Normalized the filter (but not the image - that would've made the example even less realistic!)
#  These two tricks are known in all image processing kindergartens
image = 2*image - 1; freddy = (2*freddy - 1)/freddy.size

filtered_image = convolve(image, freddy, mode = 'constant', cval = -1) # 'convolve' or 'correlate' - that's the question!
freddy_location = np.unravel_index(np.argmax(filtered_image, axis = None), filtered_image.shape)
# Pinpoint Freddy's location
# It doesn't work all the time - even in the noise-free conditions... D'ya know why?
filtered_image[freddy_location] = 0o2 # Try 0o2 to see a few poltergeists (and 0o20 to hide them all)
# Display the original and filtered images
fig, axes = plt.subplots(1, 2, figsize = (10, 5))

for a, t, im in zip(axes.ravel(), ('Where\'s Freddy?', f'There he is {freddy_location}!'), (image, filtered_image)):
   a.axis('off')
   a.set_title(t)
   a.imshow(im, cmap = plt.cm.copper)

plt.tight_layout()
plt.show()
