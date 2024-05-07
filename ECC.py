'''
ECC, Koblitz & Miller, 1985
Elliptic-curve cryptography
https://en.wikipedia.org/wiki/Schoof%27s_algorithm
https://link.springer.com/book/10.1007/978-3-642-04101-3 - Chapter 9 [in person: https://youtu.be/vnpZXJL6QCQ?t=111 ]
'''

from matplotlib.pyplot import scatter as scat, title, show, contour
from itertools import product
from numpy.random import rand
from numpy import ogrid

''' Examples of elliptic curves (Weiestrass equation $(y^2 = x^3 + ax + b) mod q$):
    ++ for kids $(y^2 = x^3 + 2x + 2) mod 17$ 
    + for teens $(y^2 = x^3 + 3x + 7) mod 2503$
    
    It is interesting in general how many integer solutions these equations have, 
    but... let's start from drawing them for real, shall we?
    https://stackoverflow.com/a/19757132/17524824  
    To make the elliptic curves more, well, straightforward:
    see e.g. https://link.springer.com/book/10.1007/978-1-4615-5207-9, p. 13
'''

# Real curves...
coeffs = (1, 0, 0), (0, -1, 0), (0, 0, 0), (0, 1, 1)
for c, a, b in coeffs:
    y, x = ogrid[-4:4:100j, -4:4:100j]
    contour(x.ravel(), y.ravel(), x**3 + c*x**2 + a*x + b - y**2, [0])
    title(f'Elliptic curve $x³ + {c}x² + {a}x + {b} - y² = 0$')
    show()

# and the rational ones...  
params = (17, 2, 2, 'cividis'), (2503, 3, 7, 'twilight')
for q, a, b, cm in params:
    # Elliptic curve points (x, y) for a given equation
    ec = [(x, y) for (x, y) in product(range(q), range(q)) if 0 == (x**3 + a*x + b - y**2) % q]
    # Scatter plot data (re)arrangement(s)
    cc, ce = rand(len(ec)), list(zip(*ec))
    xy = (eval(f'ce[{_}]') for _ in (0, 1))
    # Where the plot tickens...
    _ = scat(*xy, c = cc, cmap = cm), title(f'group order = {len(ec)} + 1'), show()
