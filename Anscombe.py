from matplotlib.pyplot import hist, show
from numpy.random import poisson
from numpy import sqrt, ones

## Mathemagically...
anscombe = lambda p: 2 * sqrt(p + .375)
    
λ, N = 0x2, 0x400
Λ = λ * ones(N)

P = poisson(Λ)
G = anscombe(P)

_ = hist((P, G), range(λ << 0b10))
show()