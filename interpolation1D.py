import numpy as np; import matplotlib.pyplot as plt
from interpolation import Π, Λ, ϕ, ξ, interpolate
from auxiliary import displayPlots

#Some shortcuts...
Σφ, κ = interpolate, 'Π, Λ, ϕ, ξ'
φ, φφ = list(eval(κ)), κ.split(',')  

## 1D Examples 
#  A staple one...
Fn = [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Fx = np.array(Σφ(N = 1024, fn = Fn, φ = φ)).T

displayPlots(Fx.T, φφ); plt.plot(Fx); plt.title(κ); plt.show()

#  User-defined...
while True:
    rawFn = input("Samples: ").split()
    if len(rawFn) > 1:
        N = int(input("Output size (N): ")); Fn = [float(n) for n in rawFn]        
        # 2in1: computations and presentation 
        displayPlots(Σφ(Fn, N), φφ)        
    else:
        break