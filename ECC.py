r''' ECC, Koblitz & Miller, 1985
Elliptic-curve cryptography
https://en.wikipedia.org/wiki/Schoof%27s_algorithm
https://en.wikipedia.org/wiki/Elliptic_curve#Elliptic_curves_over_finite_fields
https://link.springer.com/book/10.1007/978-3-642-04101-3 - Chapter 9 [in person: https://youtu.be/vnpZXJL6QCQ?t=111 ]
'''
from matplotlib.pyplot import scatter as scat, title, show, contour, subplots, subplot
from itertools import product
from numpy.random import rand, randint
from numpy import linspace as lp, meshgrid
from matplotlib.widgets import Slider
r''' A few examples of elliptic curves 
    (incl. instances of the Weiestrass equation $(y^2 = x^3 + ax + b) mod q$):
    ++ for kids $(y^2 = x^3 + 2x + 2) mod 17$ 
    + for teens $(y^2 = x^3 + 3x + 7) mod 2503$
    
    It is not obvious how many integer solutions each of these equations has: 
    see Hasse's theorem: https://en.wikipedia.org/wiki/Hasse%27s_theorem_on_elliptic_curves
        $|N - (q + 1)| \leq 2\sqrt{q}$, 
    where $N$ is the number of points on the curve over a finite field of order $q$.
    
    But... To make the elliptic curves more, well, straightforward: 
    see e.g. https://link.springer.com/book/10.1007/978-1-4615-5207-9, p. 13, 
    let's start from drawing them for real(-like) numbers, shall we?
    https://stackoverflow.com/a/19757132/17524824  
 '''


# Create an elliptic curve
y, x = meshgrid(lp(-3, 3, 0x200), lp(-3, 3, 0x200))
a, b, c = 0, 0, 0
z = x**3 + a*x**2 + b*x + c - y**2

fig, dx = subplots(num = 'Elliptic curve demo x³ + ax² + bx¹ + cx⁰ = y³')
dx.set_xlabel('X'), dx.set_ylabel('Y')
dx.contour(x, y, z, [0])
title(f'x³ = y³')
    
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left = 1/5, bottom = 1/6)
# Make sliders to control a, b, and c
_sp_ = (([0.25, 0.06125, 0.6125, 0.0125], 'a', 'horizontal'),
        ([0.06125, 0.25, 0.0125, 0.6125], 'b', 'vertical'),
        ([0.93875, 0.25, 0.0125, 0.6125], 'c', 'vertical'))
x_slider, y_slider, z_slider = (Slider(ax = fig.add_axes(_a), label = _l, orientation = _o,
                                       valmin = -3, valmax = 3, valinit = 0, valstep = .1)
                                for _a, _l, _o in _sp_)
# Real curves...
def update(_):
    global a, b, c, x, y
    a, b, c = x_slider.val, y_slider.val, z_slider.val
    z = x**3 + a*x**2 + b*x + c - y**2
    dx.cla()

    cc = f'#{randint(100):02}{randint(100):02}{randint(100):02}'
    contour(x, y, z, [0], colors = cc)
    
    # Anonymous poly-formatting 
    sg = lambda a: '+' if a > 0 else '—'
    ao = lambda a, _: f'{abs(round(a) if round(a, 0) == round(a, 1) else round(a, 1))}' if abs(a) != 1 else '' if _ != '' else '1'
    dsp = lambda a, _: f'{ sg(a)} {ao(a, _)}{_}' if a else '' 
    title(f'x³ {dsp(a, "x²")}{dsp(b, "x")}{dsp(c, "")} = y³')

# register the update function with each slider
x_slider.on_changed(update), y_slider.on_changed(update), z_slider.on_changed(update)
subplot(1, 1, 1); show() #... must go on!



# Now, let's move on to the integer solutions of the elliptic curves
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
    

# Now, we are talking...
# https://en.wikipedia.org/wiki/File:ECClines.svg        
# https://en.wikipedia.org/wiki/Elliptic_curve#Elliptic_curves_over_finite_fields    
# https://youtu.be/F3zzNa42-tQ?t=722    