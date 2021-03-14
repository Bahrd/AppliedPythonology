# A 'sawtooth' bona fide generator (a.k.a a multiplicative pseudo-random number generator)  
import numpy as np
def sawtooth(x, z):
    while True:
        yield x
        x = x * z - np.floor(x * z)

# Pseudo-random sequence parameters (quite random already)
N, Z, S = 0o2000, 0o1001, 1/np.pi; sprngr = sawtooth(S, Z)
X = [next(sprngr) for _ in range(N)]

''' And a slew of look'n'feel uniform randomness checks... 
    For a bit more serious testing one should consider 
    https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test '''

import matplotlib.pyplot as plt
# Simple 'pair' check
x, y = X[0:0o2000:2], X[1:0o2000:2]
ttl = f'Pseudo-random pairs from a {Z} pseudo-tooth pseudo-generator'
_ = plt.title(ttl), plt.plot(x, y, 'r.'), plt.show()

# Histogram...
ttl = f'{N} pseudo-random samples from a {Z} pseudo-tooth pseudo-generator'
_ = plt.title(ttl), plt.hist(X, bins = 'auto', density = True), plt.show()

# Lack of periodicity check
U = np.unique(X)                #_, U = np.unique(X, return_counts = True)

# Yet another anomaly check...
adverb = 'Not' if len(U) != len(X) else 'Quite'
ttl = f'{adverb} a nonperiodic sequence: {len(U)} (out of {len(X)}) values are unique'
_ = plt.title(ttl), plt.plot(U, 'r.'), plt.show()

# And another one...
from scipy.fftpack import dct
Y = abs(dct(np.array(X) - 0.5)) # '- 0.5' ditches a "DC"
_ = plt.plot(Y, 'r.'); plt.title("DCT of X"), plt.show()