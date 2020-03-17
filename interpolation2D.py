from auxiliary import Π, ψ, ϕ, interpolate, displayImages
import numpy as np; import matplotlib.pyplot as plt

## If one wants to go 2D: https://scipython.com/book/chapter-8-scipy/additional-examples/interpolation-of-an-image/
# In principle, a 2D interpolation, for a separable interpolation function, that is,
# the function that is a product of 1D interpolation functions, 
#                      ϕ(x, y) = ϕ(x)ϕ(y)
# can be implemented as a successive application of the 1D interpolation 
# procedure to each row and then to each column of the image.

# Some shortcuts...
ξ, Λ = interpolate, [ϕ] #ψ, ϕ, Π
# A source image... 
image = np.array([[0, 0, 0, 1, 1, 0, 0, 0], 
                  [0, 0, 1, 1, 1, 1, 0, 0], 
                  [0, 1, 0, 1, 1, 0, 1, 0], 
                  [1, 1, 0, 1, 1, 0, 1, 1], 
                  [1, 1, 1, 0, 0, 1, 1, 1], 
                  [0, 1, 0, 0, 0, 0, 1, 0], 
                  [0, 0, 1, 1, 1, 1, 0, 0], 
                  [0, 0, 0, 1, 1, 0, 0, 0]])

M = len(image); N = 13
scaled_image = np.zeros((N, N))

# 2D interpolation - as simple as that?! (yes, only when M ≤ N)
for m in range(M):
    scaled_image[m, :] = np.array(ξ(image[m, :], N, Λ = Λ)).flat
for n in range(N):
    scaled_image[:, n] = np.array(ξ(scaled_image[:M, n], N, Λ = Λ)).flat

displayImages((image, scaled_image), ('Original', 'Scaled'))