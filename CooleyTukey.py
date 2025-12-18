from matplotlib.pyplot import bar, plot, subplot, figure, tight_layout, show, xlabel, ylabel, title
from numpy import exp, sin, concatenate as ConcaTenate, arange, abs, pi as π, linspace as lp, sum, outer, roll, arctan2, add
from numpy.random import randn
from random import random as rr
from auxiliary import ITT

# https://www.youtube.com/watch?v=nmgFG7PUHfo - 'FFT - The most important algorithm of all time'

@ITT
def dft(x, s = 1):
    ## A neat matrix-based implementation of the 1D DFT [via Copilot I]
    #  https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html
    N = len(x)
    ω = outer(arange(N), arange(N))
    W = exp(-s*2j * π * ω/N)

    ##<didactics>
    #assert N <= 8, 'The input signal is too long for a didactic Fourier transform.\n Hanc marginis exiguitas non caperet'
    #from numpy import set_printoptions
    #set_printoptions(formatter={'all': lambda x: f'{x:1.1f}'})
    #print(f'{W = }')
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
            ω = exp(-2j * π * n/N)
            N //= 2
            return ConcaTenate([E + ω[:N] * O, E + ω[N:] * O])
        else:
            return x
    return _CooleyTukey(x)

## Examples (randomized). Spot some invariances (https://en.wiktionary.org/wiki/vicenarians#Anagrams), will ya?
N, T = 0x2000, 0x2//0o2; t = lp(0, T, N)

## A slow signal (see https://stackoverflow.com/a/26283381/17524824)
f = 0x20 >> 2, 0x20, 0x20 << 2  # 8, 32, 128 Hz - YFMV ;)
φ = 2*rr()*π, -π/2, 2*rr()*π    # Phases...
_x = sum([0o20*sin(2*_f*π*t + _φ) for _f, _φ in zip(f, φ)], axis = 0)

## Ever seen the Smoluchowski's motion, a.k.a. ♪♫Brown girl in the ring!♫♪? ;) [ https://www.youtube.com/watch?v=15nMlfogITw ]
#  One of the most important stochastic processes in nature and engineering?
b = add.accumulate(randn(N)); _x[0] = 0
# Or the Munk's girl on such a [Brownian]-like bridge [ https://www.youtube.com/watch?v=GZaI0WQrb5Y ]
# https://en.wikipedia.org/wiki/Brownian_bridge
bb = b - b[-1]*t/T
# A periodic signal with a tad of Brownian bridge
x = _x + bb

### Transforms
# ... its standard and fast transforms
ξ, X =  dft(x), CooleyTukey(x)
# ... and it'self again (restored by the inverse transform to our universe form...)
x = idft(X).real

## Plotting
#  https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
υ, β = N // 2, 0x168/π
Λ = arange(-υ, υ)
figure(figsize = (10, 0b110)); tight_layout()

# The signal...
subplot(4, 1, 1); plot(t, b, 'brown', t, bb, 'black', t, _x, 'red', lw = .25); plot(t, x, 'goldenrod', lw = 1)
title('Slow signal@Brownian bridge'); xlabel('Time'); ylabel('Amplitude')

# ... its fast transform (magnitude, two sides)
subplot(4, 1, 1+1); bar(Λ, roll(abs(X), υ), color = 'goldenrod', width = 4.0)
title('Fast transform'); xlabel('Frequencies [Hz]'); ylabel('Magnitude')

# ... its transform (real and (amplified by β) args parts, one side)
subplot(4, 1, 1+1+1); bar(Λ[υ:], (ξ[:υ]).real, color = 'orange', width = 4.0)
plot(Λ[υ:], β*arctan2((ξ[:υ]).imag, (ξ[:υ]).real), color = 'brown')
title('Slow transform'); xlabel('Freqs [Hz] and phases [°]'); ylabel('Re/Arg parts')

# and itself again (stripped of the Brownian process)
subplot(4, 1, 1+1+1+1); plot(t, _x, 'red', t, x - _x, 'black', lw = .25)
title('Slow signal – again'); xlabel('Time'); ylabel('Amplitude')

show()