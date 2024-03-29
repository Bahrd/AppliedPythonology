from numpy.random import rand, randn, randint
from numpy.linalg import norm as np_norm
from numpy import arange, cos, kron, mat, r_ as rng, round
from math import pi as π

from cvxpy import Problem, Minimize, Variable
from cvxpy import norm as cvx_norm, CLARABEL as CLB
from auxiliary import displayPlotsXY

# Main function stuff                 # MATLAB's origins
def m(X, A):                          # function Y = m(X, A)
    L = arange(A.size)                #   L  = length(A);
    Φ = cos(kron(X, L))               #   Φ = cos(kron(X, 1:L));
    return Φ @ A                      #   Y  = Φ * A;

## Measurements (note N << L - the one way around...)
α = randint(-2, 3, (6, 1))             # α = randi([-2, 3], 6, 1);
R = 1; ρ = np_norm(α, 1) * R
N  = 128; X = π*(2 * rand(N, 1) - 1)  # if randint(2) else randn(N, 1) 
X, Z = sorted(X), randn(N, 1) * 0.125
Y = m(X, α) + Z
## Regressors matrix (note L >> N - the other way around...) 
L  = 512; Φ = cos(kron(X, arange(L))) # Φ = cos(kron(X, 1:L)); 

#Python CVX                                 # MATLAB CVX
                                            # cvx_begin quiet
A = Variable((L, 1))                        #  variable A(L) 
o = Minimize(cvx_norm(Φ @ A - Y, 2))        #  minimize(norm(Φ * A - Y, 2)) 
c = [cvx_norm(A, 1) <= ρ]                   #  subject to norm(A, 1) <= ρ
p = Problem(o, c); p.solve(solver = CLB)    # cvx_end

## Presentation stuff
Q = mat(rng[-3: 3: 3e-3]).T; YY = m(Q, A.value)
print(' A = ', round(A.value[:α.size], 2).T, 
      ' α = ',                       α.T)
ttl = f'arg min‖Φ*A-Y‖₂² st. ‖A‖₁ ≤ {ρ} → A = {round(A.value[:α.size]).T}'
displayPlotsXY([(X, Y), (Q, YY)], ['(X, Y)', ttl])
