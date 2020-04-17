from interpolation import Π, ψ, ϕ, ξ, eddie
from auxiliary import displayImages as DI
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
def fl(img, x, y, λ = ϕ, Δ = 3):
    N, M = img.shape; xx, yy = int(x), int(y)

    fxy = 0.0
    for n in range(*rclp(xx - Δ, xx + Δ, N)):
        for m in range(*rclp(yy - Δ, yy + Δ, M)):
            fxy += λ(x - n) * λ(y - m) * img[n, m]
    return fxy
# ... and a quicker'n'cleaner (explicit-loop-free) one
def f(img, x, y, λ = ϕ, Δ = 3):
    N, M = img.shape; xx, yy = int(x), int(y)
    n, m = A(*rclp(xx - Δ, xx + Δ, N)), A(*rclp(yy - Δ, yy + Δ, M))

    Λx, Λy = λ(x - n), λ(y - m) 
    Λxy = tendot(Λx.T, Λy, axes = 0)

    img = img[clp(xx - Δ, N):clp(xx + Δ, N), clp(yy - Δ, M):clp(yy + Δ, M)]
    return tendot(Λxy, img)

## Setting...
#  A rotation angle α...
ϱ = eval(argv[1]) if len(argv) > 1 else RR(-180, 180) #°
α, Cu = ϱ * pi/180.0, 'copper' # Main and auxiliary variables

#  A source image... 
img = eddie; M = len(img); N = eval(argv[2]) if len(argv) > 2 else M << 0b1
out = empty((N, N)) 
# ... and rotation of ϑ = [x, y].T, w.r.t. OXY and through that angle 
OXY, Rα = array([M/2, M/2]), array([[cos(α), -sin(α)], 
                                    [sin(α),  cos(α)]]) # turns clockwise when α > 0

# ... and an interpoland...:) Π, ψ, ϕ, or ξ, "or else..."
λλ = argv[3] if len(argv) > 3 else ϕ.__name__; λ = eval(λλ) 

f = f if 0x0 else fl
if 0b0: 
    # Omloop Het...
    for n in range(N):
        for m in range(N):
            ϑ = array([n/N, m/N]) * M - OXY
            x, y = Rα @ ϑ + OXY
            out[n, m] = f(img, x, y, λ) # cf. rotationNN.py's '... = img[x, y]'
else:   
    # A harder-coded version (but a tad faster, right?)
    out = [[f(img, *(OXY + Rα @ (array([n/N, m/N]) * M - OXY)), λ) 
                                                 for m in range(N)] 
                                                 for n in range(N)]

DI((img, out), ('Original', '{0}-rotated by {1}°'.format(λλ, ϱ)), cmp = Cu)

## Random users' fun: "python .\rotation2D.py '-RR(44)' '42 + RR(7) - 6' 'lambda x: ψ(x + RR(9)/12)'"
# 44:   "A imię jego..." A. M. Dz. III 
# 42:   The Deep Thought's answer ( = 7 * 6)
# 9/12: A quote of Heidegger/Wittgenstein