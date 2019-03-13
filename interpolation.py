import numpy as np; import matplotlib.pyplot as plt
## Some interpolating functions, Π(x), ψ(x) and ϕ(x) or whatchamacallit this thingamajig..

def Π(x, l = -1/2, r = 1/2):    # The window/rectangular function
    return (x >= l) * (x < r)
def ψ(x):                       # The hat/tent/triangular function
    return (1 - abs(x)) * (abs(x) < 1)
def ϕ(x):                       # The Keys' cubic interpolating function
    return ((    4/3 * abs(x**3) - 7/3 * x**2 + 1)                                         * Π(x, -1, 1)
            + (-7/12 * abs(x**3) +   3 * x**2 - 59/12 * abs(x) + 15/6) * (1 - Π(x, -1, 1)) * Π(x, -2, 2)  
            + ( 1/12 * abs(x**3) - 2/3 * x**2 + 21/12 * abs(x) -  3/2) * (1 - Π(x, -2, 2)) * Π(x, -3, 3)) 
# An interpolation routine Λ: f(n) ➞ f(x) using ϕ, ψ or Π, or an "ad hoc"
def Φ(x, f, λ):                     # lambda x: 3/4*(abs(x) < 1)*(1 - x**2)
    n = np.arange(len(f))
    Λ = λ(x - n)                         
    return Λ @ f                       
# An actual interpolation Φ: Fn ➞ Fx 
def interpolate(fn, N, Λ = [Π, ψ, ϕ]):
    X = np.linspace(0, len(fn), N)
    return [[Φ(x, fn, λ) for λ in Λ] for x in X] 

## Examples
#  A staple one...
Fn = [0, 0, 1, 1, -1, -1, 0]; Fx = interpolate(N = 128, fn = Fn)
plt.plot(Fx); plt.show()
#  User-defined...
while True:
    rawFn = input("Samples: ").split()
    if len(rawFn) > 1:
        N = int(input("Output size (N): ")) 
        Fn = [float(n) for n in rawFn]; Fx = interpolate(Fn, N)
        # Presentation 
        plt.plot(Fx)
        plt.title("Interpolations from {0} to {1} samples".format(len(Fn), len(Fx)))
        plt.show()
    else:
        break