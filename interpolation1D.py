import numpy as np; import matplotlib.pyplot as plt
from interpolation import Π, ψ, ϕ, ξ, interpolate
from auxiliary import displayPlots

#Some shortcuts...
κ = 'ψ, ϕ, Π, ξ'
ΣΛ, Λ, ΛΛ = interpolate, list(eval(κ)), κ.split(',')  

## 1D Examples 
#  A staple one...
Fn = [0, 0, 0, 1, 0, 0, 0]
Fx = np.array(ΣΛ(N = 1024, fn = Fn, Λ = Λ)).T
plt.plot(Fx); plt.title(κ); plt.show(); displayPlots(Fx.T, ΛΛ)

#  User-defined...
while True:
    rawFn = input("Samples: ").split()
    if len(rawFn) > 1:
        N = int(input("Output size (N): ")); Fn = [float(n) for n in rawFn]        
        # 2in1: computations and presentation 
        displayPlots(ΣΛ(Fn, N), ΛΛ)        
    else:
        break