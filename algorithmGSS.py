## The GSS (golden section search algorithm) implementations

# See: https://en.wikipedia.org/wiki/Golden-section_search#Algorithm 
# Given an interval [l, r] and a maximum of unimodal function f at x, 
# find an interval [x - ε, x + ε] in the smallest number of steps.

import math
φ  = (math.sqrt(5) - 1) / 2     # Since 1/φ == φ - 1 
## Wikipedia's implementation
def gss(f, a, b, ε = 1e-5, h = None,  c = None, d = None,
                             fc = None, fd = None):
    (a, b) = (min(a, b), max(a, b))
    
    # Log: print('[{:.4f}, {:.4f}]'.format(a, b))
    # Interval width
    if h == None: h = b - a
    if h <= ε: return (a, b)

    # Interval bounds
    if c == None: c = a + φ * φ * h
    if d == None: d = a +  φ * h
    if fc == None: fc = f(c)
    if fd == None: fd = f(d)
    
    if fc > fd:
        return gss(f, a, d, ε, h * φ, 
                      c = None, fc = None, d = c, fd = fc)
    else:
        return gss(f, c, b, ε, h * φ, 
                      c = d, fc = fd, d = None, fd = None)

## Our take:
# A recursive implementation... 
def gssl(f, ε, l, r):
    φ  = (math.sqrt(5) - 1)/2   # Note: φ - 1 == 1/φ
    n, m = l + (r - l) * φ, r - (r - l) * φ
    def gsslk(f, ε, l, r, n , m):
        if r - l <= ε: return (l, r)
        if f(m) > f(n):
            r, n = n, m
            m = r - (r - l) * φ
            return gsslk(f, ε, l, r, n, m)
        else:
            l, m = m, n  
            n = l + (r - l) * φ
            return gsslk(f, ε, l, r, n, m)
    
    return gsslk(f, ε, l, r, n , m)

# ... disguised in an OO interface
class GSS:
    def __init__(s, f, ε, l, r):
        s.f, s.ε = f, ε 
        s.l, s.r = l, r
        s.φ = (math.sqrt(5) - 1)/2 # Note: φ - 1 == 1/φ
    # The recursive search
    def search(s, l, r, n, m):
        if r - l <= s.ε: return (l, r)

        if s.f(m) > s.f(n):
            r, n = n, m
            m = r - (r - l) * φ
            return s.search(l, r, n, m)
        else:
            l, m = m, n  
            n = l + (r - l) * φ
            return s.search(l, r, n, m)
    # The interface...
    def find(s):
        l, r, φ = s.l, s.r, s.φ
        n, m = l + (r - l) * φ, r - (r - l) * φ

        return s.search(l, r, n, m)

## Tests...
f = lambda x: -abs(x - 1/φ)

# Wiki's...
l, r, ε = 0, 2/φ, 1e-3
(c,d) = gss(f, l, r, ε)
print('\n[{:.6f}, {:.6f}]'.format(c, d))

# ... and ours
(c,d) = gssl(f, ε, l, r)
print('\n[{:.6f}, {:.6f}]'.format(c, d))

gs = GSS(f, ε, l, r)
(c,d) = gs.find()
print('\n[{:.6f}, {:.6f}]'.format(c, d))