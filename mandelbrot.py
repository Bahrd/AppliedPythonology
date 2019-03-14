import matplotlib.pyplot as plt
from numpy import linspace as lnsp, power as pwr, mat as mt

## An approximate Mandelbrot set function (accuracy grows with n)
# see e.g. https://en.wikipedia.org/wiki/Mandelbrot_set
def mandelbrot(c, n = 64):
    x = complex() 
    for _ in range(n):
        x = pwr(x, 2) + c
    return abs(x) < 2       # x ∈ M if |x| < 2

## Presentation
# Rehearsal...
X, Y, eps = -1/2, 0, 1
R = 16; N, M = R * 32, R * 32 
A = mt([[complex(n, m) for n in lnsp(X - eps, X + eps, N)] 
                       for m in lnsp(Y - eps, Y + eps, M)])
# ... and act!
M = mandelbrot(A)
plt.imshow(M,
           interpolation = 'bicubic', # uncomment if you fancy a colorful image
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
