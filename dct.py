from sys import argv
from numpy import linspace as lp, random, ones, arange
from scipy.fftpack import dct, idct
from math import pi as π
from matplotlib.pyplot import (grid, plot, subplot, show, title, xlabel, bar,
                               subplots, tight_layout, yticks, legend)

T = eval(argv[1]) if len(argv) > 1 else π/2
L, intervals, rng = 0x100, 1, random.default_rng()
X, (f1, f2) = lp(0, 1.0, L), (0b111, 0b1111) # ♪♫ I'll be seeing you again!         https://youtu.be/xYQ2rJUT0Vg?t=101
                                             #    I'll be seeing you in Hertz's! ♫♪ https://youtu.be/0o4yv6Cm_ag
#'''
## Almost like a photo...? pleth...?? Anyway, a PPG-like signal!
#  https://en.wikipedia.org/wiki/Photoplethysmogram#Monitoring_heart_rate_and_cardiac_cycle
#  See also: https://en.wikipedia.org/wiki/Photoplethysmogram#Monitoring_depth_of_anesthesia
from numpy import abs, cos
from itertools import repeat; from more_itertools import flatten
name = 'PPG-like signal'
s = 0o10 + 0b100*cos(f1 * π*X) + 0b10*cos(f2 * π*X); s = list(flatten(repeat(s, intervals)))
# ♪♫ Here come the rain [of photons] again ♫♪ https://www.youtube.com/watch?v=TzFnYcIqj6I
# (albeit in their usual random and Poissonian fashion...)
S = rng.poisson(s)
#'''
'''
## A square wave (a.k.a. a digital signal?)
from numpy import sqrt, cos, sign, zeros
from itertools import repeat; from more_itertools import flatten
name = 'square wave'
_s = sign(sqrt(1/0b101)*cos(f1 * π*X)) - sign(sqrt(1/0b101)*cos(f2 * π*X))
s, ε = list(flatten(repeat(_s, intervals))), zeros(L * intervals)
S = s + ε
'''
'''
## A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
#  https://www.youtube.com/watch?v=iphcyNWFD10 - Veritasium's take on it
#  https://www.youtube.com/watch?v=B4XzLDM3Py8 - MIT
from numpy import sin, linspace as lp
name = 'chirp'
X = lp(0.05, 1.0, L * intervals)
s, ε = sin(1/X), rng.standard_normal(L * intervals)/0b100
S = s + ε
'''

subplots(num = "When DCT and thresholding crossed paths...")[1].axis('off'); tight_layout()
# A bit of grid drama...
ax = subplot(0b10, 0b10, 0o1); stop, step = 0x10 + 0b100, 0b10
yticks(range(0o0, stop, step))
for _c, a in enumerate(ax.get_ygridlines()):
    c = _c*(step/stop)
    a.set_color((c, c, c)); a.set_linestyle('dashed')
grid()

## Checkpoint I
plot(S, 'k.'); plot(s, 'xkcd:orangey yellow', alpha = 0b1/0o10)
legend(['Measurements', 'Ground truth']); title(f'I. Raw {name}')
FS = dct(S, norm = 'ortho')
# A DC component is usually important, but not here and now...
# (Note that DC and DCT only look and sound similarly!)
DC = FS[0]; FS[0] = 0
Hz = arange(FS.shape[0])/intervals
___, lw = ones(len(Hz)) * T, 1/0b100 # Just a threshold line

## Checkpoint II: A frequency domain representation
subplot(0b10, 0b10, 0b10)
bars, pplot = bar(Hz, FS, color = 'xkcd:pale orange', width = 1.0), plot(Hz, ___, 'k', lw = lw)
legend(['Threshold', 'Frequencies']); title('II. DCT'); xlabel('Hz', color = 'xkcd:dark orange')

# ... and a bit of threshold drama too (in the "Orange is the new black" style)
# https://www.imdb.com/title/tt2372162/trivia/?item=tr2033915&ref_=ext_shr_lnk
# That is, changing colors of "any bar bars above" ♪♫ Back to black ♫♪ https://youtu.be/TJAfLE39ZZ8?t=17
abba = lambda x: abs(x.get_height()) > pplot[0].get_data()[1][1]
for hibar in (fubar for fubar in bars if abba(fubar)): hibar.set_color('xkcd:black')

## Checkpoint III: A fast'n'ferocius'in'frequency domain data processing (a.k.a. L₁-like regularization)

FS[abs(FS) < T] = 0

# No drama, just good ole ♪♫ Back in black! ♫♪ https://youtu.be/pAgnJDJN4VA?t=10
subplot(0b10, 0b10, 0b100); bar(Hz, FS, color = 'k', width = 1.0); plot(Hz, ___, 'k', lw = lw); plot(Hz, -___, 'k', lw = lw)
legend(['Frequencies', 'Threshold']); title('III. DCT²'); xlabel('Hz', color = 'xkcd:dull orange')


## Checkpoint IIII: DC restoration and IDCT
FS[0] = DC; IS = idct(FS, norm = 'ortho')
subplot(0b10, 0b10, 0b11); plot(IS, 'k'); plot(IS - s, color = 'xkcd:tan'); plot(s, color = 'xkcd:red orange')
title(f'IV. Recovered {name}'); legend(['Estimate', 'Error', 'Ground truth']); show()

'''——————
    Magic pencils!
    * https://youtu.be/vPFy8QQmf2k?t=176          [PG]
    " If you're good at something, never do it for free!" https://www.imdb.com/title/tt0468569/quotes/?item=qt0484261
    * https://www.youtube.com/watch?v=ppOVLojanC8 [R+]
    " Let's not blow this out of proportion! " https://www.imdb.com/title/tt0468569/quotes/?item=qt0484294
'''