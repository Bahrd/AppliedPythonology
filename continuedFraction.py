'''Continued fraction [represent|approxim]ation of x (the simple one)
   See also: https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html#example-continued-fractions
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
import re
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

# A scalar quantizer (n: number of digits of the fractional part in b-nary system)
qnz = lambda x, n, b = 10, ε = 1/2: floor(x * b**n + ε)/b**n

##  Pipeline/command line mode:   
#   echo '(1 + sqrt(5))/2, 2**2' | <path-to-python-env\>python.exe .\continuedFraction.py
if(len(argv) == 1): 
    for line in fileinput.input():
        n, x = re.sub(',[ 0-9*+-]*$', '', line.rstrip()), (eval(s) for s in line.rstrip().split(', '))
        print(f'{n} = {scf(qnz(*x))}')
## 'Demo'mode ♪♫ If you dare... ♫♪ https://youtu.be/5dvMRYuPnEI 4 more [than φ or π...?]
#  <path-to-python-env\>python.exe .\continuedFraction.py --demo
else:         
    for n, x in ('φ', ((1 + sqrt(5))/2, 3)), ('π', (pi, 4)), ('-1/4', (-1/4, 2)): 
        print(f'{n} = {scf(qnz(*x))}')
    