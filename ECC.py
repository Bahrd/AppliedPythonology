''' ECC, Koblitz & Miller, 1985
Elliptic-curve cryptography
https://en.wikipedia.org/wiki/Schoof%27s_algorithm
https://en.wikipedia.org/wiki/Elliptic_curve#Elliptic_curves_over_finite_fields
https://link.springer.com/book/10.1007/978-3-642-04101-3 - Chapter 9 [in person: https://youtu.be/vnpZXJL6QCQ?t=111 ]
'''

from matplotlib.pyplot import scatter as scat, title, show, contour
from itertools import product
from numpy.random import rand
from numpy import ogrid

''' A few examples of elliptic curves 
    (incl. instances of the Weiestrass equation $(y^2 = x^3 + ax + b) mod q$):
    ++ for kids $(y^2 = x^3 + 2x + 2) mod 17$ 
    + for teens $(y^2 = x^3 + 3x + 7) mod 2503$
    
    It is not obvious how many integer solutions each of these equations has: 
    see Hasse's theorem: https://en.wikipedia.org/wiki/Hasse%27s_theorem_on_elliptic_curves
        $|N - (q + 1)| \leq 2\sqrt{q}$, 
    where $N$ is the number of points on the curve over a finite field of order $q$.
    
    But... To make the elliptic curves more, well, straightforward: 
    see e.g. https://link.springer.com/book/10.1007/978-1-4615-5207-9, p. 13, 
    let's start from drawing them for real (well, almost) numbers, shall we?
    https://stackoverflow.com/a/19757132/17524824  
 '''

# Real curves...
params = ((1, 0, 0), 'red'), ((0, -1, 0), 'brown'), ((0, 0, 0), 'orange'), ((0, 1, 1), 'black')
y, x = ogrid[-2:2:200j, -1.5:2.5:200j]

for (c, a, b), color in params:
    contour(x.ravel(), y.ravel(), x**3 + c*x**2 + a*x + b - y**2, [0], colors = color)
_ = title('Elliptic curves'); show()

# and the promised [more] rational ones...  
params = (17, (2, 2), 'cividis'), (331, (3, 3), 'ocean'), (2503, (3, 7), 'twilight')
for q, (a, b), cm in params:
    # Elliptic curve points (x, y) for a given equation
    ec = [(x, y) for (x, y) in product(range(q), range(q)) if 0 == (x**3 + a*x + b - y**2) % q]
    # Scatter plot data (re)arrangement(s)
    cc, ce = rand(len(ec)), tuple(zip(*ec))
    xy = (eval(f'ce[{_}]') for _ in (0, 1))
    # Have you noticed how the plot tickens? ;)
    _ = scat(*xy, c = cc, cmap = cm, alpha = 0.75), title(f'group order = {len(ec)} + 1 for {q = }'), show()