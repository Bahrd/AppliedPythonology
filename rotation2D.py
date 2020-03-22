from auxiliary import displayImages as DI
from interpolation import *
from random import randrange as RR
from numpy import array, empty
from math import sin, cos, pi
from sys import argv
## 2D rotation - the canonical version of the NN, bi-linear and bi-qubic-based algorithms
#  If one wants a serious 2D: https://scipython.com/book/chapter-8-scipy/additional-examples/interpolation-of-an-image/

clp = lambda n, nmax, nmin = 0: nmin if n < 0 else n if n < nmax else nmax - 1
## Turning a 2D image f(n, m) into a 2D function f(x, y) - using 'Π, ψ, or ϕ'
def f(x, y, img, λ = ϕ, Δ = 3):
    N, M = img.shape; xx, yy = int(x), int(y)
    n = np.arange(clp(xx - Δ, N), clp(xx + Δ, N))
    m = np.arange(clp(yy - Δ, M), clp(yy + Δ, M))

    Λx, Λy = λ(x - n), λ(y - m) 
    Λxy = np.tensordot(Λx.T, Λy, axes = 0)

    return np.tensordot(Λxy, img[clp(xx - Δ, N):clp(xx + Δ, N), clp(yy - Δ, M):clp(yy + Δ, M)])
    ## A loop-in-loop version...
    #fxy = 0.0
    #for n in range(clp(xx - Δ, N), clp(xx + Δ, N)):
    #    for m in range(clp(yy - Δ, M), clp(yy + Δ, M)):
    #        fxy += λ(x - n) * λ(y - m) * img[n, m]
    #return fxy

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
M = len(img); N = M << 0b100; out = empty((N, N)) 

# Setting a rotation angle α
α = int(argv[1]) if len(argv) == 2 else RR(-180, 180) #°
ϱ = α # an auxiliary variable
α *= pi/180.0

# Rotation of the vector ϑ = [x, y].T, w.r.t. OXY and through an angle α
OXY, Rα = array([M/2, M/2]), array([[cos(α), -sin(α)], 
                                    [sin(α),  cos(α)]]) # '+' clockwise
for n in range(N):
    for m in range(N):
        ϑ = array([n/N, m/N]) * M - OXY
        x, y = Rα @ ϑ + OXY
        out[n, m] = f(x, y, img)  

DI((img, out), ('Original', '{0}-rotated by {1}°'.format(ϕ.__name__, ϱ)), cmp = 'copper')
