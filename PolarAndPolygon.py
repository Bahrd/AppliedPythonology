from matplotlib.pyplot import plot, polar, title, show
from math import pi as π
from numpy import cos, sin, sqrt, linspace as lsp, arange, reciprocal as rp

##Polar square...
θ = lsp(-π/4, 0, 2) # Byenary 100 all!
r = rp(cos(θ))
for φ in arange(0, 2*π, π/2):
    polar(θ + φ, r, θ + φ + π/4, r[::-1])
title('Polar square') 
show()

#Polygon circle...
x = lsp(0.0, sqrt(0.5), 0x10) # Hexadecaphilia!
y = sqrt(1.0 - x**2)
for xy in (( x,  y), ( x, -y),
           (-x, -y), (-x,  y)):
    x, y = xy
    plot(x, y, y, x)
title('Polygon circle')
show()