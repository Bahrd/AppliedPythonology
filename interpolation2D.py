from interpolation import Π, ψ, ϕ, interpolate
from auxiliary import displayImages
import numpy as np; import matplotlib.pyplot as plt
from random import randrange

## In principle, a 2D interpolation, for a separable interpolation function, that is,
#  the function that is a product of 1D interpolation functions, 
#                      ϕ(x, y) = ϕ(x)ϕ(y)
#  can be implemented as a successive application of the 1D interpolation 
#  procedure to each row and then to each column of the image.
## If one wants a serious 2D: https://scipython.com/book/chapter-8-scipy/additional-examples/interpolation-of-an-image/

# Some shortcuts...
randbin, ΣΣ, Λ = lambda: randrange(0b10), interpolate, [ϕ] # Π, ψ, ϕ 
# A source image... 
s = randbin(); g = s ^ 0b1; img = np.array([[0, 0, 0, 1, 1, 1, 0, 0, 0], 
                [0, 1, 1, 1, 1, 1, 1, 1, 0], 
                [0, 1, 0, 0, 1, g, g, 1, 0], 
                [1, 1, 0, 0, 1, 0, 0, 1, 1], 
                [1, 1, 1, 1, 0, 1, 1, 1, 1], 
                [0, 1, s, 1, 1, 1, s, 1, 0], 
                [0, 0, 1, 0, 0, 0, 1, 0, 0], 
                [0, 0, 1, g, g, g, 1, 0, 0], 
                [0, 0, 0, 1, 1, 1, 0, 0, 0]])
M = len(img); N = M << 0b1 #13 #

# 2D interpolation - simple as that?! (only when M ≤ N...)
## A loop-by-loop version
out = np.zeros((N, N)) # out = np.empty((N, N)) for brave enough...
for m in range(M):
    out[m, :] = np.block(ΣΣ(img[m, :], N, Λ = Λ)).flat
displayImages((img, out), ('Original', 'Re-scaled rows'), cmp = 'copper')
for n in range(N):
    out[:, n] = np.block(ΣΣ(out[:M, n], N, Λ = Λ)).flat
displayImages((img, out), ('Original', 'Re-scaled rows & columns'), cmp = 'copper')

## A pretty scary stuff... (or rather yet another aliasing-related effect)
if 0b0: 
    # Troughs and crests
    plt.plot(out[0b1101, :], 'ro-'); plt.show()
    out[out < 0.0] = 1.0; out[out > 1.0] = 0.0
    displayImages((img, out), ('Original', 'Re-scaled'), cmp = 'copper')

# cd C:\Users\Przem\source\repos\Bahrd\AppliedPythonology
# python .\interpolation2D.py