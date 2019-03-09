from numpy.random import randn, randint; from numpy.linalg import norm
from numpy import arange, cos, kron, mat, r_ as rng, round, stack

# Main function stuff                 # MATLAB origins
def m(X, A):                          # function Y = m(X, A)
    L = arange(A.size)                #   L  = length(A);
    Φ = cos(kron(X, L))               #   Φ = cos(kron(X, 1:L));
    return Φ @ A                      #   Y  = Φ * A;

## Measurements
α = randint(-2, 3, (6, 1))            # α = randi([-2, 3], 6, 1);
ρ = norm(α, 1)
N  = 128
X, Z = (randn(N, 1), randn(N, 1) * .25); Y = m(X, α) + Z
## Regressors matrix 
L  = 512; Φ = cos(kron(X, arange(L))) # Φ = cos(kron(X, 1:L)); 

from cvxpy import Problem, Minimize, Variable
from cvxpy import norm as cvx_norm
#Python CVX                           # MATLAB CVX
                                      # cvx_begin quiet
A = Variable(L)                       #  variable A(L) 
o = Minimize(cvx_norm(Φ @ A - Y, 2))  #  minimize(norm(Φ * A - Y, 2)) 
c = [cvx_norm(A, 1) <= ρ]             #  subject to norm(A, 1) <= ρ
p = Problem(o, c); p.solve()          # cvx_end

## Presentation stuff
from matplotlib.pyplot import plot, show

Q = mat(rng[-3: 3: 3e-3]).T; Y = m(Q, A.value)
plot(Q, Y); show()
print(" A = ", round(A.value[:α.size]).T, 
      " α = ",                       α.T)