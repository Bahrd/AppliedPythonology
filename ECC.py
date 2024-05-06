'''
ECC, Koblitz & Miller, 1985
Elliptic-curve cryptography
https://en.wikipedia.org/wiki/Schoof%27s_algorithm
https://link.springer.com/book/10.1007/978-3-642-04101-3 - Chapter 9
'''

from matplotlib.pyplot import show, scatter 
from itertools import product
from numpy.random import rand

## Examples of elliptic curves (Weiestrass equation: $(y^2 = x^3 + ax + b) mod q$)
# For kids: $(y^2 = x^3 + 2x + 2) mod 17$
q = 17
ec = [(x, y) for (x, y) in product(range(q), range(q)) if 0 == (x**3 + 2*x + 2 - y**2)%q]
cc, ec = rand(len(ec)), list(zip(*ec)) # Data (re)arrangement for the scatter plot
scatter(ec[0], ec[1], c = cc, cmap = 'cividis')
show()

# For teens: $(y^2 = x^3 + 3x + 7) mod 2503$
q = 2503
ec = [(x, y) for (x, y) in product(range(q), range(q)) if 0 == (x**3 + 3*x + 7 - y**2)%q]
cc, ec = rand(len(ec)), list(zip(*ec))
scatter(ec[0], ec[1], c = cc, cmap = 'twilight'); show()
# Anyway... In general, how many solutions are there for these kind of equations? [https://en.wikipedia.org/wiki/Hasse%27s_theorem_on_elliptic_curves]