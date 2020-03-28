from auxiliary import displayImages as DI
from interpolation import *
from random import randrange as RR
from numpy import array, empty, arange as A, tensordot as tendot
from math import sin, cos, pi
from sys import argv
## 2D rotation - the canonical version of the NN, bi-linear and bi-qubic-based algorithms
#  If one wants a serious 2D: https://scipython.com/book/chapter-8-scipy/additional-examples/interpolation-of-an-image/

clp = lambda n, nmax, nmin = 0: nmin if n < 0 else n if n < nmax else nmax - 1
rclp = lambda n, m, nmax: (clp(n, nmax), clp(m, nmax)) # range clipper

## Turning a 2D image f(n, m) into a 2D function f(x, y) - using 'Π, ψ, or ϕ'
# A not-so-quick-yet-dirty (loop-in-loop) version... 
# Since "premature optimization is the root of all evil"! 
# -- D. Knuth [http://wiki.c2.com/?PrematureOptimization]
def fl(x, y, img, λ = ϕ, Δ = 3):
    N, M = img.shape; xx, yy = int(x), int(y)

    fxy = 0.0
    for n in range(*rclp(xx - Δ, xx + Δ, N)):
        for m in range(*rclp(yy - Δ, yy + Δ, M)):
            fxy += λ(x - n) * λ(y - m) * img[n, m]
    return fxy
# ... and a quick'n'clean (loop-free) one
def f(x, y, img, λ = ϕ, Δ = 3):
    N, M = img.shape; xx, yy = int(x), int(y)
    n, m = A(*rclp(xx - Δ, xx + Δ, N)), A(*rclp(yy - Δ, yy + Δ, M))

    Λx, Λy = λ(x - n), λ(y - m) 
    Λxy = tendot(Λx.T, Λy, axes = 0)

    img = img[clp(xx - Δ, N):clp(xx + Δ, N), clp(yy - Δ, M):clp(yy + Δ, M)]
    return tendot(Λxy, img)

# A source image... (cf. './rotationNN.py')
s = RR(0b10); g = s ^ 0b1; img = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                                         [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 
                                         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0], 
                                         [0, 0, 0, 1, 0, 0, 1, g, g, 1, 0, 0], 
                                         [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0], 
                                         [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0], 
                                         [0, 0, 0, 1, s, 1, 1, 1, s, 1, 0, 0], 
                                         [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
                                         [0, 0, 0, 0, 1, g, g, g, 1, 0, 0, 0], 
                                         [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],])
M = len(img); N = int(argv[2]) if len(argv) == 3 else M << 0b1; out = empty((N, N)) 

# Setting a rotation angle α
α = int(argv[1]) if len(argv) > 1 else RR(-180, 180) #°
ϱ, Cu = α, 'copper' # Auxiliary variables
α *= pi/180.0

# Interpoland...:) Π, ψ, ϕ
λ = ψ; λλ = λ.__name__
# Rotation of the vector ϑ = [x, y].T, w.r.t. OXY and through an angle α
OXY, Rα = array([M/2, M/2]), array([[cos(α), -sin(α)], 
                                    [sin(α),  cos(α)]]) # turns clockwise when α > 0
f = f if 0x1 else fl
# Omloop Het...
if 0b0:
    for n in range(N):
        for m in range(N):
            ϑ = array([n/N, m/N]) * M - OXY
            x, y = Rα @ ϑ + OXY
            out[n, m] = f(x, y, img, λ)
    DI((img, out), ('Original', '{0}-rotated by {1}°'.format(λλ, ϱ)), cmp = Cu)
## A harder-coded version (but a tad faster, right?)
else:
    out = [[f(*(OXY + Rα @ (array([n/N, m/N]) * M - OXY)), img, λ) for m in range(N)] for n in range (N)]
    DI((img, out), ('Original', '{0}-rotated by {1}°'.format(λλ, ϱ)), cmp = Cu)
