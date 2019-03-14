import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt, log as nlg
from math import log10

# An approximate Julia set function (accuracy grows with n)
# see e.g. https://en.wikipedia.org/wiki/Julia_set for nicer c's
def julia(x, c = -.835 -.2321j, p = 2, n = 32):
    for _ in range(n):
        x = pwr(x, p) + c
    return abs(x) < 2       # x ∈ J if |x| < 2
    #return abs(x)          # A fancier version

## Presentation
# Unsettling settings
R = 16; N, M = R * 64, R * 32
A = mt([[complex(n, m) for n in lnsp(-2, 2, N)] 
                       for m in lnsp(-1, 1, M)])
# ... and show off!
J = julia(A)                # J = nlg(julia(A)); J[J > 255] = 255
plt.imshow(J, 
           #interpolation = 'lanczos', 
           cmap = 'Blues')
plt.show()
