# https://matplotlib.org/stable/gallery/widgets/slider_demo.html
# https://www.pbr-book.org/4ed/Shapes/Curves

import matplotlib.pyplot as plt
from numpy import linspace as lp, outer as op
from matplotlib.widgets import Button, Slider

def bézier(p0, p1, p2, p3, n = 128):
    u = lp(0, 1, n)
    b = ( op(p0, (1 - u)**3)       + op(p1, 3*u * (1 - u)**2) 
        + op(p2, 3*(1 - u) * u**2) + op(p3, u**3))
    return b

# A pair of pairs of the end- and control-points
P = [[0, 0], [.25, -.5], [.75, .75], [1, 0]]
pp, cp = bézier(*P), tuple(zip(*P))

# Create the figure and a Bézier curve that we will manipulate
fig, ax = plt.subplots(num="de Bézier curve demo")
curve, points, = ax.plot(pp[0], pp[1], '-', cp[0], cp[1], 'k.')
ax.set_xlabel('X'), ax.set_ylabel('Y')
# ax.set_xlim(0, 1), ax.set_ylim(-1, 1)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left = 0.25, bottom = 0.25)
# Make a horizontal slider to control the p1.X
x_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
x_slider = Slider(
    ax = x_ax,
    label = 'p₁.X',
    valmin = -1,
    valmax = 2,
    valinit = P[1][0],
    valstep = 0.01
)
# Make a vertically oriented slider to control p1.Y
y_ax = fig.add_axes([0.1, 0.25, 0.03, 0.65])
y_slider = Slider(
    ax = y_ax,
    label = 'p₁.Y',
    valmin = -1,
    valmax = 2,
    valinit = P[1][1],
    orientation = "vertical",
    valstep = 0.01
)

# The function to be called anytime a slider's value changes
def update(_):
    P[1][0], P[1][1] = x_slider.val, y_slider.val
    pp, cp = bézier(*P), tuple(zip(*P))

    curve.set_xdata(pp[0]),  curve.set_ydata(pp[1])
    points.set_xdata(cp[0]), points.set_ydata(cp[1])
    fig.canvas.draw_idle()

# register the update function with each slider
x_slider.on_changed(update), y_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor = '0.975')

def reset(_):
    x_slider.reset(), y_slider.reset()
    
button.on_clicked(reset)
plt.show() #... must go on!
