from scipy.fftpack import dct, idct
import numpy as np
import math
from matplotlib.pyplot import plot, show, title, xlabel, bar
from itertools import repeat
from more_itertools import flatten

L, intervals = 0x100, 1
X, (f1, f2) = np.linspace(0, 1.0, L), (5, 10) #Hz
_S = np.cos(f1 * math.pi * X) - np.sqrt(2)*np.cos(f2 * math.pi * X)
rng = np.random.default_rng()

s, ε = list(flatten(repeat(_S, intervals))), rng.standard_normal(L * intervals)
S = s + ε/0b100
## Magic pencils! 
# https://youtu.be/vPFy8QQmf2k?t=176          [G]
# https://www.youtube.com/watch?v=ppOVLojanC8 [R]

#'''
# A chirp-like signal (https://www.youtube.com/watch?v=TWqhUANNFXw [LIGO] ;)
X, (f1, f2) = np.linspace(0.05, 1.0, L * intervals), (5, 10) #Hz
rng = np.random.default_rng()

s, ε = np.sin(1/X), rng.standard_normal(L * intervals)/0b100
S = s + ε/0b100
#'''

#Checkpoint I
plot(S, 'k.'); plot(s, 'r'); title('PPG-like'); show()
#Checkpoint I: DCT 
FS = dct(S, norm = 'ortho')

Hz = np.arange(FS.shape[0])/intervals
bar(Hz, FS, color = 'red', width = 1.0); title('dct'); xlabel('Hz', color = 'red'); show()
## Processing in a frequence domain
FS[abs(FS) < 1] = 0
bar(Hz, FS, color = 'red', width = 1.0); title('dct'); xlabel('Hz', color = 'red'); show()
#Checkpoint II: IDCT 
S = idct(FS, norm = 'ortho')
plot(S, 'k.'); plot(S-s, color = 'gray'); plot(s, color = 'red'); title('idct'); show()