from matplotlib.pyplot import imshow, title, show
from numpy import linspace as lsp, power as pwr, mat as mt, isnan, any, log, e
from auxiliary import displayImages as DI; 

## An approximate Julia set function (resolution grows with ν)
#       J = {ω ∈ Ω: julia(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Julia_set for some nicer c's
def julia(ω, ν = 0x40, c = -.8 + .156j, p = 2):
    for _ in range(ν):
        ω = pwr(ω, p) + c
        # Julia's face-lifting...
        ω[any([isnan(ω), abs(ω) > 0xff], axis = 0)] = 0xf
    return log(e + abs(ω))  # Not exactly a set function (like it would've been with 'return abs(ω) > 2')
                            # but looks somehow fancier..

## Presentation
# Unsettling settings
N, M = 0x400, 0x200  # resolution
Ω = mt([[complex(n, m) for n in lsp(-2, 2, N)] 
                       for m in lsp(-1, 1, M)])
# ... and a show off!
c = -.8 + .156j; J = julia(Ω, c = c)

DI(J, 'Julia set for c = {}'.format(c), cmp = 'Blues')