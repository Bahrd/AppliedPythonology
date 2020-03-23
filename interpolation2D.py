from interpolation import Π, ψ, ϕ, interpolate
from auxiliary import displayImages
import matplotlib.pyplot as plt
from random import randrange
from numpy import block, zeros, array
from sys import argv

## In principle, a 2D interpolation, for a separable interpolation function, that is,
#  the function that is a product of 1D interpolation functions, 
#                      ϕ(x, y) = ϕ(x)ϕ(y)
#  can be implemented as a successive application of the 1D interpolation 
#  procedure to each row and then to each column of the image.

# Some shortcuts...
randbin, ΣΣ, Λ = lambda: randrange(0b10), interpolate, [ϕ] # Π, ψ, ϕ 
ΛΛ = Λ[0].__name__
# A source image... 
s = randbin(); g = s ^ 0b1; img = array([[0, 0, 0, 1, 1, 1, 0, 0, 0], 
                                            [0, 1, 1, 1, 1, 1, 1, 1, 0], 
                                            [0, 1, 0, 0, 1, g, g, 1, 0], 
                                            [1, 1, 0, 0, 1, 0, 0, 1, 1], 
                                            [1, 1, 1, 1, 0, 1, 1, 1, 1], 
                                            [0, 1, s, 1, 1, 1, s, 1, 0], 
                                            [0, 0, 1, 0, 0, 0, 1, 0, 0], 
                                            [0, 0, 1, g, g, g, 1, 0, 0], 
                                            [0, 0, 0, 1, 1, 1, 0, 0, 0]])
M = len(img); N = int(argv[1]) if len(argv) > 1 else M << 0b1 #13 #

##2D interpolation - simple as that?! (yeap, but only when M ≤ N...)
# A loop-by-loop version
out = zeros((N, N)) 
for m in range(M):
    out[m, ...] = block(ΣΣ(img[m, ...], N, Λ = Λ)).flat
displayImages((img, out), ('Original', '{0}-scaled rows'.format(ΛΛ)), cmp = 'copper')
for n in range(N):
    out[..., n] = block(ΣΣ(out[:M, n], N, Λ = Λ)).flat
displayImages((img, out), ('Original', '{0}-scaled rows & columns'.format(ΛΛ)), cmp = 'copper')

## A pretty scary stuff... Will you dare? 
#  (Or rather yet another aliasing-related effect ;)
if 0b1: 
    # Troughs and crests
    plt.plot(out[0b1101, ...], 'ro-'); plt.show()
    out[out < 0.0] = 1.0; out[out > 1.0] = 0.0
    displayImages((img, out), ('Original', '{0}-scaled'.format(ΛΛ)), cmp = 'copper')
