import numpy as np; import matplotlib.pyplot as plt
# Some interpolating functions, Π(x), ψ(x) and ϕ(x)
def Π(x, l = -1/2, r = 1/2):  # window, rectangular function
    return (x >= l) * (x < r)
def ψ(x):   # hat, tent, triangular function
    return (1 - abs(x)) * (abs(x) < 1)
def ϕ(x):   # Keys' cubic interpolating function
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
        plt.title("Interpolations from {0} to {1} samples"
                  .format(len(Fn), len(Fx)))
        plt.show()
    else:
        break
### Outtakes
## An actual interpolation Φ: X ➞ Y 
#X = [0, 0, 1, 1, 1, 1, 1, 0, 1, 2, 3, 2, 1, 0, 1, 4, 9, 4, 1, 0]
#Y = [[Φ(x, X, λ) for λ in [ϕ, ψ, Π]] for x in np.linspace(0, len(X), 128)]
                                                    
## Presentation Y
#plt.plot(Y); 
#plt.title("Interpolations from {0} to {1} pixels".format(len(X), len(Y))); 
#plt.show()
## for-loop versions
## An interpolation routine Λ: f(n) ➞ f(x)
#def Λ(x, f, λ):
#   y = 0.0; 
#   for n in range(len(I)):
#       y += I[n] * ff(x - n)
#       return y
## Interpolation: X ➞ Y
## An actual interpolation: X ➞ Y using ϕ or ψ, or an "ad hoc": lambda x: (abs(x) < 1) * 3/4*(1 - x**2)
# Y = np.empty(45)
# for n in range(len(Y)):
#     x = len(X)/len(Y) * n           
#     Y[n] = Λ(x, X, ϕ)
