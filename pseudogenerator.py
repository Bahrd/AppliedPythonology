import matplotlib.pyplot as plt
from numpy import pi as π, floor, array, unique, histogram, arange
from matplotlib import colormaps as cmps
from matplotlib.colors import LinearSegmentedColormap as lscm
from auxiliary import YCoCg_ext_channels as YCoCg

# Fancy parsing... https://docs.python.org/3/howto/argparse.html#argparse-tutorial
# Check this out: '.\pseudogenerator.py --N 0o011110 --Z π**π'
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--N', help = 'N - number of numbers (a multiple of 6 - just for [our] coding convenience])')
parser.add_argument('--Z', help = 'Z - an integer multiplier')
parser.add_argument('--S', help = 'S - a seed', type = float)
# Pseudo-random sequence parameters
args = parser.parse_args()
N = eval(args.N) if args.N and eval(args.N)%6 == 0 else 0o010010
Z = eval(args.Z) if args.Z else 0o1001
S = args.S if args.S else π

# A helper function for a colormap "pick'n'roll" (that is, selecting and resampling)
cmn = lambda name, N, υ = 1: cmps[name].resampled(N//υ)([next(sprngr) for _ in range(N//υ)])

## A 'sawtooth' bona fide generator (a.k.a a multiplicative pseudo-random number generator)  
def sawtooth(x, z):
    while True:
        x = x * z - floor(x * z)
        yield x

sprngr = sawtooth(S, Z)
X = [next(sprngr) for _ in range(N)]

''' And here is a slew of look'n'feel uniform randomness checks... 
    For a bit more serious testing one should consider 
    https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test '''

# Simple 'pair' test (Double-check, they say...)
ttl = f'Pseudo-random pairs from a {Z} pseudo-tooth pseudo-generator'
υ = 2
x, y = [array(X[n:N:υ]) for n in range(υ)]
_ = plt.title(ttl), plt.scatter(x, y, c = cmn('ocean', N, υ)), plt.show()

# Simple 'tripple' test (A triple-check is better 
# (3/2, that is, three seconds better - to be precise... ;) 
# than the double-one, ain't it?)
ttl = f'Pseudo-random tripples from a {Z} pseudo-tooth pseudo-generator'
υ = 3
x, y, z = [array(X[n:N:υ]) for n in range(υ)]
ax = plt.figure().add_subplot(projection = '3d')
_ = plt.title(ttl), ax.scatter(x, y, z, c = cmn('terrain', N, υ), marker = '*')
plt.show()

# Histogram...
bins = 0o100

colors = lscm.from_list(YCoCg[2][0], YCoCg[2][1:], N = bins)(arange(N))
ttl = f'{N} pseudo-random samples from a {Z} pseudo-tooth pseudo-generator'

# A few thingumajigs... to make a histogram look likeable
h, x = histogram(X, bins = bins); nx = x[1:]*0x200/(max(x[1:]) - min(x[1:]))
_ = plt.title(ttl), plt.bar(nx, h, width = 10, color = colors, alpha = 0.7)
plt.show()

# Yet another (quick'n'dirty) anomaly check: lack of periodicity
U = unique(X)                #_, U = np.unique(X, return_counts = True)
adverb = 'Not' if len(U) != len(X) else 'Quite'
ttl = f'{adverb} a nonperiodic sequence: {len(U)} (out of {len(X)}) values are unique'
_ = plt.title(ttl), plt.scatter(U, U, c = cmn('winter', len(U)), marker = '.'), plt.show()

# And another one...
from scipy.fftpack import dct
Y = dct(array(X)) 
Y[0] = 0 # Ditch a "DC"... No one cares! ;)
_ = plt.scatter(arange(len(Y)), Y, c = cmn('summer', N), marker = '.'), plt.title("DCT of X"), plt.show()