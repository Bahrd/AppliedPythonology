﻿from auxiliary import displayImages as DI
from interpolation import *
from random import randrange as RR
from numpy import array, empty
from math import sin, cos, pi
from sys import argv
## 2D rotation - the canonical version of NN, bi-linear and bi-qubic-based algorithms
#  If one wants a serious 2D: https://scipython.com/book/chapter-8-scipy/additional-examples/interpolation-of-an-image/

clp = lambda n, nmin, nmax: nmin if n < 0 else n if n < nmax else nmax - 1
## Turning a 2D image f(n, m) into 2D function f(x, y) using 'Π, ψ, or ϕ'
def f(x, y, img, λ, ε = 3):
    N, M = img.shape; xx, yy = int(x), int(y)
    fxy = 0
    for n in range(clp(xx - ε, 0, N), clp(xx + ε, 0, N)):
        for m in range(clp(yy - ε, 0, M), clp(yy + ε, 0, M)):
            fxy += λ(x - n) * λ(y - m) * img[n, m]
    return fxy


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
M = len(img); N = M << 0b1; out = empty((N, N)) 

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
        out[n, m] = f(x, y, img, ϕ)  

DI((img, out), ('Original', '{0}-rotated by {1}°'.format(ϕ.__name__, ϱ)), cmp = 'copper')
