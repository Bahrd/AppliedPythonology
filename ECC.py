'''
ECC, Koblitz & Miller, 1985
Elliptic-curve cryptography
https://en.wikipedia.org/wiki/Schoof%27s_algorithm
https://link.springer.com/book/10.1007/978-3-642-04101-3 - Chapter 9
'''

from matplotlib.pyplot import imshow, show, scatter 
from numpy import reshape
from itertools import product

## Examples of elliptic curves
# For kids... (Weiestrass equation: $(y^2 = x^3 + 2x + 2) mod 17$)
q = 17
ec = list(zip(*[(x, y) for (x, y) in product(range(q), range(q)) if not (x**3 + 2*x + 2 - y**2)%q]))
scatter(ec[0], ec[1], s = 1); show()

# For teens... (Weiestrass equation: $(y^2 = x^3 + 3x + 7) mod 2503$)
q = 2503
ec = list(zip(*[(x, y) for (x, y) in product(range(q), range(q)) if not (x**3 + 3*x + 7 - y**2)%q]))
scatter(ec[0], ec[1], s = 1); show()