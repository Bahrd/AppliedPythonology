from interpolation import Π, ψ, ϕ, interpolate
from auxiliary import displayImages
import numpy as np; import matplotlib.pyplot as plt
from random import randrange as RA

## In principle, a 2D interpolation, for a separable interpolation function, that is,
#  the function that is a product of 1D interpolation functions, 
#                      ϕ(x, y) = ϕ(x)ϕ(y)
#  can be implemented as a successive application of the 1D interpolation 
#  procedure to each row and then to each column of the image.
## If one wants a serious 2D: https://scipython.com/book/chapter-8-scipy/additional-examples/interpolation-of-an-image/

# Some shortcuts...
ΣΣ, Λ = interpolate, [ϕ] # Π, ψ, ϕ
# A source image... 
s, g = (0x1, 0x0) if RA(2) else (0x0, 0x1)
img = np.array([[0, 0, 0, 1, 1, 1, 0, 0, 0], 
                [0, 1, 1, 1, 1, 1, 1, 1, 0], 
                [0, 1, 0, 0, 1, g, g, 1, 0], 
                [1, 1, 0, 0, 1, 0, 0, 1, 1], 
                [1, 1, 1, 1, 0, 1, 1, 1, 1], 
                [0, 1, s, 1, 1, 1, s, 1, 0], 
                [0, 0, 1, 0, 0, 0, 1, 0, 0], 
                [0, 0, 1, g, g, g, 1, 0, 0], 
                [0, 0, 0, 1, 1, 1, 0, 0, 0]])
M = len(img); N = M << 1 #13 #

# 2D interpolation - simple as that?! (only when M ≤ N...)
## A loop-by-loop version
out = np.zeros((N, N)) # out = np.empty((N, N)) if not used interactively...
for m in range(M):
    out[m, :] = np.block(ΣΣ(img[m, :], N, Λ = Λ)).flat
displayImages((img, out), ('Original', 'Re-scaled rows'), cmp = 'copper')
for n in range(N):
    out[:, n] = np.block(ΣΣ(out[:M, n], N, Λ = Λ)).flat
displayImages((img, out), ('Original', 'Re-scaled rows & columns'), cmp = 'copper')

## A pretty scary stuff... (or rather yet another aliasing-related effect)
if 0x0: 
    # Troughs and crests
    plt.plot(out[13, :], 'ro-'); plt.show()
    out[out < 0.0] = 1.0; out[out > 1.0] = 0.0
    displayImages((img, out), ('Original', 'Re-scaled'), cmp = 'copper')

# cd C:\Users\Przem\source\repos\Bahrd\AppliedPythonology
# python .\interpolation2D.py