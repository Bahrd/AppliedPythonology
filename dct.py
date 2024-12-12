from sys import argv
from numpy import linspace as lp, random, ones, arange
from scipy.fftpack import dct, idct
from math import pi as π
from matplotlib.pyplot import plot, subplot, show, title, xlabel, bar, subplots, tight_layout

T = eval(argv[1]) if len(argv) > 1 else π/2
L, intervals, rng = 0x100, 1, random.default_rng()
X, (f1, f2) = lp(0, 1.0, L), (0b101, 0b1110) # ♪♫ I'll be seeing you again!         https://youtu.be/xYQ2rJUT0Vg?t=101
                                             #    I'll be seeing you in Hertz's! ♫♪ https://youtu.be/0o4yv6Cm_ag
#'''
## Almost like a photo... pleth... PPG signal 
#  https://en.wikipedia.org/wiki/Photoplethysmogram#Monitoring_heart_rate_and_cardiac_cycle
#  See also: https://en.wikipedia.org/wiki/Photoplethysmogram#Monitoring_depth_of_anesthesia
from numpy import abs, cos
from itertools import repeat; from more_itertools import flatten

_s = 0b100*cos(f1 * π*X) + 0b10*cos(f2 * π*X)
s = list(flatten(repeat(_s, intervals))); ε = abs(s) - rng.poisson(abs(s))
#'''
'''
## A square wave (a.k.a. a digital signal?)
from numpy import sqrt, cos, sign, zeros
from itertools import repeat; from more_itertools import flatten

_s = sign(sqrt(1/0b101)*cos(f1 * π*X)) - sign(sqrt(1/0b101)*cos(f2 * π*X))
s, ε = list(flatten(repeat(_s, intervals))), zeros(L * intervals)
'''
'''
## A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
#  https://www.youtube.com/watch?v=iphcyNWFD10 - Veritasium's take on it
#  https://www.youtube.com/watch?v=B4XzLDM3Py8 - MIT
from numpy import sin, linspace as lp
X = lp(0.05, 1.0, L * intervals)
s, ε = sin(1/X), rng.standard_normal(L * intervals)/0b100
'''

S = s + ε

_, ax = subplots(num = "When DCT and thresholding crossed paths...")
ax.axis('off')
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
