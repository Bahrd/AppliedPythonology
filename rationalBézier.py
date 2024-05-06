## See e.g. https://en.wikipedia.org/wiki/B%C3%A9zier_curve #Rational_B%C3%A9zier_curves
#  It's just been implemented here! [cf. https://youtu.be/SoL3hPQHMqA?t=2094  ]

import matplotlib.pyplot as plt; from matplotlib.pyplot import show as Show
from numpy import linspace as lp, outer as op, tensordot as tp, multiply as hp, reciprocal as rp
from matplotlib.widgets import Button, Slider

def rationalBézier3(P, w, p = 128):
    assert len(P) == 3 and len(w) == 3, 'Works for a triplet of control points ¡ONLY!'
    
    u, n = lp(0, 1, p), len(P)
    # A triplet of internal helper functions for the triplet of control points
    binomial = lambda n, k: 1 if k == 0 or n == k else binomial(n - 1, k - 1) + binomial(n - 1, k)
    BernsteinPoly = lambda P: zip(*((binomial(n - 1, i), op(P[i], (1 - u)**(n - i - 1) * u**i)) for i in range(n)))
    deBézier = lambda: rp(w[0]*(1 - u)**2 + w[1]*2*(1 - u)*u + w[2] * u**2)
    
    # The main function body
    nuBézier, deBézier = tp(*BernsteinPoly(hp(P, list(zip(w, w)))), 1), deBézier()
    '''  Rationale = Bézier/deBézier '''
    return hp(nuBézier[0], deBézier), hp(nuBézier[1], deBézier)

# A pair of the endpoints and the control singleton between them)
P, w = [[0.0, 0], [1/2, 1/2], [1, 0]], [1, 0, 1]
pp, cp = rationalBézier3(P, w), tuple(zip(*P))

# Create the figure and a Bézier curve that we will manipulate
fig, ax = plt.subplots(num = "Rational 3-point Bézier curve demo"); plt.tight_layout()
curve, points = ax.plot(pp[0], pp[1], '-', cp[0], cp[1], 'k.')
ax.set_xlabel('X'), ax.set_ylabel('Y')

# Sliders' parameters
slider_locations = [0.25, 0.06125, 0.6125, 0.0125], [0.04, 0.25, 0.0125, 0.6125], [0.96, 0.25, 0.0125, 0.6125]
slider_parameters = ({'label': 'p₁.X', 'valmin': -1, 'valmax': 2, 'valinit': P[1][0], 'valstep': 0.1}, 
                     {'label': 'p₁.Y', 'valmin': -1, 'valmax': 2, 'valinit': P[1][1], 'valstep': 0.1, 'orientation': "vertical",}, 
                     {'label': 'w₁', 'valmin': -2, 'valmax': 2, 'valinit': w[1], 'valstep': 0.1, 'orientation': "vertical",})
# Adjust the main plot to make room for the sliders that control p₁.X, p₁.Y and w₁ parameters...
fig.subplots_adjust(top = 11/12, right = 11/12, left = 1/6, bottom = 1/6)
# ... and insert them
x_ax, y_ax, w_ax = (fig.add_axes(sl) for sl in slider_locations)
x_slider, y_slider, w_slider = (Slider(ax = ax, **sp) for ax, sp in zip((x_ax, y_ax, w_ax), slider_parameters))

# The event handler called back anytime the sliders' values change
def update(_):
    global fig, x_slider, y_slider, P, curve, points
    P[1][0],  P[1][1] = x_slider.val, y_slider.val
    w[1] = w_slider.val
   
    pp, cp = rationalBézier3(P, w), tuple(zip(*P))
        
    curve.set_xdata(pp[0]),  curve.set_ydata(pp[1])
    points.set_xdata(cp[0]), points.set_ydata(cp[1])
    fig.canvas.draw_idle()

# Register the update function for each slider
x_slider.on_changed(update), y_slider.on_changed(update), w_slider.on_changed(update)

# A `matplotlib.widgets.Button` resetting the sliders
resetax = fig.add_axes([0.03125, 0.05, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor = '0.975')
def reset(_):
    x_slider.reset(), y_slider.reset(), w_slider.reset()
button.on_clicked(reset)

## Et voilà!
# ♪♫
Show() # must go on! 
# ♫♪ 