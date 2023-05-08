from numpy import cos, sqrt, linspace as lsp, reciprocal as rp
from matplotlib.pyplot import plot, polar, title, show, gca
from math import pi as π
from random import uniform as U

##Polar square ♪♫...and the byenary 100 all!♫♪
θ, ρ = lsp(0, π/0b100, 0b10), U(π/0o10, π*0o1) # ... or for octoplus!
r = rp(cos(θ))   
for θ in (θ + n*π/0b10 for n in range(0b100)): 
    _ = polar(θ + ρ, r, θ + (π/0b100 + ρ), r[::-1]) 
_ = title('Polar square'), show()

#Polygon circle...
x = lsp(0, sqrt(0b10)/0b10, 0x10) # Hexadecaphilia!
y = sqrt(1 - x**0b10)
gca().set_aspect('equal')
for x, y in ((x, y), (x, -y), (-x, -y), (-x, y)):
    _ = plot(x, y, y, x)
_ = title('Polygon circle'), show()

''' 
Source(s):
1. https://en.wikipedia.org/wiki/Parametric_equation#Some_sophisticated_functions
2. https://www.youtube.com/watch?v=AoOv6bWg9lk - "Polar Equations of Polygons"
'''