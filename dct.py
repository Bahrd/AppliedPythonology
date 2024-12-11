from numpy import linspace as lp, random, ones, arange
from scipy.fftpack import dct, idct
from math import pi as π
from matplotlib.pyplot import plot, subplot, show, title, xlabel, bar, subplots, tight_layout

L, intervals, rng = 0x100, 1, random.default_rng()
X, (f1, f2) = lp(0, 1.0, L), (0b101, 0b111) # ♪♫ I'll be seeing you again!         https://youtu.be/xYQ2rJUT0Vg?t=101
                                            #    I'll be seeing you in Hertz's! ♫♪ https://youtu.be/0o4yv6Cm_ag

#'''
## Almost like a PPG signal
from numpy import abs, sqrt, cos
from itertools import repeat; from more_itertools import flatten

_s = sqrt(1/0b101)*cos(f1 * π*X) - sqrt(1/0b101)*cos(f2 * π*X)
s = list(flatten(repeat(_s, intervals))); ε = (abs(s) - rng.poisson(abs(s)))/0b10
T = 1
#'''
'''
## A square wave (a.k.a. a digital signal?)
from numpy import sqrt, cos, sign, zeros
from itertools import repeat; from more_itertools import flatten

_s = sign(sqrt(1/0b101)*cos(f1 * π*X)) - sign(sqrt(1/0b101)*cos(f2 * π*X))
s, ε = list(flatten(repeat(_s, intervals))), zeros(L * intervals)
T = 1
'''
'''
## A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
#  https://www.youtube.com/watch?v=iphcyNWFD10 - Veritasium's take on it
#  https://www.youtube.com/watch?v=B4XzLDM3Py8 - MIT
from numpy import sin, linspace as lp
X = lp(0.05, 1.0, L * intervals)
s, ε = sin(1/X), rng.standard_normal(L * intervals)/0b100
T = π/2
'''

S = s + ε

subplots(num = "When DCT's and thresholding's paths crossed...")
tight_layout()

#Checkpoint I
subplot(0b10, 0b10, 0o1); plot(S, 'k.'); plot(s, 'r'); title('Raw PPG')
FS = dct(S, norm = 'ortho')
Hz = arange(FS.shape[0])/intervals

#Checkpoint II: IDCT
subplot(0b10, 0b10, 0b10); bar(Hz, FS, color = 'red', width = 1.0);title('DCT'); xlabel('Hz', color = 'red')
FS[abs(FS) < T] = 0; __ = ones(len(Hz)) * T
plot(Hz, __, 'k', linewidth = .25); plot(Hz, -__, 'k', linewidth = .25)

## Processing in a frequency domain
subplot(0b10, 0b10, 0b100); bar(Hz, FS, color = 'black', width = 1.0); title('DCT²'); xlabel('Hz', color = 'red')
plot(Hz, __, 'k', linewidth = .25); plot(Hz, -__, 'k', linewidth = .25)

#Checkpoint III: IDCT
IS = idct(FS, norm = 'ortho')
subplot(0b10, 0b10, 0b11); plot(IS, 'k'); plot(IS - s, color = 'xkcd:light gray'); plot(s, color = 'red'); title('Smooth PPG')
show()

## Magic pencils!
# https://youtu.be/vPFy8QQmf2k?t=176          [G]
# https://www.youtube.com/watch?v=ppOVLojanC8 [R]
