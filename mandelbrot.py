import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt

## An approximate Mandelbrot set function (accuracy grows with n)
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
def mandelbrot(c, n = 32): 
    x = complex() 
    for _ in range(n):
        x = pwr(x, 2) + c
    return abs(x) < 2       # x ∈ M if |x| < 2

## Presentation 
# Rehearsal...
R = 2; N, M = R * 768, R * 512 
A = mt([[complex(n, m) for n in lnsp(-2, 1, N)] 
                       for m in lnsp(-1, 1, M)])
# Act!
plt.imshow(mandelbrot(A), 
           interpolation = 'lanczos', # uncomment if you fancy a colorful image
           cmap = 'Blues')
plt.show()

## Outtakes
#N = 48; M = 32
#A = mt([[mandelbrot(complex(n, m)) for n in lnsp(-2, 1, N)] 
#                                   for m in lnsp(-1, 1, M)])
#plt.imshow(A, 
#           #interpolation = 'lanczos', # uncomment if you fancy a colorful image
#           cmap = 'Blues')
#plt.show()
