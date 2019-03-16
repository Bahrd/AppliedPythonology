import matplotlib.pyplot as plt
from numpy import linspace as lsp, power as pwr, mat as mt, isnan

## An approximate Julia set function (accuracy grows with ν)
#       J = {ω: julia(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Julia_set for nicer c's
def julia(ω, c = -.8 + .156j, p = 2, ν = 0x40):
    for _ in range(ν):
        ω = pwr(ω, p) + c
    return abs(ω)           # Not exactly a set function
                            # but looks somehow fancier..
## Presentation
# Unsettling settings (ζ - zoom factor, ρ - resolution)
ζ, ρ = 0x1, 0x10
N, M = ρ * 0x40, ρ * 0x20
n = int(0x40 * pwr(ζ, 1/3)) # Accuracy n should grow with a zoom factor ζ
                            # A cube root makes it nicer for ζ = 1,...,100
Ω = mt([[complex(n, m) 
         for n in lsp(-2/ζ, 2/ζ, N)] 
         for m in lsp(-1/ζ, 1/ζ, M)])
# ... and a show off!
J = julia(Ω, ν = n)
J[isnan(J) | (J > 0xff)] = 0xff # Handling the "NaNs'n'Infs"

plt.imshow(J, cmap = 'Blues')
plt.show()