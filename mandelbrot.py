from matplotlib.pyplot import imshow, show, title
from numpy import linspace as lnsp, power as pwr, mat as mt, isnan, log, any, e

## An approximate Mandelbrot set function (accuracy grows with ν)
#       M = {ω ∈ Ω: mandelbrot(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
def mandelbrot(c, ν = 0x40):
    ω = complex() 
    for _ in range(ν):
        ω = pwr(ω, 2) + c
        # Face-lifting of an old set...
        ω[any([isnan(ω), abs(ω) > 0xfffffffff], axis = 0)] = 0x0
    # A picturesque version   And a more set-like one...
    return abs(ω)             # return abs(ω) < 2.0

## Presentation
# Rehearsal...
[N, M] = [0x200, 0x200]     # resolution
[X, Y], ε = [-1/2, 0], 3/2  # size
Ω = mt([[complex(n, m) for n in lnsp(X - ε, X + ε, N)] for m in lnsp(Y - ε, Y + ε, M)])
# ... and act!
while True:
    rawN = input("Iterations: ")
    N = int(rawN) if len(rawN) > 0 else 0x6             # '0x6' and '0x42' are rather arbitrarily selected
    M = log(e + mandelbrot(Ω, N) + mandelbrot(Ω, 0x42)) # to make the compound image look nice(r)...
    imshow(M, cmap = 'copper'); title('Mandelbrot set'); show()
