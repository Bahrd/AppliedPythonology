from matplotlib.pyplot import plot, polar, title, show
from math import pi as π
from numpy import cos, sin, sqrt, linspace as lsp, arange, reciprocal as rp

#Polar square...
for x, f, s in zip(arange(-π/4, 7/4*π, π/2), (cos, sin, cos, sin), (1, 1, -1, -1)):
    θ = lsp(x, x + π/2, 2) # 2?!?
    r = rp(f(θ)) * s
    polar(θ, r)
title('Polar square') 
show()

#Polygon circle...
x = lsp(0.0, sqrt(0.5), 16) # 16?!?
y = sqrt(1.0 - x**2)
for xy in (( x,  y), ( y,  x), 
           ( x, -y), (-y,  x), 
           (-x, -y), (-y, -x), 
           (-x,  y), ( y, -x)):
    plot(*xy)
title('Polygon circle') 
show()
