from auxiliary import displayImages as DI
from numpy import linspace as ls, power as pwr, mat as mt, log, e

## An approximate Mandelbrot set function (accuracy grows with ν)
#       M = {ω ∈ Ω: mandelbrot(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
#          https://www.youtube.com/watch?v=Oh1AiiPpoTo
#          https://link.springer.com/book/10.1007/b97624
def mandelbrot(c, ν = 0x42):
    ω = complex() 
    for _ in range(ν):
        ω = pwr(ω, 2) + c  
        # Overflow prevention makes NaN-check superfluous...
        # ω[any([isnan(ω), abs(ω) > 0x2], axis = 0)] = 0x2
        ω[abs(ω) > 0x2] = 0x2 
    return abs(ω) < 2.0

## And a picturesque version  
def mandelbrother(c, ν = 0x42):
    ω = complex() 
    for _ in range(ν):
        ω = pwr(ω, 2) + c        
        ω[abs(ω) > 0xfffffffff] = 0x0 # Face-lifting an old set...
    return abs(ω)

## Presentation
# Rehearsal...
N, M = 0x400, 0x400     # resolution
X, Y, ε = -1/2, 0, 3/2  # size
Ω = mt([[complex(n, m) for n in ls(X - ε, X + ε, N)] for m in ls(Y - ε, Y + ε, M)])

## ... and act! Iteration numbers, '0x6' and '0x42', are rather arbitrarily
#               selected to make the compound image look nice(r)...
M, MM = mandelbrot(Ω), mandelbrother(Ω, 0x6) + mandelbrother(Ω)
DI((M, log(e + MM)), ('Mandelbrot...', 'Mandelbrothers...'), cmp = 'copper')
