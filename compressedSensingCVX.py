## https://www.ti.rwth-aachen.de/~behboodi/src/papers/introduction_to_CS.pdf
# and some sources...
## https://groups.google.com/g/wncc_iitb/c/6AzF1lCN0Zs?pli=1
## https://jrom.ece.gatech.edu/index-8/
## https://community.wolfram.com/groups/-/m/t/246929

## CSA - COMPRESSIVE SENSING [COMPRESSED SAMPLING] ALGORITHM 
#  1. $m$ - an image vector in a canonical (pixel) base
#  2. $y$ - a vector of linear measurements (inner products) $y = \fi * m$ 
#  3. $\beta$ - a representation of $m$ in a sparse base $\psi$; $m = \psi * \beta$ (i.e. a 'transform' of $m$)
#  
#  Observe:
#  I.  $\fi$ is (by design) a random matrix, however, once generated, it remains fixed during the experiment.
#      Therefore, we have $y = \theta * \beta$, where $\theta = \fi * \psi$ and $\theta * \b$ are the 
#      compressed measurements of the approximation of $m$ in each step of the optimization algorithm
#  II. If $\fi$ is an identity matrix then $y$ are just (samples of) $m$
### https://dsp.stackexchange.com/questions/61375/orthogonal-basis-for-a-2d-signals-compressive-sensing
import cvxpy as cvx; import cv2; import numpy as np

# 1.1 Import an image of interest
img = cv2.cvtColor(cv2.imread('./GrassHopper.png'), cv2.COLOR_BGR2GRAY)
N, K = 64, 128
img = cv2.resize(img, (N, N))
# 1.2 Converting a 2D image into a 1D vector (Huh?! A kinda dissapointing approach...)
img = np.reshape(img, -1)

# 2.1 Samples of an image 
np.random.seed(0x123456)
fi = np.random.choice([0, 1], (N * N, K))
# 2.2 Compressive measurements (in a canonical basis)
y = fi @ img
ρ = 1000

#Python CVX                           
                                      
#A = cvx.Variable((K, 1))              
#o = cvx.Minimize(cvx.cvx_norm(fi @ A - y, 2)) 
#c = [cvx.cvx_norm(A, 1) <= ρ]             
#p = cvx.Problem(o, c); p.solve()   



