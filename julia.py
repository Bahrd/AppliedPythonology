import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt

# An approximate Julia set function (precision grows with n)
# see e.g. https://en.wikipedia.org/wiki/Julia_set for nicer c's
def julia(x, c = -.835 -.2321j, p = 2, n = 32):
    for _ in range(n):
        x = pwr(x, p) + c
    return abs(x) < 2       # x ∈ J if |x| < 2

## Presentation
# Unsettling settings
R = 1; N, M = R * 1024, R * 512
A = mt([[complex(n, m) for n in lnsp(-2, 2, N)] 
                       for m in lnsp(-1, 1, M)])
# Show off!
plt.imshow(julia(A), 
           interpolation = 'gaussian', 
           cmap = 'Blues')
plt.show()
