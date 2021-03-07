from matplotlib.pyplot import plot, polar, title, show, figure, xticks, yticks
from math import pi as π
from numpy import cos, sin, sqrt, linspace as lsp, arange, reciprocal as rp

#Polar square...
for x, f, s in zip(arange(-π/4, 7/4*π, π/2), (cos, sin, cos, sin), (1, 1, -1, -1)):
    θ = lsp(x, x + π/4, 0b10) # Byenary 100 all!
    r = rp(f(θ)) * s
    polar(θ, r); polar(θ+ π/4, r[::-1])
title('Polar square') 
show()

#Polygon circle...
x = lsp(0.0, sqrt(0.5), 0x10) # Hexadecaphilia!
y = sqrt(1.0 - x**2)
for xy in (( x,  y), ( x, -y),
           (-x, -y), (-x,  y)):
    x, y = xy
    plot(x, y); plot(y, x)
title('Polygon circle')
show()