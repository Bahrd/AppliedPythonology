## Continued fraction representation (in LaTeX)
#  x = a0 + ______1______
#           a1 + ___1____
#                a2 + ...
# Exemplum: -3.142 = -4+\frac{1}{1+\frac{1}{6+\frac{1}{23+\frac{1}{1+\frac{1}{1+\frac{1}{1}}}}}}
#  https://en.wikipedia.org/wiki/Continued_fraction

from cmath import pi as π
from math import floor
from sys import float_info

def cfc(x):
    ltx = lambda str: print(str, end = '')
    def _cfc_(p, q):
        an, n = floor(p/q), p%q

        ltx(r'\frac{1}{' + f'{an}')         # Either raw or interpolated...
        if (n > float_info.epsilon * 1000): # At hoc Deus ex machina!
            ltx('+')
            _cfc_(q, n)
        ltx('}')

    ltx(f'{x} = ')
    n = floor(x)
    if(n != 0.0):
        ltx(f'{n}+')
    _cfc_(1, x - n)

#Dare 4 more π!
cfc(floor(-π * 1000)/1000)