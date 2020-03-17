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
img = np.array([[0, 0, 0, 1, 1, 0, 0, 0], 
                [0, 0, 1, 1, 1, 1, 0, 0], 
                [0, 1, 0, 1, 1, 0, 1, 0], 
                [1, 1, 0, 1, 1, 0, 1, 1], 
                [1, 1, 1, 0, 0, 1, 1, 1], 
                [0, 1, 0, 0, 0, 0, 1, 0], 
                [0, 0, 1, 1, 1, 1, 0, 0], 
                [0, 0, 0, 1, 1, 0, 0, 0]])

M = len(img); N = 17


# 2D interpolation - simple as that?! (only when M ≤ N...)
## A loop-by-loop version
out = np.zeros((N, N))
for m in range(M):
    out[m, :] = np.array(ξ(img[m, :], N, Λ = Λ)).flat
for n in range(N):
    out[:, n] = np.array(ξ(out[:M, n], N, Λ = Λ)).flat

displayImages((img, out), ('Original', 'Re-scaled'), cmp = 'copper')

## with or without transposition
#out = np.block([np.array(ξ(img[ m, :], N, Λ = Λ)) for m in range(M)]).T
#out = np.block([np.array(ξ(out[:M, n], N, Λ = Λ)) for n in range(N)])
#
#out = np.block([np.array(ξ(img[m, :], N, Λ = Λ)) for m in range(M)])
#out = np.block([np.array(ξ(out[n,:M], N, Λ = Λ)) for n in range(N)])
