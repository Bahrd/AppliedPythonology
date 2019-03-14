import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt, isnan

## An approximate Mandelbrot set function (accuracy grows with n)
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
def mandelbrot(c, n = 0x40):
    x = complex() 
    for _ in range(n):
        x = pwr(x, 2) + c
    return abs(x) < 2       # x ∈ M if |x| < 2

## Presentation
# Rehearsal...
X, Y, eps = -1/2, 0, 1
R = 0x10; N, M = R * 0x20, R * 0x20 
A = mt([[complex(n, m) for n in lnsp(X - eps, X + eps, N)] 
                       for m in lnsp(Y - eps, Y + eps, M)])
# ... and act!
M = mandelbrot(A)
plt.imshow(M, cmap = 'Blues')
plt.show()
