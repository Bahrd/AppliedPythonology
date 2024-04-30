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
    
        def _scf_(p, q):
            an, n = flr(p/q), p%q

            ltx(r'\frac{1}{' + f'{an}')
            if (n >= ε):    
                ltx('+')
                _scf_(q, n)
            ltx('}')

        n = flr(x)
        if(n): ltx(f'{n}+')
        _scf_(1, x - n)
'''

from sys import float_info as fi
from math import floor, sqrt, pi
from sys import argv
import fileinput, string

def scf(x: float) -> string: 
    ε, ltx = 1e3 * fi.epsilon, ''       # At hoc Deus ex machina!
    
    def _scf_(p: int, q: int):
        nonlocal ltx, ε;
        an, n = floor(p/q), p%q
        
        ltx += r'\frac{1}{' + f'{an}'   # Either raw or interpolated...
        if (n >= ε):    
            ltx += '+'
            _scf_(q, n)
        ltx += '}'

    n = floor(x)
    if(n): 
        ltx += f'{n}+'
    _scf_(1, x - n)   
    return ltx

# Decimal quantizer (n: number of digits after a decimal point)
qnz = lambda x, n: floor(x * 10**n)/10**n

##  Pipeline/command line mode:   
#   echo '(1 + sqrt(5))/2, 2**2' | <path-to-python-env\>python.exe .\continuedFraction.py
if(len(argv) == 1): 
    for line in fileinput.input():
        x = (eval(s) for s in line.split(', '))
        print(scf(qnz(*x)))
## "Demo" mode 
#  <path-to-python-env\>python.exe .\continuedFraction.py --demo
else:              
    φ, π, q = .5*(1 + sqrt(5)), pi, -1/4    # Dare 4 more than π & φ?
    cfs = (('π ~', qnz(π, 4)), ('φ ~', qnz(φ, 3)), ('-1/4 =', qnz(q, 4)))
    for n, x in cfs: 
        print(f'{n} {scf(x)} = {x}')
    