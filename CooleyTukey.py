from matplotlib.pyplot import bar, plot, subplot, figure, tight_layout, show, xlabel, ylabel, title
from numpy import exp, sin, concatenate, arange, abs, pi as π, linspace as lp, sum
from random import random as rr, randrange as ri

def CooleyTukey(x):
    """
    A recursive implementation of the 1D Cooley-Tukey FFT
    https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.03-Fast-Fourier-Transform.html 
    [via Copilot]
    """
    N = len(x)
    if N > 1:
        E, O = CooleyTukey(x[::2]), CooleyTukey(x[1::2])
        t = exp(-2j * π * arange(N)/N)
        N = N >> 1
        return concatenate([E + t[:N] * O, E + t[N:] * O])
    else:
        return x
    
N = 0x100
# time, frequencies & phases
t, f, φ = lp(0, 1, N), (1<<ri(3), 1<<ri(4), 1<<ri(5)), (2*rr()*π, 2*rr()*π, 2*rr()*π)
# A slow signal (see https://stackoverflow.com/a/26283381/17524824)
x = sum([sin(2*_f*π*t + _φ) for _f, _φ in zip(f, φ)], axis = 0)
# ... and its fast transform
X = CooleyTukey(x)

# Plotting
figure(figsize = (10, 6))
subplot(2, 1, 1)
plot(t, x, color = 'brown')
title("Input Signal"); xlabel("Time"); ylabel("Amplitude")

subplot(2, 1, 2)
N = N >> 1
bar(arange(N), abs(X[:N]), color = 'red', width = 1.0)
bar(arange(N), abs(X[N:]), color = 'black', width = 1.0)
title("FFT Spectrum"); xlabel("Frequency Bin"); ylabel("Magnitude")

tight_layout(); show()