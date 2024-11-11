﻿## Copilot'ed... See also: https://www.youtube.com/watch?v=QuY1hfd6zJk for a MATLAB flavor

import numpy as np
from random import random
from matplotlib import pyplot as plt

## Pretentious homonyms mode ON...
def deBézierFace(samples, steps = 128):
   binomial = lambda n, k: 1 if k == 0 or n == k else binomial(n - 1, k - 1) + binomial(n - 1, k)
   BernsteinPloy = lambda i, n, t: binomial(n, i) * (t ** i) * ((1 - t) ** (n - i))

   uv = np.linspace(0, 1, steps), np.linspace(0, 1, steps)
   U, V = np.meshgrid(*uv)
   n, m, _ = samples.shape
   
   sureface = np.zeros((steps, steps, 3))
   for i in range(n):
      for j in range(m):
         sureface += np.outer(BernsteinPloy(i, n - 1, U) * BernsteinPloy(j, m - 1, V),
                              samples[i, j]).reshape(steps, steps, 3)
   return sureface

# An NxM grid of samples of a surface
N, M = 8, 16
samples = np.array([[[i, j, 2*random() - 1] for i in range(N)] for j in range(M)])
sure_face = deBézierFace(samples)

# Go, figure!
ax = plt.figure().add_subplot(111, projection = '3d')
plt.tight_layout()
ax.plot_surface(*(sure_face[:, :, d] for d in range(3)), cmap = 'terrain') # À la da Vinci: https://en.wikipedia.org/wiki/Hypsometric_tints#History
ax.set_title("Bizarre de Bézier's decor")
# Reflections anyone?
for c, l in zip(('x', 'y', 'z'), ('Longitude', 'Latitude', 'Altitude')):
     eval(f'ax.set_{c}label')(l)
plt.show()