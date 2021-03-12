from matplotlib.pyplot import plot, polar, title, show
from math import pi as π
from numpy import cos, sin, sqrt, linspace as lsp, arange, reciprocal as rp

##Polar square...
θ, ρ = lsp(0, π/0b100, 0b10), π/0o10 # Byenary 100 all! & Octoplus... ;)
r = rp(cos(θ))   
for _ in range(4):
    θ += π/2
    _ = polar(θ + ρ, r, θ + (π/4 + ρ), r[::-1]) # 'r[::-1]' or 'list(reversed(r))' 
_ = title('Polar square'), show()

#Polygon circle...
x = lsp(0.0, sqrt(0.5), 0x10) # Hexadecaphilia!
y = sqrt(1.0 - x**2)
for xy in (( x,  y), ( x, -y),
           (-x, -y), (-x,  y)):
    x, y = xy
    _ = plot(x, y, y, x)
_ = title('Polygon circle'), show()

### https://en.wikipedia.org/wiki/Parametric_equation#Some_sophisticated_functions