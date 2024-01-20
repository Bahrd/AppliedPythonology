'''Continued fraction [represent|approxim]ation of x (the simple one)
   x = a0 + ______1______
            a1 + ___1____
                 a2 + ...
   See: https://en.wikipedia.org/wiki/Continued_fraction
   Exemplum (in LaTeX): -3.142 = -4+\frac{1}{1+\frac{1}{6+\frac{1}{23
                                   +\frac{1}{1+\frac{1}{1+\frac{1}{1}}}}}}

    def cfc(x):
        ltx = lambda str: print(str, end = '')
        ε = float_info.epsilon * 1000 
    
        def _cfc_(p, q):
            an, n = flr(p/q), p%q

            ltx(r'\frac{1}{' + f'{an}')
            if (n >= ε):    
                ltx('+')
                _cfc_(q, n)
            ltx('}')

        n = flr(x)
        if(n): ltx(f'{n}+')
        _cfc_(1, x - n)
'''

from math import pi as π
from math import floor as flr, sqrt
from sys import float_info as fi

def cfc2ltx(x): 
    ε, ltx = 1e3 * fi.epsilon, ''       # At hoc Deus ex machina!
    
    def _cfc_(p, q):
        nonlocal ltx, ε;
        an, n = flr(p/q), p%q
        
        ltx += r'\frac{1}{' + f'{an}'   # Either raw or interpolated...
        if (n >= ε):    
            ltx += '+'
            _cfc_(q, n)
        ltx += '}'

    n = flr(x)
    if(n): 
        ltx += f'{n}+'
    _cfc_(1, x - n)   
    return ltx

#Dare 4 more: π or φ!
scf = ((flr(π * 1e4)/10000,              'π'), 
       (-3/4,                            '-3/4'), 
       (flr((1 + sqrt(5))/2 * 1e3)/1000, 'φ'))

for x, n in scf: print(f'{n}: {x} = {cfc2ltx(x)}')