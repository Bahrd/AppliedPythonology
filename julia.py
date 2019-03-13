import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt

# An approximate Julia set function 
def julia(x, p = 2, n = 16):   # precision grows with n
    c = - .835 - .2321j # see e.g. https://en.wikipedia.org/wiki/Julia_set
    for _ in range(n):
        x = pwr(x, p) + c
    return abs(x) < 2       # x ∈ M if |x| < 2

# Unsettling settings
R = 1; N, M = R * 1024, R * 512
A = mt([[complex(n, m) for n in lnsp(-2, 2, N)] 
                       for m in lnsp(-1, 1, M)])

plt.imshow(julia(A), 
           interpolation = 'gaussian', 
           cmap = 'Blues')
plt.show()
