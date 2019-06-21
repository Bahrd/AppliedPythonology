## The GSS (golden section search algorithm) implementations

# See: https://en.wikipedia.org/wiki/Golden-section_search#Algorithm 
# Given an interval [l, r] and a maximum of unimodal function f at x, 
# find an interval [x - ε, x + ε] in the smallest number of steps.

import math
## Wikipedia's implementation
def gss(f, a, b, ε = 1e-5, h = None,  c = None, d = None,
                          fc = None, fd = None):
    (a, b) = (min(a, b), max(a, b))
    ιφ  = (math.sqrt(5) - 1) / 2     # Since 1/φ == φ - 1 

    # Log: print('[{:.4f}, {:.4f}]'.format(a, b))
    # Interval width
    if h == None: h = b - a
    if h <= ε: return (a, b)

    # Interval bounds
    if c == None: c = a + ιφ * ιφ * h
    if d == None: d = a +  ιφ * h
    if fc == None: fc = f(c)
    if fd == None: fd = f(d)
    
    if fc > fd:
        return gss(f, a, d, ε, h * ιφ, 
                      c = None, fc = None, d = c, fd = fc)
    else:
        return gss(f, c, b, ε, h * ιφ, 
                      c = d, fc = fd, d = None, fd = None)

## Our take:
# A recursive implementation... 
def gssl(f, ε, l, r):
    ιφ  = (math.sqrt(5) - 1)/2   # Note: φ - 1 == 1/φ
    n, m = l + (r - l) * ιφ, r - (r - l) * ιφ
    def gsslk(f, ε, l, r, n , m):
        if r - l <= ε: return (l, r)
        if f(m) > f(n):
            r, n = n, m
            m = r - (r - l) * ιφ
            return gsslk(f, ε, l, r, n, m)
        else:
            l, m = m, n  
            n = l + (r - l) * ιφ
            return gsslk(f, ε, l, r, n, m)
    
    return gsslk(f, ε, l, r, n , m)

# ... disguised in an OO interface
class GSS:
    def __init__(λ, f, ε, l, r): # 'λ' stands for 'λογιστικόν' (a part of soul
        λ.f, λ.ε = f, ε          # associated with logic - according to Plato)
        λ.l, λ.r = l, r          # or a usual 'self' in a Python OO approach
        λ.ιφ = (math.sqrt(5) - 1)/2 # Note again: φ - 1 == 1/φ
    # The recursive search
    def search(λ, l, r, n, m):
        if r - l <= λ.ε: return (l, r)
        ιφ = λ.ιφ
        if λ.f(m) > λ.f(n):
            r, n = n, m
            m = r - (r - l) * ιφ
            return λ.search(l, r, n, m)
        else:
            l, m = m, n  
            n = l + (r - l) * ιφ
            return λ.search(l, r, n, m)
    # The interface...
    def find(λ):
        l, r, ιφ = λ.l, λ.r, λ.ιφ
        n, m = l + (r - l) * ιφ, r - (r - l) * ιφ

        return λ.search(l, r, n, m)

## Tests...
φ  = (math.sqrt(5) + 1)/2
f = lambda x: -abs(x - φ)
l, r, ε = 0, 2*φ, 1e-3

# Wiki's...
(c,d) = gss(f, l, r, ε)
print('\n[{:.6f}, {:.6f}]'.format(c, d))

# ... and ours
(c,d) = gssl(f, ε, l, r)
print('\n[{:.6f}, {:.6f}]'.format(c, d))

gs = GSS(f, ε, l, r)
(c,d) = gs.find()
print('\n[{:.6f}, {:.6f}]'.format(c, d))