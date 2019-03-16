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
# Unsettling settings (ζ - zoom factor, ρ - resolution)
ζ, ρ = 0x1, 0x10            # size
N, M = ρ * 0x20, ρ * 0x10   # resolution
n = int(0x40 * pwr(ζ, 1/3)) # Accuracy set to grow with a zoom factor ζ
                            # A cube root makes it nicer for ζ = 1,...,100
# ... and a show off!
Ω = mt([[complex(n, m) for n in lsp(-2/ζ, 2/ζ, N)] 
                       for m in lsp(-1/ζ, 1/ζ, M)])
J = julia(Ω, n)
J[isnan(J) | (J > 0xff)] = 0xff # Handling the "NaNs'n'Infs"

plt.imshow(J, cmap = 'Blues')
plt.show()
