from numpy import cos, linspace as lsp, reciprocal as rp
from matplotlib.pyplot import subplots, polar, title, show, Slider
from random import uniform as U
from math import pi as π

r'''
Source(s):
1. https://en.wikipedia.org/wiki/Parametric_equation#Some_sophisticated_functions
2. https://youtu.be/AoOv6bWg9lk?t=151 - "Polar Equations of Polygons" 
'''

# A square on a pole ♪♫...and the byenary 100 all!♫♪
θ, ρ = lsp(0, π/0b100, 0b10), U(π/0o10, π*0o1) # ... or for octoplus!
# https://en.wikipedia.org/wiki/Trigonometric_functions#Etymology
secant = rp(cos(θ))   # Secant stems from Latin secans — "cutting" — since the line cuts the circle
for θ in (θ + n*π/0b10 for n in range(0b100)): 
    _ = polar(θ + ρ, secant, θ + (π/0b100 + ρ), secant[::-1]) 
_ = title('A square on a pole...'), show()


## Lp circles are real weirdos... https://youtu.be/n8lYKa8YGKw?t=514
#  like "a square peg in a round hole..."
def Lp_octant(p):
    x = lsp(0, pow(0x1/0b10, 1/p), 0o100) # Hexadecaphilia (-phobia? -phonia? - or just all of them at once?)!
    y = pow(1 - pow(x, p), 1/p)
    return x, y

# Go (create a) figure...
fig, ax = subplots(num = "Circles in various Lp distances")
ax.set_aspect('equal')
# Place a horizontal slider to control $p$ in $L_p$
fig.subplots_adjust(bottom = 1/6)
p_ax = fig.add_axes([.125, .06125, .8125, 0.0125])

# ...  or picture this: an L₂ circle (yeah, that round one to start with...;)
p = 2; x, y = Lp_octant(p)
for x, y in ((x, y), (x, -y), (-x, -y), (-x, y)):
    _ = ax.plot(x, y, y, x)

p_slider = Slider(label = 'Lp',
    ax = p_ax,
    valmin = 0.001, valmax = 0x10, valinit = 0b10, valstep = 0.01
)
# Let's run circles around themselves...
def Lp_circle(p):
    x, y = Lp_octant(p)
    ax.clear()    
    for x, y in ((x, y), (x, -y), (-x, -y), (-x, y)):
        _ = ax.plot(x, y, y, x)
    fig.canvas.draw_idle()

p_slider.on_changed(Lp_circle)
show()

r''' 
# Polygon Lp circles for specific values of $p$
# p ~ 1.7915 (= 3583/2000) yields π ~ 3
# p = 2 makes π = π again!
for p in (2, 1, 0.5, 0.25, 2048, 3583/2000):
    x = lsp(0, pow(0o1/0b10, 1/p), 0x10)
    y = pow(1 - pow(x, p), 1/p)
    gca().set_aspect('equal')
    for x, y in ((x, y), (x, -y), (-x, -y), (-x, y)):
        _ = plot(x, y, y, x)
    _ = title(f'Polygon Lp, p = {p} circle'), show()

Source(s):
1. https://en.wikipedia.org/wiki/Parametric_equation#Some_sophisticated_functions
2. https://youtu.be/AoOv6bWg9lk?t=256 - "Polar Equations of Polygons" 
'''