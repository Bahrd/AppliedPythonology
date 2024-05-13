from scipy.fftpack import dct, idct
import numpy as np
import math
from matplotlib.pyplot import plot, subplot, show, title, xlabel, bar
from itertools import repeat
from more_itertools import flatten

L, intervals, rng = 0x100, 1, np.random.default_rng()
X, (f1, f2) = np.linspace(0, 1.0, L), (0b101, 0b111) #Hz

#'''
## PPG-like signal
_s = np.sqrt(1/0b101)*np.cos(f1 * math.pi * X) - np.sqrt(1/0b101)*np.cos(f2 * math.pi * X)
s = list(flatten(repeat(_s, intervals))); ε = (np.abs(s) - rng.poisson(np.abs(s)))/0b10
T = 1
#'''

'''
## A square wave (a.k.a. digital signal?) 
_s = np.sign(np.sqrt(1/0b101)*np.cos(f1 * math.pi * X)) - np.sign(np.sqrt(1/0b101)*np.cos(f2 * math.pi * X))
s, ε = list(flatten(repeat(_s, intervals))), np.zeros(L * intervals)
T = 5 
'''

'''
## A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
#  https://www.youtube.com/watch?v=iphcyNWFD10 - Veritasium's take on it
#  https://www.youtube.com/watch?v=B4XzLDM3Py8 - MIT
X = np.linspace(0.05, 1.0, L * intervals)
s, ε = np.sin(1/X), rng.standard_normal(L * intervals)/0b100
T = 2.5
'''

S = s + ε

#Checkpoint I
subplot(2, 2, 1); plot(S, 'k.'); plot(s, 'r'); title('Raw PPG')
FS = dct(S, norm = 'ortho')
Hz = np.arange(FS.shape[0])/intervals

#Checkpoint II: IDCT 
subplot(2, 2, 2); bar(Hz, FS, color = 'red', width = 1.0);title('DCT'); xlabel('Hz', color = 'red')
FS[abs(FS) < T] = 0; __ = np.ones(len(Hz)) * T
plot(Hz, __, 'k', linewidth = .25); plot(Hz, -__, 'k', linewidth = .25)

## Processing in a frequence domain
subplot(2, 2, 4); bar(Hz, FS, color = 'black', width = 1.0); title('DCT²'); xlabel('Hz', color = 'red')
plot(Hz, __, 'k', linewidth = .25); plot(Hz, -__, 'k', linewidth = .25)

#Checkpoint III: IDCT 
IS = idct(FS, norm = 'ortho')
subplot(2, 2, 3); plot(IS, 'k'); plot(IS - s, color = 'lightgray'); plot(s, color = 'red'); title('Smooth PPG'); show()

## Magic pencils! 
# https://youtu.be/vPFy8QQmf2k?t=176          [G]
# https://www.youtube.com/watch?v=ppOVLojanC8 [R]
