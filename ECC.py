r''' ECC (Elliptic-curve cryptography) by Koblitz & Miller, 1985
+ [Silverman, Tate - Rational Points on Elliptic Curves](https://link.springer.com/book/10.1007/978-3-319-18588-0) - Chapter 4
+ [Paar *et al.* - Understanding Cryptography](https://link.springer.com/book/10.1007/978-3-662-69007-9) - Chapter 9
+ https://en.wikipedia.org/wiki/Schoof%27s_algorithm
+ https://en.wikipedia.org/wiki/Elliptic_curve#Elliptic_curves_over_finite_fields
'''
from matplotlib.pyplot import scatter as scat, title, show, contour, subplots, subplot, plot
from matplotlib import colormaps as cmps
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

fig, dx = subplots(num = 'Elliptic curve demo x³ + ax² + bx¹ + cx⁰ = y²')
dx.set_xlabel('X'), dx.set_ylabel('Y')
dx.contour(x, y, z, [0])
title(f'x³ = y², Δ = {round(-16*(4*a**3 + 27*b**2), 1):.1f}')
    
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left = 1/5, bottom = 1/6)
# Insert sliders to control a, b, and c
_sp_ = (([0.25, 0.06125, 0.6125, 0.0125], 'a', 'horizontal'),
        ([0.06125, 0.25, 0.0125, 0.6125], 'b', 'vertical'),
        ([0.93875, 0.25, 0.0125, 0.6125], 'c', 'vertical'))
a_slider, b_slider, c_slider = (Slider(ax = fig.add_axes(_a), label = _l, orientation = _o,
                                       valmin = -3, valmax = 3, valinit = 0, valstep = .1)
                                for _a, _l, _o in _sp_)
# Real el'curves...
def update(_):
    global x, y
    a, b, c = a_slider.val, b_slider.val, c_slider.val
    z = x**3 + a*x**2 + b*x + c - y**2
    dx.cla()

    cc = f'#{randint(100):02}{randint(100):02}{randint(100):02}'
    contour(x, y, z, [0], colors = cc)
    
    # Anonymous poly-formatting 
    sg = lambda a: '+' if a > 0 else '—'
    ao = lambda a, _: f'{abs(round(a) if round(a, 0) == round(a, 1) else round(a, 1))}' if abs(a) != 1 else '' if _ != '' else '1'
    dsp = lambda a, _: f'{ sg(a)} {ao(a, _)}{_}' if a else '' 
    title(f'x³ {dsp(a, "x²")}{dsp(b, "x")}{dsp(c, "")} = y², Δ = {round(-16*(4*a**3 + 27*b**2), 1):.1f}')

# register the update function with each slider
for _slider in (a_slider, b_slider, c_slider): _slider.on_changed(update)
subplot(1, 1, 1); show() #... must go on!

# Let's move on to the integer solutions of the elliptic curves
# and the promised [more] rational ones...  

params = (17, (2, 2), 'ocean'), (331, (3, 3), 'twilight'), (2503, (3, 7), 'terrain')
for q, (a, b), cm in params:
    # Elliptic curve points (x, y) for a given equation
    ec = [(x, y) for (x, y) in product(range(q), range(q)) if 0 == (x**3 + a*x + b - y**2) % q]
    # Scatter plot data (re)arrangement(s)
    cc, ce = rand(len(ec)), tuple(zip(*ec))
    xy = (eval(f'ce[{_}]') for _ in (0, 1))
    # Have you already noticed how the plot tickens? ;)
    cmn = cmps[cm].resampled(0x100)
    _ = scat(*xy, c = cmn(cc), alpha = 0.75), title(f'group order = {len(ec)} + 1 for {q = }'), show()

r'''
 Now, we are talking...
 https://en.wikipedia.org/wiki/File:ECClines.svg        
 https://en.wikipedia.org/wiki/Elliptic_curve#Elliptic_curves_over_finite_fields    
 And again... https://link.springer.com/book/10.1007/978-3-662-69007-9
 
 See pp. 244nn of the book: Note that we start with doubling of G (a point on a curve with integer coordinates) and then we just add 
 G's (it remains magic [to me] that the other points are integer, too ("but that's apparently the beauty of elliptic curves" ;))

       2G = G + G, 3G = 2G + G, ..., nG = (n - 1)G + G, etc.

 nG encrypts the private key n with the help of the publicly known quadruplet (a, b, q, G)
 They say finding n given nG is infeasible (and we need to believe them...)
'''

### An example taylored to the following parameters:
a, b, q = 2, 2, 17
_1G = (5, 1)        # A primitive element... (incidentally - the first element of the sequence - for educational purposes)
# Not the elegant solution to the problem of default argument values (in fact, a solution to create problems... ;)
def add(P, Q = _1G, a = a, q = q):
    x1, y1, x2, y2 = *P, *Q
    ## A slope (tangent for doubling, "secant for adding": https://en.wikipedia.org/wiki/Secant_line) - ThnX, Copilot!
    #  There is no need to mess around with arguments here...
    def s(x1 = x1, y1 = y1, x2 = x2, y2 = y2, a = a, q = q): 
        # Observe that 'pow(x, -1, q)' computes the multiplicative inverse of $x mod q$
        return (y2 - y1) * pow(x2 - x1, -1, q) % q if (x1, y1) != (x2, y2) else (3 * x1**2 + a) * pow(2 * y1, -1, q) % q

    ### <Don't do this at home!...>
    # if x1 == x2 and y1 != y2: return _1G
    ### </Don't do this at home!...>
    m = s()
    x3 = (m**2 - x1 - x2) % q
    y3 = (m * (x1 - x3) - y1) % q
    # Why there is no constant 'b' anymore here?;)
    return x3, y3

r'''
_1G = (5, 1)
# ♪♫ Gimme more, gimme more...♫♪ [ https://www.youtube.com/watch?v=P51IVqf28Hs or https://www.youtube.com/watch?v=lhdiQ8isyLo ]
_2G = add(_1G, _1G); _3G = add(_1G, _2G)
_4G = add(_1G, _3G); _5G = add(_1G, _4G)
# Noch zweimal...
_6G, _7G = add(_1G, _5G), add(_1G, add(_1G, _5G))
'''

# But everyone can be "smarter every day"... and "I told you: EVERY!ONE!!" [ https://youtu.be/74BzSTQCl_c?t=4 ]
# https://stackoverflow.com/questions/46617233/how-to-create-a-varying-variable-name-in-python
print(f'1G = {_1G}', end = ', ')   
for n in range(2, 19):                                  # ♪♫ You [should] run on for a long time [ https://youtu.be/eJlN9jdQFSc ]
    globals()[f'_{n}G'] = add(globals()[f'_{n - 1}G'])  #    run on for a long time...♫♪ [ https://youtu.be/9o6RyF9kXoA?t=160 ]
    print(f'{n}G = {globals()[f"_{n}G"]}', end = ', ') 

## We manually add the point at infinity (that is, the neutral element of the group - like '0' in the "normal" sense):
#  because (5, 1) + (5, 16) = 0 and - as "zero" - it naturally denotes "infinity". Yeah, yeah...
print('19G = 0')    # By the way, how few steps are needed to reach infinity these days...

## Another example... (this time with a different curve)
a, b, q = 3, 3, 331
G = (7, 6); GG = [G]
print(f'{G = }')   
for n in range(1, 333):
    GG.append(add(GG[n - 1], G, a, q))
    

from matplotlib.pyplot import rcParams, cycler, cm
rcParams["axes.prop_cycle"] = cycler("color", cm.cividis.colors)

#  How about that? Does it look random - at least to the naked eye?...
#  (Okay, those wearing glasses can also take a look...;)
for n in range(1, 333 - 1):
    _ = plot((GG[n - 1][0], GG[n][0]), (GG[n - 1][1], GG[n][1]))
_ = title('A Brownian motion (kind of?) over an elliptical curve...'), show()

## From now on, everyone can use the ECC in DHM (see p. 250) to create the 
#  the private key to use in e.g. the DES/AES scheme. Because:
#  ♪♫ What's down in the dark will be brought to the light ♫♪ [ https://youtu.be/eJlN9jdQFSc?t=126 ]

## https://datatracker.ietf.org/doc/html/rfc6090 - homogeneous coordinates to avoid multiplicative inverses