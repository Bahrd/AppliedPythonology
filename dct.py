from scipy.fftpack import dct, idct
import numpy as np
import math
from matplotlib.pyplot import plot, show, title, ylabel, bar
from itertools import repeat
from more_itertools import flatten


X, intervals, (f1, f2) = np.linspace(-1.0, 1.0, 128), 10, (1, 2) #Hz
_S = np.cos(f1 * math.pi * X) - np.sqrt(2)*np.cos(f2 * math.pi * X)
S = list(flatten(repeat(_S, intervals)))

#Checkpoint I
plot(S); title('PPG-like'); show()
#Checkpoint I: DCT 
FS = dct(S, norm = 'ortho')
Hz = np.arange(FS.shape[0])/intervals
bar(Hz, FS, color = 'red', width = 1.0); title('dct'); ylabel('Hz', color = 'red'); show()
## Processing in a frequence domain
FS[4] = 0; FS[8] = 0
#Checkpoint II: IDCT 
S = idct(FS, norm = 'ortho')
plot(S); title('idct'); show()