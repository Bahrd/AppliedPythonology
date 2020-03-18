import numpy as np; import matplotlib.pyplot as plt
from interpolation import Π, ψ, ϕ, interpolate

#Some shortcuts...
Σ, Λ = interpolate, [ψ, ϕ, Π] #[ϕ] #

## 1D Examples 
#  A staple one...
Fn = [0, 0, 0, 1, 0, 0, 0]
for Fx in zip(*Σ(N = 1024, fn = Fn, Λ = Λ)):
    plt.plot(Fx) 
plt.show()
#  User-defined...
while True:
    rawFn = input("Samples: ").split()
    if len(rawFn) > 1:
        N = int(input("Output size (N): ")) 
        Fn = [float(n) for n in rawFn]
        # Presentation 
        for Fx in zip(*Σ(Fn, N)):
            plt.plot(Fx)
        plt.title("Interpolations from {0} to {1} samples".format(len(Fn), len(Fx)))
        plt.show()
    else:
        break

# cd C:\Users\Przem\source\repos\Bahrd\AppliedPythonology
# python .\interpolation1D.py