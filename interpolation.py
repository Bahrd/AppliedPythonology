import numpy as np; import matplotlib.pyplot as plt
## Some interpolating functions, Π(x), ψ(x) and ϕ(x) or... 
#  whatchamacallit this thingamajig...
def Π(x, l = -1/2, r = 1/2):    # The window/rectangular function
    return (x >= l) * (x < r)
def ψ(x):                       # The hat/tent/triangular function
    x = abs(x)
    return (1 - x) * (x < 1)
def ϕ(x):                       # The Keys' cubic interpolating function
    x, a = abs(x), -0.5
    return (((a + 2) * x**3 - (a + 3) * x**2 + 1)             * Π(x, 0, 1) 
           + (     a * x**3 -     5*a * x**2 + 8*a * x - 4*a) * Π(x, 0, 2) * (1 - Π(x, 0, 1)))

# An interpolation routine Λ: f(n) ➞ f(x) using ϕ, ψ or Π, 
# or an 'ad hoc/inline' function 'lambda x: f(x)'
def Φ(x, f, λ):
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