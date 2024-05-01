# https://matplotlib.org/stable/gallery/widgets/slider_demo.html
# https://en.wikipedia.org/wiki/B%C3%A9zier_curve

import matplotlib.pyplot as plt
from numpy import linspace as lp, outer as op, tensordot as tp
from matplotlib.widgets import Button, Slider
from sys import argv as controlPoints

# See e.g. https://stackoverflow.com/questions/26560726/python-binomial-coefficient
#          https://en.wikipedia.org/wiki/Binomial_coefficient
#          https://en.wikipedia.org/wiki/Bernstein_polynomial #Approximating_continuous_functions
def bézier(P, p = 128):
    binomial = lambda n, k: 1 if k == 0 or n == k else binomial(n - 1, k - 1) + binomial(n - 1, k)
    BernsteinPoly = lambda u = lp(0, 1, p), P = P, n = len(P): zip(*((binomial(n - 1, i), op(P[i], (1 - u)**(n - i - 1) * u**i)) for i in range(n))) 
    
    c, b = BernsteinPoly()
    return tp(c, b, 1)

##  Special case: a (cubic polynomial) Bézier curve (see also 'rationalBézier.py')
# https://www.pbr-book.org/4ed/Shapes/Curves
def bézier3(P, p = 128):
    u, (p0, p1, p2, p3), = lp(0, 1, p), P
    return op(p0, (1 - u)**3) + op(p1, 3*u * (1 - u)**2) + op(p2, 3*(1 - u) * u**2) + op(p3, u**3)

## User-defined control points:  python ./deBézier.py '[[0, 0], [1/8, -1], [1/4, 1], [1/2, -2], [3/4, 1], [7/8, -1], [1, 0]]'
P = [[0, 0], [1/2, 1/2], [1, 0]] if len(controlPoints) < 2 else eval(controlPoints[1])
pp, cp, hP = bézier(P), tuple(zip(*P)), len(P) >> 1

# Create the figure and a Bézier curve that we will manipulate
fig, ax = plt.subplots(num = "[de]* Bézier curve demo"); plt.tight_layout()
curve, points, = ax.plot(pp[0], pp[1], '-', cp[0], cp[1], 'k.')
ax.set_xlabel('X'), ax.set_ylabel('Y')

# Adjust the main plot to make room for the sliders
fig.subplots_adjust(top = 11/12, right = 11/12, left = 1/6, bottom = 1/6)
# Make sliders to control p₁
x_ax = fig.add_axes([0.25, 0.06125, 0.6125, 0.0125])
x_slider = Slider(label = 'p₁.X',
    ax = x_ax,
    valmin = -2, valmax = 2, valinit = P[hP][0], valstep = 0.01)

y_ax = fig.add_axes([0.04, 0.25, 0.0125, 0.6125])
y_slider = Slider(label = 'p₁.Y',
    ax = y_ax, orientation = "vertical",
    valmin = -2, valmax = 2, valinit = P[hP][1], valstep = 0.01)

# The function to be called anytime a slider's value changes
def update(_):
    global fig, x_slider, y_slider, P, hP, curve, points
    P[hP][0], P[hP][1] = x_slider.val, y_slider.val
    pp, cp = bézier(P), tuple(zip(*P))

    curve.set_xdata(pp[0]),  curve.set_ydata(pp[1])
    points.set_xdata(cp[0]), points.set_ydata(cp[1])
    fig.canvas.draw_idle()

# Register the update function with each slider
x_slider.on_changed(update), y_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.03125, 0.05, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor = '0.975')

def reset(_):
    x_slider.reset(), y_slider.reset()
    
button.on_clicked(reset)
plt.show() #... must go on!
