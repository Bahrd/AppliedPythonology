import matplotlib.pyplot as plt;
from numpy import linspace as lnsp, power as pwr, mat as mt, isnan

# An approximate Julia set function (accuracy grows with n)
# see e.g. https://en.wikipedia.org/wiki/Julia_set for nicer c's
def julia(x, c = -.8 + .156j, p = 2, n = 0x20):
    for _ in range(n):
        x = pwr(x, p) + c
    return abs(x)          # Not a set function (x ∈ J if |x| < 2) 
                           # but renders fancier figures..
## Presentation
# Unsettling settings
R = 0x10; N, M = R * 0x40, R * 0x20
A = mt([[complex(n, m) for n in lnsp(-2, 2, N)] 
                       for m in lnsp(-1, 1, M)])
# ... and show off!
J = julia(A)
J[isnan(J) | (J > 0xff)] = 0xff

plt.imshow(J, cmap = 'Blues')
plt.show()
