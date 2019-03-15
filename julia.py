import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt, isnan

## An approximate Julia set function (accuracy grows with n)
#       J = {ω: julia(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Julia_set for nicer c's
def julia(ω, c = -.8 + .156j, p = 2, n = 0x40):
    for _ in range(n):
        ω = pwr(ω, p) + c
    return abs(ω)       # Not exactly a set function
                        # but looks somehow fancier..
## Presentation
# Unsettling settings
zoom = 0x5; ρ = 0x10; N, M = ρ * 0x40, ρ * 0x20
Ω = mt([[complex(n, m) for n in lnsp(-2/zoom, 2/zoom, N)] 
                       for m in lnsp(-1/zoom, 1/zoom, M)])
# ... and a show off!
J = julia(Ω, n = 0x30 * zoom)
J[isnan(J) | (J > 0xff)] = 0xff

plt.imshow(J, cmap = 'Blues')
plt.show()