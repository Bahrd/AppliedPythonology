import numpy as np; import matplotlib.pyplot as plt
from auxiliary import displayPlots
from interpolation import Π, Λ, ϕ, ξ, interpolate

# Compare with: https://en.wikipedia.org/wiki/Lagrange_polynomial#Definition

#Some shortcuts...
Σψ, κ = interpolate, 'Π, Λ, ϕ, ξ'
ψ, ψψ = list(eval(κ)), κ.split(',')  

## 1D Examples 
#  A staple one...
Fn = [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Fx = np.array(Σψ(N = 0o2000, fn = Fn, ϕ = ψ)).T         # Octoplus!

displayPlots(Fx.T, ψψ); plt.plot(Fx); plt.title(κ); plt.show()

#  User-defined...: 
sumup = lambda n, step = 2: sum(range(1, n, step))
# 0 0 0 sumup(1) sumup(3) sumup(5) sumup(7) sumup(9)  0 0 0

while True:
    rawFn = input("Samples: ").split()
    if rawFn != []:
        N = int(input("Output size (N): ")); Fn = [eval(n) for n in rawFn]        
        # 2in1: computations and presentation 
        displayPlots(Σψ(Fn, N), ψψ)        
    else:
        break