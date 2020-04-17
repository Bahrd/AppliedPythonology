## Some interpolating functions, Π(x), ψ(x) and ϕ(x) or sinc(x)... 
#  whatchamacallit this thingamajig...
# The window/rectangular and the hat/tent/triangular/sinc (not anonymous!) functions
def Π(x, l = -.5, r = .5): return (x >= l) * (x < r)
def ψ(x): return (1 - abs(x)) * (abs(x) < 1)
# The Keys' cubic interpolating function (b'cause: https://realpython.com/python-lambda/#syntax)
def ϕ(x): 
    x, a = abs(x), -.5
    return (((a + 2) * x**3 - (a + 3) * x**2 + 1)             * Π(x, 0, 1) 
           + (     a * x**3 -     5*a * x**2 + 8*a * x - 4*a) * Π(x, 0, 2) * (1 - Π(x, 0, 1)))

from numpy import sin, ones_like, pi
def ξ(x, m = pi): 
    x = x * m; ss = ones_like(x)
    ss[x != 0] = sin(x[x != 0])/(x[x != 0])
    return ss
# Or, simply...
#from numpy import sinc

from numpy import arange, linspace
# An interpolation routine Λ: f(n) ➞ f(x) using λ = ϕ, ψ or Π, ξ 
def Φ(x, f, λ):
    n = arange(len(f))
    Λ = λ(x - n)                         
    return Λ @ f

# An actual interpolation Φ: Fn ➞ Fx 
def interpolate(fn, N, Λ = [Π, ψ, ϕ, ξ]):
    X = linspace(0, len(fn), N)
    return [[Φ(x, fn, λ) for x in X] for λ in Λ] if type(Λ) is list else [Φ(x, fn, Λ) for x in X]

#  A source image...
from random import randrange as RR
from numpy import array

s = RR(0b10); g = s ^ 0b1
eddie = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
