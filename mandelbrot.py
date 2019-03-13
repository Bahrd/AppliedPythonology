import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt

# An approximate Mandelbrot set function 
def mandelbrot(c, n = 32):  # precision grows with n
    x = complex(0, 0) 
    for _ in range(n):
        x = pwr(x, 2) + c
    return abs(x) < 2       # x ∈ M if |x| < 2

# Presentation preparation
R = 1; N, M = R * 768, R * 512
A = mt([[complex(n, m) for n in lnsp(-2, 1, N)] 
                       for m in lnsp(-1, 1, M)])

plt.imshow(mandelbrot(A), 
           #interpolation = 'lanczos', # uncomment if you fancy a colorful image
           cmap = 'Blues')
plt.show()

## Outtakes
#N = 32; M = 48
#A = mt([[mandelbrot(complex(n, m)) for n in lnsp(-2, 1, N)] 
#                                   for m in lnsp(-1, 1, M)])
