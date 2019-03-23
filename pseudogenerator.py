import numpy as np; import matplotlib.pyplot as plt

# A "saw" function definition
def p(x, z, m = 1.0):
    y = (x * z) - np.floor(x * z)   # 'toothing' operation
    return m * y

# Pseudo-random sequence parameters (quite random already)
N, Z, X = 1023, 31415, [1.0/np.pi]; #Quantity, Teeth number, Initial value

# Sequence generation
for _ in range(N):
    x  = X.pop();      # Note:   'pop()' removes 'x' from 'X'!
    X += x, p(x, Z)    # Equiv.: X.append(x); X.append(p(x, Z))

# Presentations (look'n'feel randomness checks)
# Histogram...
plt.hist(X, bins = 'auto', density = True) 
plt.title("{0} pseudorandom samples for a {1} tooth pseudogenerator"
          .format(N, Z))
plt.show()

# A simple lack of periodicity check
U = np.unique(X)                #_, U = np.unique(X, return_counts = True)
# Yet another anomaly check...
plt.plot(U)
plt.title("{0} a nonperiodic sequence: {1} (out of {2}) values are unique."
          .format("Not" if len(U) != len(X) else "Quite", len(U), len(X)))
plt.show()

# And another one...
from scipy.fftpack import dct
Y = abs(dct(np.array(X) - 0.5)) # '- 0.5' ditches a "DC"
plt.plot(Y); plt.title("DCT of X"); plt.show()
