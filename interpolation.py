## Some interpolating functions, Π(x), ψ(x) and ϕ(x) or... 
#  whatchamacallit this thingamajig...
# The window/rectangular and the hat/tent/triangular (not anonymous!) function
def Π(x, l = -.5, r = .5): return (x >= l) * (x < r)
def ψ(x): return (1 - abs(x)) * (abs(x) < 1)
# The Keys' cubic interpolating function (b'cause: https://realpython.com/python-lambda/#syntax)
def ϕ(x): 
    x, a = abs(x), -.5
    return (((a + 2) * x**3 - (a + 3) * x**2 + 1)             * Π(x, 0, 1) 
           + (     a * x**3 -     5*a * x**2 + 8*a * x - 4*a) * Π(x, 0, 2) * (1 - Π(x, 0, 1)))

import numpy as np
# An interpolation routine Λ: f(n) ➞ f(x) using λ = ϕ, ψ or Π, 
def Φ(x, f, λ):
    n = np.arange(len(f))
    Λ = λ(x - n)                         
    return Λ @ f

# An actual interpolation Φ: Fn ➞ Fx 
def interpolate(fn, N, Λ = [Π, ψ, ϕ]):
    X = np.linspace(0, len(fn), N)
    return [[Φ(x, fn, λ) for x in X] for λ in Λ] if type(Λ) is list else [Φ(x, fn, Λ) for x in X]