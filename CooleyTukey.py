from matplotlib.pyplot import bar, plot, subplot, figure, tight_layout, show, xlabel, ylabel, title
from numpy import exp, sin, concatenate as ConcaTenate, arange, abs, pi as π, linspace as lp, sum, outer, roll, arctan2 
from random import random as rr
from auxiliary import ITT

@ITT
def dft(x, s = 1):
    ## A neat matrix-based implementation of the 1D DFT [via Copilot I]
    #  https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html
    N = len(x)
    ω = outer(arange(N), arange(N))
    W = exp(-s*2j * π * ω/N)
    
    ##<didactics>
    # assert N <= 8, "The input signal is too long for a didactic Fourier transform"
    # from numpy import set_printoptions
    # set_printoptions(formatter={'all': lambda x: f'{x:1.1f}'})
    # print(f'{W = }')
    ## </didactics>

    return W @ x

idft = lambda x: dft(x, -1)/len(x)

@ITT
def CooleyTukey(x):
    ## A neat recursive implementation of Cooley'n'Tukey's 1D FFT [via Copilot II]
    #  https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.03-Fast-Fourier-Transform.html 
    def _CooleyTukey(x):
        N = len(x)
        if N > 1:
            E, O = _CooleyTukey(x[::2]), _CooleyTukey(x[1::2])
            n = arange(N)
            ω = exp(-2j * π * n/N); N >>= 1
            
            return ConcaTenate([E + ω[:N] * O, E + ω[N:] * O])
        else:
            return x
    return _CooleyTukey(x)
    
## Examples (randomized). Spot some invariances, will ya?
N = 0x1000; t = lp(0, 1, N)
f = 0x20 >> 2, 0x20, 0x20 << 2  # 8, 32, 128 Hz - YFMV ;)
φ = 2*rr()*π, -π/2, 2*rr()*π    # Phases...
# A slow signal (see https://stackoverflow.com/a/26283381/17524824)
x = sum([sin(2*_f*π*t + _φ) for _f, _φ in zip(f, φ)], axis = 0)
# ... its standard and fast transforms
_X, X =  dft(x), CooleyTukey(x)
# ... and it'self again (restored by the standard inverse transform)
_x = idft(X).real

## Plotting
#  https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
υ, β = N >> 1, 0x168/π
Λ = arange(-υ, υ)
figure(figsize = (10, 0b110))

# The signal
subplot(4, 1, 1); plot(t, x, color = 'darkred')
title("Slow signal"); xlabel("Time"); ylabel("Amplitude")

# Its fast transform (magnitude, two sides)
subplot(4, 1, 1+1); bar(Λ, roll(abs(X), υ), color = 'goldenrod', width = 4.0)
title("Fast transform"); xlabel("Frequencies [Hz]"); ylabel("Magnitude")

# Its transform (real and (amplified by β) args parts, one side)
subplot(4, 1, 1+1+1); bar(Λ[υ:], (_X[:υ]).real, color = 'orange', width = 4.0)
plot(Λ[υ:], β*arctan2((_X[:υ]).imag, (_X[:υ]).real), color = 'brown')
title("Slow transform"); xlabel("Freqs [Hz] and phases [°]"); ylabel("Re/Arg parts")

# Itself (stripped of the residual imaginary part)
subplot(4, 1, 1+1+1+1); plot(t, _x, color = 'darkred'); plot(t, _x - x, 'k')
title("Slow signal"); xlabel("Time"); ylabel("Amplitude")

tight_layout(); show()