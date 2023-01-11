## Fraction (positive) to continued fraction (in LaTeX) converter
#  https://en.wikipedia.org/wiki/Continued_fraction

from cmath import pi as π
from math import floor
from sys import float_info

def cfc(x):
    ltx = lambda str: print(str, end = '')
    def _cfc(p, q):
        an, n = floor(p/q), p%q

        ltx(r'\frac{1}{' + f'{an}')         # String interpolation...
        if (n > float_info.epsilon * 1000): # At hoc Deus ex machina!
            ltx('+')
            _cfc(q, n)
        ltx('}')

    ltx(f'{x} = ')
    n = floor(x)
    if(n != 0.0):
        ltx(f'{n}+')
    _cfc(1, x - n)

#Go4π!
cfc(floor(π * 1000)/1000)