# https://matplotlib.org/stable/gallery/widgets/slider_demo.html
# https://www.pbr-book.org/4ed/Shapes/Curves

import matplotlib.pyplot as plt
from numpy import linspace as lp, outer as op, tensordot as td
from matplotlib.widgets import Button, Slider

def bézier(p0, p1, p2, p3, n = 128):
    u = lp(0, 1, n)
    # 'outer' and 'tensordot' because... why not?
    b = ( op(p0, (1 - u)**3),   op(p1, u*(1 - u)**2), 
          op(p2, (1 - u)*u**2), op(p3, u**3))
    return td([1, 3, 3, 1], b, 1)
    # A likely faster one-liner...
    # return (op(p0, (1 - u)**3) + op(p1, 3*u * (1 - u)**2) + op(p2, 3*(1 - u) * u**2) + op(p3, u**3))

# A pair of pairs of the end- and control-points, that is (p₀, p₁, p₂, p₃)
P = [[0, 0], [1/4, -1/2], [3/4, 3/4], [1, 0]]
pp, cp = bézier(*P), tuple(zip(*P))

# Create the figure and a Bézier curve that we will manipulate
fig, ax = plt.subplots(num = "de Bézier curve demo")
curve, points, = ax.plot(pp[0], pp[1], '-', cp[0], cp[1], 'k.')
ax.set_xlabel('X'), ax.set_ylabel('Y')

# Adjust the main plot to make room for the sliders
fig.subplots_adjust(top = 11/12, right = 11/12, left = 1/6, bottom = 1/6)
# Make sliders to control p₁
x_ax = fig.add_axes([0.25, 0.06125, 0.6125, 0.0125])
x_slider = Slider(label = 'p₁.X',
    ax = x_ax,
    valmin = -1, valmax = 2, valinit = P[1][0], valstep = 0.01)

y_ax = fig.add_axes([0.04, 0.25, 0.0125, 0.6125])
y_slider = Slider(label = 'p₁.Y',
    ax = y_ax, orientation = "vertical",
    valmin = -1, valmax = 2, valinit = P[1][1], valstep = 0.01)

# The function to be called anytime a slider's value changes
def update(_):
    P[1][0], P[1][1] = x_slider.val, y_slider.val
    pp, cp = bézier(*P), tuple(zip(*P))

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
