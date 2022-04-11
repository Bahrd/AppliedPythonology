## A convenience store...
from matplotlib.pyplot import hist, show
from numpy import array
from numpy.random import (rand as rnd, 
                          standard_normal as stdn, 
                          standard_cauchy as stdc)
# ... and a handy shorcut to it
def show_hist(m, b): 
    _ = hist(array(m), bins = b, density = True, rwidth = 0b1), show()

## A normal sum of some normal (yet different!) rvs
#  N(a, 1), N(b, 1) and N(c, 1) 
def summa(a = -0o4, b = 0o0, c = 0o4): 
    return (stdn() + a) + (stdn() + b) + (stdn() + c)
## A normal mixture - an example of a mixture distribution 
#  (of three otherwise normal rvs): N(a, 1) with prob. A, 
#  N(b, 1) with prob. B and N(c, 1) with prob. 1 - (A + B)
#  It can, for instance, be the output of the Markovian process 
#  with three internal (hidden) states (seen through the noise).
#  (In that case [A B 1 - B - A] can be its stationary distribution.)
def mixture(A  = 0.4, B = 0.4, a = -0x4, b = 0x4, c = 0x0): 
    m, s = rnd(), stdn()
    return s + (a if m < A else b if m < A + B else c)

M = [[mixture(), summa()] for _ in range(0o444 << 0o4)]
show_hist(array(M), 0o44)



## 'A blot [of Cauchy] on the [Gaussian] landscape'
#   i.e. some rather visciuos mixture/potion...
#   see: https://en.wikipedia.org/wiki/Mixture_distribution#A_normal_and_a_Cauchy_distribution
def Tukey_mixture(T  = 0.00004): 
    m, g, c = rnd(), stdn(), stdc()
    return c if m < T else g 

M = [Tukey_mixture() for _ in range(0x4444 << 0x4)]
show_hist(M, 0x44)
