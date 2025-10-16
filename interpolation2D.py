from interpolation import Π, Λ, ϕ, ξ, interpolate as ΣΣ, eddie, RR
from matplotlib.pyplot import plot, show, subplots
from auxiliary import displayImages as di
from random import choice
from numpy import zeros, array
from sys import argv

''' In principle, a 2D interpolation, for a separable interpolation function, that is,
the function that is a product of 1D interpolation ones,
                     ψ(x, y) = ψ(x)ψ(y)  # Π, Λ, ϕ, ξ
can be implemented as a successive application of the 1D interpolation
procedure to each row and then to each column of the image. '''

## Setting:
#  A source image...
img = eddie; M = len(img); N = eval(argv[1]) if len(argv) > 1 else M << 0b1 #13 #
# ... and some shortcuts.
את, nomina = lambda : choice([True, False]), argv[0b10] if len(argv) > 0b10 else ϕ.__name__
ψ, Cu = eval(nomina), 'copper'

##2D interpolation - simple as that?! (yeah, but only when M ≤ N...)
# A loop-by-loop version...
if את():
    out = zeros((N, N))
    for m in range(M):
        out[m, ...] = array(ΣΣ(img[m, ...], N, φ = ψ)).flat
    di((img, out), ('Original', f'{nomina}-scaled rows'), cmp = Cu, clip = False, grid = False)

    for n in range(N):
        out[..., n] = array(ΣΣ(out[:M, n], N, φ = ψ)).flat
    di((img, out), ('Original', f'{nomina}-scaled rows & columns'), cmp = Cu, clip = False, grid = False)
# ... and the more convoluted (snaky, sneaky'n'snacky) version
else:
    out = array([ΣΣ(img[m, ...], N, φ = ψ) for m in range(M)]).reshape(M, N)
    di((img, out), ('Original', f'{nomina}-scaled rows II'), cmp = Cu, clip = False, grid = False)

    out = array([ΣΣ(out[..., n], N, φ = ψ) for n in range(N)]).reshape(N, N).T
    di((img, out), ('Original', f'{nomina}-scaled rows & columns II'), cmp = Cu, clip = False, grid = False)

## A pretty scary stuff...
#  "Let's put a smile on that face." https://www.imdb.com/title/tt0468569/quotes/?item=qt1148950
#  (Or rather yet another aliasing-related effect ;)
if 0b1:
    # Troughs and crests
    _ = plot(out[N >> 0b1, ...], 'ro-'), show()
    out[out < 0.0] = 1.0; out[out > 1.0] = 0.0
    di((img, out), ('Original', f'{nomina}-scaled'), cmp = Cu, title = '"Let\'s put a smile on that face."', clip = False, grid = False)

## (In)Deterministic users' enjoyment:
#  "python .\interpolation2D.py 42 'lambda x: Λ(x + RR(2) * RR(9)/12)'"