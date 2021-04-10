from matplotlib.pyplot import hist, show, title, legend
from numpy.random import poisson
from numpy import sqrt, ones

## Mathemagically...
anscombe = lambda p: 2 * sqrt(p + .375)
    
λ, N = 0x10, 0x400
Λ = λ * ones(N)

P = poisson(Λ)
G = anscombe(P)

_ = (hist((P, G), range(λ << 0b10), density = True), 
     title(f'Poissonian distribution and its Gaussian-like counterpart (with σ² ≈ 1)'), 
     legend((f'Poisson, λ = {λ} ', f'Gauss, m = {anscombe(λ):,.0f}')))
show()