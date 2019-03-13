import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt

# An approximate Julia set function 
def julia(x, n = 32):  # precision grows with n
    c = - .835 - .2321j     # see e.g. https://en.wikipedia.org/wiki/Julia_set
    for _ in range(n):
        x = pwr(x, 2) + c
    return abs(x) < 2       # x ∈ M if |x| < 2

# Presentation resolution
R = 1; N, M = R * 1024, R * 512
A = mt([[complex(n, m) for n in lnsp(-2, 2, N)] 
                       for m in lnsp(-1, 1, M)])
A = julia(A)
plt.imshow(A, 
           interpolation = 'gaussian', # uncomment if you fancy a colorful image
           cmap = 'Blues')
plt.show()