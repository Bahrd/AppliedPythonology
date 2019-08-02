import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt, isnan

## An approximate Mandelbrot set function (accuracy grows with ν)
#       M = {ω ∈ Ω: mandelbrot(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
def mandelbrot(c, ν = 0x40):
    ω = complex() 
    for _ in range(ν):
        ω = pwr(ω, 2) + c
    return abs(ω) < 2       

## Presentation
# Rehearsal...
[N, M] = [0x200, 0x200]     # resolution
[X, Y], ε = [-1/2, 0], 3/2  # size
Ω = mt([[complex(n, m) for n in lnsp(X - ε, X + ε, N)] 
                       for m in lnsp(Y - ε, Y + ε, M)])
# ... and act!
M = mandelbrot(Ω)
plt.imshow(M, cmap = 'Blues')
plt.show()
