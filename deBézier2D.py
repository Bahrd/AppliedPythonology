## Copilot'ed... See also: https://www.youtube.com/watch?v=QuY1hfd6zJk for a MATLAB flavor

import numpy as np
from random import random
from matplotlib import pyplot as plt

## Pretentious homonyms mode ON...
def deBézier_face(samples, u_steps = 128, v_steps = 128):
   def bernstein_poly(i, n, t):
      return binomial_coeff(n, i) * (t ** i) * ((1 - t) ** (n - i))

   def binomial_coeff(n, k):
      if k == 0 or k == n: return 1
      return binomial_coeff(n - 1, k - 1) + binomial_coeff(n - 1, k)

   u, v = np.linspace(0, 1, u_steps), np.linspace(0, 1, v_steps)
   U, V = np.meshgrid(u, v)
   n, m, _ = samples.shape

   sure_face = np.zeros((u_steps, v_steps, 3))
   for i in range(n):
      for j in range(m):
         sure_face += np.outer(bernstein_poly(i, n - 1, U) * bernstein_poly(j, m - 1, V),
                               samples[i, j]).reshape(u_steps, v_steps, 3)
   return sure_face

# An NxM grid of samples of a surface
N, M = 8, 16
samples = np.array([[[i, j, 2*random() - 1] for i in range(N)] for j in range(M)])
sure_face = deBézier_face(samples)

# Go, figure!
ax = plt.figure().add_subplot(111, projection = '3d')
plt.tight_layout()
ax.plot_surface(*(sure_face[:, :, d] for d in range(3)), cmap = 'terrain') # À la da Vinci: https://en.wikipedia.org/wiki/Hypsometric_tints#History
ax.set_title("Bizarre de Bézier's decor")
# Reflections anyone?
for c, l in zip(('x', 'y', 'z'), ('Longitude', 'Latitude', 'Altitude')):
     eval(f'ax.set_{c}label')(l)
plt.show()