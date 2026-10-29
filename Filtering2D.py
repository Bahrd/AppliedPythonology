from scipy.ndimage import convolve
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

δ, ζ = 1, 0
eddie, freddy = _eddie(δ, ζ), _eddie(ζ, δ)

w, u = eddie.shape; v, z = image.shape

## Freddys' random settlement locations
for _ in range(0x10):
   x, y = ri(v - w), ri(z - u)
   image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + freddy, 0, 1)

## Eddie's random location
x, y = ri(v - w), ri(z - u)
image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + eddie, 0, 1)

## Make the image a bit more 'realistic' by incurring some noise
λ = 0xffff # The more the merrier (try λ = 0x1 if really you feel lucky... And "do you feel lucky, punk?")
image = poisson(image * λ)/λ

# Apply the filter to the image (a.k.a. find the smiling Eddie!)
filtered_image = convolve(2*image - 1, 2*freddy - 1)/freddy.size

# Observe that we have done:
# 1. Changed the range of the image and of the filter to [-1, 1]
# 2. Normalized the result by dividing by the size of the filter
# These two tricks are known in all image processing kindergartens

skull_location = np.unravel_index(np.argmax(filtered_image, axis = None), filtered_image.shape)
# Pinpoint Eddie's location
# It doesn't work all the time - even in the noise-free conditions... D'ya know why?
filtered_image[skull_location] = 0o20 # Try 0o2 to see a few poltergeists (and 0o20 to hide them all)
# Display the original and filtered images
fig, axes = plt.subplots(1, 2, figsize = (10, 5))

for a, t, im in zip(axes.ravel(), ('Where\'s Eddie?', f'There he is {skull_location}!'), (image, filtered_image)):
   a.axis('off')
   a.set_title(t)
   a.imshow(im, cmap = plt.cm.copper)

plt.tight_layout()
plt.show()
