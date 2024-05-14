from matplotlib.pyplot import bar, plot, subplot, figure, tight_layout, show, xlabel, ylabel, title
from numpy import exp, sin, concatenate as ConcaTenate, arange, abs, pi as π, linspace as lp, sum, outer
from random import random as rr, randrange as ri
from auxiliary import ITT


@ITT
def dft(x, s = 1):
    ## A neat matrix-based implementation of the 1D DFT [via Copilot I]
    #  https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html
    N = len(x)
    ω = outer(arange(N), arange(N))
    W = exp(-s*2j * π * ω/N)
    
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
    
## Usage example (look for some invariances...)        
N = 0x100; t = lp(0, 1, N)
f = 0x20 >> 1, 0x20, 0x20 << 1  # 8, 32, 128 Hz (for 256 Hz sampling rate)
φ = 2*rr()*π, -π/2, 2*rr()*π    # Do phase matter?

# A slow signal (see https://stackoverflow.com/a/26283381/17524824)
x = sum([sin(2*_f*π*t + _φ) for _f, _φ in zip(f, φ)], axis = 0)
# ... and its standard and fast transforms
_X, X = dft(x), CooleyTukey(x)

## Plotting
figure(figsize = (10, 0b110))

# A signal
subplot(4, 1, 1); plot(t, x, color = 'red')
title("Slow signal"); xlabel("Time"); ylabel("Amplitude")

# Its fast transform
subplot(4, 1, 2); bar(arange(N), abs(X), color = 'brown', width = 1.0)
title("Fast transform"); ylabel("Magnitude")

# Its transform
subplot(4, 1, 3); bar(arange(N), abs(_X), color = 'black', width = 1.0)
title("Slow transform"); xlabel("Frequencies [Hz]"); ylabel("Magnitude")

# Itself
subplot(4, 1, 4); plot(arange(N), idft(_X).real, color = 'red')
title("Slow signal"); xlabel("Time"); ylabel("Amplitude")

tight_layout(); show()