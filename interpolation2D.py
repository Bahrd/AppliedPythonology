from interpolation import Π, ψ, ϕ, ξ, interpolate as intrpl, eddie
from matplotlib.pyplot import plot, show
from auxiliary import displayImages as DI
from random import randrange as RR
from numpy import zeros, array
from sys import argv

## In principle, a 2D interpolation, for a separable interpolation function, that is,
#  the function that is a product of 1D interpolation functions, 
#                      ϕ(x, y) = ϕ(x)ϕ(y)  # Π, ψ, ϕ, ξ 
#  can be implemented as a successive application of the 1D interpolation 
#  procedure to each row and then to each column of the image.

## Setting:
#  A source image... 
img = eddie; M = len(img); N = int(argv[1]) if len(argv) > 1 else M << 0b1 #13 #
# ... and some shortcuts.
את, ΣΣ, ΛΛ = lambda : RR(0b10), intrpl, argv[2] if len(argv) > 2 else ϕ.__name__ 
Λ, Cu = eval(ΛΛ), 'copper'

##2D interpolation - simple as that?! (yeap, but only when M ≤ N...)
# A loop-by-loop version...
if את():
    out = zeros((N, N)) 
    for m in range(M):
        out[m, ...] = array(ΣΣ(img[m, ...], N, Λ = Λ)).flat
    DI((img, out), ('Original', '{0}-scaled rows'.format(ΛΛ)), cmp = Cu)

    for n in range(N):
        out[..., n] = array(ΣΣ(out[:M, n], N, Λ = Λ)).flat
    DI((img, out), ('Original', '{0}-scaled rows & columns'.format(ΛΛ)), cmp = Cu)
# ... and the more convoluted (snaky, sneaky'n'snacky) version
else:
    out = array([ΣΣ(img[m, ...], N, Λ = Λ) for m in range(M)]).reshape(M, N)
    DI((img, out), ('Original', '{0}-scaled rows'.format(ΛΛ)), cmp = Cu)

    out = array([ΣΣ(out[..., n], N, Λ = Λ) for n in range(N)]).reshape(N, N).T
    DI((img, out), ('Original', '{0}-scaled rows & columns'.format(ΛΛ)), cmp = Cu)

## A pretty scary stuff... Will you dare? 
#  (Or rather yet another aliasing-related effect ;)
if 0b1: 
    # Troughs and crests
    plot(out[N >> 0b1, ...], 'ro-'); show()
    out[out < 0.0] = 1.0; out[out > 1.0] = 0.0
    DI((img, out), ('Original', '{0}-scaled'.format(ΛΛ)), cmp = Cu)

## (In)Deterministic users' enjoyment:
#  "python .\interpolation2D.py 42 'lambda x: ψ(x + RR(2) * RR(9)/12)'"