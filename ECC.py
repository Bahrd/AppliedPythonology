## ECC, Koblitz & Miller, 1985
#  Elliptic-curve cryptography

## https://en.wikipedia.org/wiki/Schoof%27s_algorithm

## Example (of Weiestrass equation): $y^2 = x^3 + 3x + 7 mod 2503$
#  Since we are interested in integer solutions, the above equation is a Diophantine one)
from matplotlib.pyplot import imshow, show 
from numpy import reshape
from itertools import product

q = 2503

ec = [(i**2)%q != (j**3 + 3*j + 7)%q for (i, j) in product(range(q), range(q))]
ec = reshape(ec, (q, q))

imshow(ec, cmap = 'gray'); show()