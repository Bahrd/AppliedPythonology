from scipy.ndimage import convolve
import numpy as np
import matplotlib.pyplot as plt

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

from random import randint; ri = lambda x: randint(0, x)

δ, ζ = 1, 0
eddie = _eddie(δ, ζ)
w, u = eddie.shape; v, z = image.shape

#δ, ζ = 0, 1
freddy = _eddie(ζ, δ)

## Freddys' random settlement locations
for _ in range(0x10):
   x, y = ri(v - w), ri(z - u)
   image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + freddy, 0, 1)

## Eddie's random location
x, y = ri(v - w), ri(z - u)
image[x:x + w, y:y + u] = np.clip(image[x:x + w, y:y + u] + eddie, 0, 1)

## Make the image a bit more realistic by incuring some noise
from numpy.random import poisson
λ = 0xffff # The more the merrier (try λ = 0x1 if you feel lucky... "Do you feel lucky, punk?")
image = poisson(image * λ)/λ

# Apply the filter to the image (a.k.a. find smiling Eddie!)
filtered_image = convolve(2*image - 1, 2*freddy - 1)/freddy.size

# Observe that we have done:
# 1. We've changed the range of the image and filter to [-1, 1] 
# 2. We've normalized the result by dividing by the size of the filter
# 3. These two tricks are known in all image processing kindergartens

skull_location = np.unravel_index(np.argmax(filtered_image, axis = None), filtered_image.shape)
# Pinpoint Eddie's location 
# It doesn't work all the time - even in the noise-free conditions... D'ya know why?
filtered_image[skull_location] = 0o2 # try 0o2 to spot poltergeists
# Display the original and filtered images
fig, axes = plt.subplots(1, 2, figsize = (10, 5))

for a, t, im in zip(axes.ravel(), ('Where\'s Eddie?', f'There he is {skull_location}!'), (image, filtered_image)):
   a.axis('off')
   a.set_title(t)
   a.imshow(im, cmap = plt.cm.copper)

plt.tight_layout()
plt.show()
