import matplotlib.pyplot as plt
from numpy import pi as π, floor, array, unique, histogram, arange
from matplotlib import colormaps as cmps
from matplotlib.colors import LinearSegmentedColormap as lscm
from auxiliary import YCoCg_ext_channels as YCoCg

# A 'sawtooth' bona fide generator (a.k.a a multiplicative pseudo-random number generator)  
def sawtooth(x, z):
    while True:
        x = x * z - floor(x * z)
        yield x

# Pseudo-random sequence parameters (quite random already)
N, Z, S = 0o4004, 0o1001, π; sprngr = sawtooth(S, Z)
X = [next(sprngr) for _ in range(N)]


''' And a slew of look'n'feel uniform randomness checks... 
    For a bit more serious testing one should consider 
    https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test '''

# Simple 'pair' test (Double-check, they say...)
υ = 2
x, y = array(X[0:N:υ]), array(X[1:N:υ])

cmn = cmps['ocean'].resampled(N//υ)([next(sprngr) for _ in range(N//υ)])
ttl = f'Pseudo-random pairs from a {Z} pseudo-tooth pseudo-generator'
_ = plt.title(ttl), plt.scatter(x, y, c = cmn), plt.show()

# Simple 'tripple' test (A triple-check is better (3/2, that is, three seconds better - to be precise... ;) than the double-one, ain't it?)
ax = plt.figure().add_subplot(projection = '3d')

υ = 3
x, y, z = array(X[0:N:υ]), array(X[1:N:υ]), array(X[2:N:υ])

cmn = cmps['terrain'].resampled(N//υ)([next(sprngr) for _ in range(N//υ)])
ttl = f'Pseudo-random tripples from a {Z} pseudo-tooth pseudo-generator'
_ = plt.title(ttl), ax.scatter(x, y, z, c = cmn, marker = 'o')
plt.show()

# Histogram...
bins = 0x20

cm = lscm.from_list(YCoCg[2][0], YCoCg[2][1:], N = bins)
colors = cm(arange(N))
ttl = f'{N} pseudo-random samples from a {Z} pseudo-tooth pseudo-generator'

# A few thingamagigs... to make a histogram look more likeable
h, x = histogram(X, bins = bins); nx = x[1:]*0x100/(max(x[1:]) - min(x[1:]))
_ = plt.title(ttl), plt.bar(nx, h, width = 10, color = colors, alpha = 0.7)
plt.show()

# Lack of periodicity check
U = unique(X)                #_, U = np.unique(X, return_counts = True)

# Yet another anomaly check...
cmn = cmps['winter'].resampled(len(U))([next(sprngr) for _ in range(len(U))])

adverb = 'Not' if len(U) != len(X) else 'Quite'
ttl = f'{adverb} a nonperiodic sequence: {len(U)} (out of {len(X)}) values are unique'
_ = plt.title(ttl), plt.scatter(U, U, c = cmn), plt.show()

# And another one...
cmn = cmps['summer'].resampled(N)([next(sprngr) for _ in range(N)])

from scipy.fftpack import dct
Y = abs(dct(array(X) - 0.5)) # '- 0.5' ditches a "DC". Somehow... ;)
_ = plt.scatter(arange(len(Y)), Y, c = cmn), plt.title("DCT of X"), plt.show()


