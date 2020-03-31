from matplotlib.pyplot import imshow, show, title
from auxiliary import displayImages as DI
from numpy import linspace as lnsp, power as pwr, mat as mt, isnan, log, any, e, array

## An approximate Mandelbrot set function (accuracy grows with ν)
#       M = {ω ∈ Ω: mandelbrot(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
def mandelbrot(c, ν = 0x42):
    ω = complex() 
    for _ in range(ν):
        ω = pwr(ω, 2) + c
        # Face-lifting an old set...
        ω[any([isnan(ω), abs(ω) > 0x2], axis = 0)] = 0x2
    return abs(ω) < 2.0

## And a picturesque version  
def mandelbrother(c, ν = 0x42):
    ω = complex() 
    for _ in range(ν):
        ω = pwr(ω, 2) + c
        # Face-lifting an old set...
        ω[any([isnan(ω), abs(ω) > 0xfffffffff], axis = 0)] = 0x0
    return abs(ω)


## Presentation
# Rehearsal...
[N, M] = [0x200, 0x200]     # resolution
[X, Y], ε = [-1/2, 0], 3/2  # size
Ω = mt([[complex(n, m) for n in lnsp(X - ε, X + ε, N)] for m in lnsp(Y - ε, Y + ε, M)])
# ... and act!
while True:
    rawN = input("Iterations [N = 0b110] = ")
    N = int(rawN) if len(rawN) > 0 else 0x6 # '0x6' and '0x42' are rather arbitrarily selected
    M = mandelbrot(Ω)                       # to make the compound image look nice(r)...
    MM = mandelbrother(Ω, N) + mandelbrother(Ω)
    MM = log(e + MM)
    DI((M, MM), ('Mandelbrot...', 'Mandelbrothers...'), cmp = 'copper')
