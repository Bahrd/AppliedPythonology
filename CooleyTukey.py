from matplotlib.pyplot import bar, plot, subplot, figure, tight_layout, show, xlabel, ylabel, title
from numpy import exp, sin, concatenate, arange, abs, pi as π, linspace as lp
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
# time, frequencies and phases
# t, (f1, f2, f3), (φ1, φ2, φ3) = lp(0, 1, N), (1<<3, 1<<4, 1<<5), (π/2, π/3, π/4)
from random import random as rr, randrange as ri
t, (f1, f2, f3), (φ1, φ2, φ3) = lp(0, 1, N), (1<<ri(3), 1<<ri(4), 1<<ri(5)), (2*rr()*π, 2*rr()*π, 2*rr()*π)

# A slow signal... 
x = sin(2*f1*π*t + φ1) + sin(2*f2*π*t + φ2) + sin(2*f3*π*t + φ3)
# ... and its fast transform
X = CooleyTukey(x)

# Plotting
figure(figsize = (10, 6))
subplot(2, 1, 1)
plot(t, x)
title("Input Signal"); xlabel("Time"); ylabel("Amplitude")

subplot(2, 1, 2)
bar(arange(N//2), abs(X[:N//2]), color = 'red', width = 1.0)
title("FFT Spectrum"); xlabel("Frequency Bin"); ylabel("Magnitude")

tight_layout(); show()
