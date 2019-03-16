import matplotlib.pyplot as plt
from numpy import linspace as lsp, power as pwr, mat as mt, isnan

## An approximate Julia set function (accuracy grows with ν)
#       J = {ω ∈ Ω: julia(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Julia_set for nicer c's
def julia(ω, ν = 0x40, c = -.8 + .156j, p = 2):
    for _ in range(ν):
        ω = pwr(ω, p) + c
    return abs(ω)           # Not exactly a set function
                            # but looks somehow fancier..
## Presentation
# Unsettling settings
[N, M] = [0x400, 0x200]     # resolution
Ω = mt([[complex(n, m) for n in lsp(-2, 2, N)] 
                       for m in lsp(-1, 1, M)])
# ... and a show off!
J = julia(Ω)
J[isnan(J) | (J > 0xff)] = 0xff # Handling the "NaNs'n'Infs"

plt.imshow(J, cmap = 'Blues')
plt.show()