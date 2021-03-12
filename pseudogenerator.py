import numpy as np; import matplotlib.pyplot as plt

# A 'sawtooth' generator function (a.k.a a multiplicative pseudo-random number generator)  
def stg(x, z):
    while True:
        yield x
        x = x * z - np.floor(x * z)

# Pseudo-random sequence parameters (quite random already)
N, Z, S = 1024, 31415, 1.0/np.pi
sprng = stg(S, Z)
X = [next(sprng) for _ in range(N)]

# A simple 'pair' check
x, y = X[0:1024:2], X[1:1024:2]
_ = plt.plot(x, y, 'r.'), plt.title(f'Pseudorandom pairs for a {Z} tooth pseudogenerator')
plt.show()

## Presentations (look'n'feel randomness checks)
# Histogram...
plt.hist(X, bins = 'auto', density = True) 
plt.title(f'{N} pseudorandom samples for a {Z} tooth pseudogenerator')
plt.show()

# A simple lack of periodicity check
U = np.unique(X)                #_, U = np.unique(X, return_counts = True)
# Yet another anomaly check...
plt.plot(U, 'r.')
adverb = 'Not' if len(U) != len(X) else 'Quite'
plt.title(f'{adverb} a nonperiodic sequence: {len(U)} (out of {len(X)}) values are unique.')
plt.show()

# And another one...
from scipy.fftpack import dct
Y = abs(dct(np.array(X) - 0.5)) # '- 0.5' ditches a "DC"
plt.plot(Y, 'r.'); plt.title("DCT of X"); plt.show()