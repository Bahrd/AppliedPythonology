'''
ECC, Koblitz & Miller, 1985
Elliptic-curve cryptography
https://en.wikipedia.org/wiki/Schoof%27s_algorithm
https://link.springer.com/book/10.1007/978-3-642-04101-3 - Chapter 9 [in person: https://youtu.be/vnpZXJL6QCQ?t=111 ]
'''

from matplotlib.pyplot import scatter, show
from itertools import product
from numpy.random import rand

## Examples of elliptic curves (Weiestrass equation $(y^2 = x^3 + ax + b) mod q$):
#  ++ for kids $(y^2 = x^3 + 2x + 2) mod 17$ 
#  + for teens $(y^2 = x^3 + 3x + 7) mod 2503$

data = (17, 2, 2, 'cividis'), (2503, 3, 7, 'twilight')
for q, a, b, cm in data:
    # Elliptic curve points (x, y) for the given equation
    ec = [(x, y) for (x, y) in product(range(q), range(q)) if 0 == (x**3 + 3*x + 7 - y**2) % q]
    # Scatter plot data (re)arrangement(s)
    cc, ec = rand(len(ec)), list(zip(*ec))
    xy = (eval(f'ec[{_}]') for _ in (0, 1))
    # And the plot tickens...
    scatter(*xy, c = cc, cmap = cm); show()
