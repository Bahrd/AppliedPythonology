''' Several interpolating functions, Π(x), Λ(x) and ϕ(x) or sinc(x) for that matter...

Whatchamacallit this thingamajig: 
* The window/rectangular and the hat/tent/triangular and Keys & sinc (thus not anonymous!) functions. 
* The Keys' cubic interpolating function (b'cause: https://realpython.com/python-lambda/#syntax)'''

def Π(x, l = -.5, r = .5): return (x >= l) * (x < r)
def Λ(x): return (1 - abs(x)) * (abs(x) < 1)
def ϕ(x): 
    x, α = abs(x), -.5
    return (((α + 2) * x**3 - (α + 3) * x**2 + 1)             * Π(x, 0, 1) 
           + (     α * x**3 -     5*α * x**2 + 8*α * x - 4*α) * Π(x, 0, 2) * (1 - Π(x, 0, 1)))

from numpy import sin, ones_like, pi as π
def ξ(x, m = π): 
    x = x * m; sinc = ones_like(x)
    sinc[x != 0] = sin(x[x != 0])/(x[x != 0])
    return sinc # sinc for syncope?
# Or, simply...
#from numpy import sinc

from numpy import arange, linspace
# An interpolation routine: f(n) ➞ f(x) using φ = Π, Λ, ϕ or ξ 
def Φ(x, f, φ):
    n = arange(len(f))
    ψ = φ(x - n)                         
    return ψ @ f

# An actual interpolation Φ: Fn ➞ Fx 
def interpolate(fn, N, φ = [Π, Λ, ϕ, ξ]):
    X = linspace(0, len(fn), N)
    return [[Φ(x, fn, ψ) for x in X] for ψ in φ] if type(φ) is list else [Φ(x, fn, φ) for x in X]

#  A source image...
from random import randrange as RR
from numpy import array

ζ = RR(0b10); ξ = ζ ^ 0b1 
eddie = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0], 
               [0, 0, 0, 1, 0, 0, 1, ξ, ξ, 1, 0, 0], 
               [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0], 
               [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0], 
               [0, 0, 0, 1, ζ, 1, 1, 1, ζ, 1, 0, 0], 
               [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
               [0, 0, 0, 0, 1, ξ, ξ, ξ, 1, 0, 0, 0], 
               [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
