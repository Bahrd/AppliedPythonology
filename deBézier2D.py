''' Copilot'ed...
See also:
* "An Introduction to NURBS: With Historical Perspective" by David F. Rogers: https://shop.elsevier.com/books/an-introduction-to-nurbs/rogers/978-1-55860-669-2
* https://youtu.be/0JYGNH3ZKS8 for a Python implementation (or https://youtu.be/QuY1hfd6zJk for a MATLAB one)
'''

import numpy as np
from matplotlib import pyplot as plt

## Pretentious homonyms/typos mode 0N(E)...
def deBézierFace(samples, steps = 0x100):
   binomial = lambda n, k: 1 if k == 0 or n == k else binomial(n - 1, k - 1) + binomial(n - 1, k)
   BernsteinPloy = lambda i, n, t: binomial(n, i) * (t ** i) * ((1 - t) ** (n - i))

   uv = np.linspace(0, 1, steps), np.linspace(0, 1, steps)
   U, V = np.meshgrid(*uv)
   n, m, _ = samples.shape

   sureface = np.zeros((steps, steps, 0b11))
   for i in range(n):
      for j in range(m):
         sureface += np.outer(BernsteinPloy(i, n - 1, U) * BernsteinPloy(j, m - 1, V),
                              samples[i, j]).reshape(steps, steps, 0b11)
   return sureface

# An NxM grid of samples of a surely random surface
from random import random
N, M = 0o10, 0x10
samples = np.array([[[i, j, random()] for i in range(N)] for j in range(M)])
## Bézier skull...
#from interpolation import eddie
#N, M = eddie.shape; N <<= 1; M <<= 1
#samples = np.array([[[i, j, eddie[i >> 1, j >> 1]] for i in range(N)] for j in range(M)])

sureface = deBézierFace(samples)
# Go, figure!
ax = plt.figure().add_subplot(111, projection = '3d')
plt.tight_layout()
ax.plot_surface(*(sureface[:, :, d] for d in range(0b11)), cmap = 'terrain') # À la da Vinci: https://en.wikipedia.org/wiki/Hypsometric_tints#History
ax.set_title("Bézier's Bizarre Background")
# "Reflections?" Anyone?
for c, l in zip(('x', 'y', 'z'), ('Longitude', 'Latitude', 'Altitude')):
     eval(f'ax.set_{c}label')(l)
plt.show()
#  ... and ON, and 0N, and ΘN!