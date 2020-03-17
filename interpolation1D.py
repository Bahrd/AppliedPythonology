import numpy as np; import matplotlib.pyplot as plt
## Some interpolating functions, Π(x), ψ(x) and ϕ(x) or... 
#  whatchamacallit this thingamajig...

# The window/rectangular and the hat/tent/triangular (yet anonymous!) function
Π, ψ =  lambda x, l = -.5, r = .5: (x >= l) * (x < r), lambda x: (1 - abs(x)) * (abs(x) < 1)
# The Keys' cubic interpolating function (b'cause: https://realpython.com/python-lambda/#syntax)
def ϕ(x):                       
    x, a = abs(x), -0.5
    return (((a + 2) * x**3 - (a + 3) * x**2 + 1)             * Π(x, 0, 1) 
           + (     a * x**3 -     5*a * x**2 + 8*a * x - 4*a) * Π(x, 0, 2) * (1 - Π(x, 0, 1)))

# An interpolation routine Λ: f(n) ➞ f(x) using ϕ, ψ or Π, 
def Φ(x, f, λ):
    n = np.arange(len(f))
    Λ = λ(x - n)                         
    return Λ @ f

# An actual interpolation Φ: Fn ➞ Fx 
def interpolate(fn, N, Λ = [Π, ψ, ϕ]):
    X = np.linspace(0, len(fn), N)
    return [[Φ(x, fn, λ) for λ in Λ] for x in X] 

## 1D Examples 
#  A staple one...
Fn = [0, 0, 0, 1, 0, 0, 0, 0]; Fx = interpolate(N = 1024, fn = Fn)
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