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
        ω[any([isnan(ω), abs(ω) > 0xffffff], axis = 0)] = 0xff
    # A picturesque version   A more set-like one...
    return log(e + abs(ω))    # return abs(ω) < 2.0

## Presentation
# Rehearsal...
[N, M] = [0x200, 0x200]     # resolution
[X, Y], ε = [-1/2, 0], 3/2  # size
Ω = mt([[complex(n, m) for n in lnsp(X - ε, X + ε, N)] 
                       for m in lnsp(Y - ε, Y + ε, M)])
# ... and act!
M = mandelbrot(Ω)
imshow(M, cmap = 'copper'); title('Mandelbrot set'); show()
