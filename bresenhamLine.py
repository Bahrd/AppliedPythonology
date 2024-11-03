## Contiguos line plotting
#  https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
#  with our variations on an anti-aliasing theme...

from typing import Iterable
from numpy.random import randint
from numpy import clip, fliplr, flipud, zeros, maximum
from matplotlib.pyplot import imshow, show, subplot, tight_layout

## See this "esplanation": https://youtu.be/CceepU1vIKo?t=20 first!
def bresenham_line(x0: int, y0: int, x1: int, y1: int):   
    y = y0
    Δx, Δy = x1 - x0, y1 - y0   # d([xy]) → Δ$1
    D = (Δy << 1) - Δx
    
    Λ = zeros((Δx, Δy + 1))
    Δx <<= 1; Δy <<= 1
    for x in range(x0, x1):       
        Λ[x, y] = 1
        if D > 0:
            y += 1; D -= Δx
        D += Δy
    return Λ

## You should rather prefer a more mature approach to anti-aliasing...
#  https://www.youtube.com/watch?v=f3Rs20k-hcI
#  which is, however, not that downsampling-proof
def bresenhamAAline(x0: int, y0: int, x1: int, y1: int, AA:Iterable):
    def Γ(y: int):
        return clip(y, y0, y1)
    
    Δx, Δy = x1 - x0, y1 - y0
    D = (Δy << 1) - Δx
    
    Λ = zeros((Δx, Δy + 1))
    y, L = y0, len(AA)
    c, HL = 1 - (L % 0b10), L >> 1
    for x in range(x0, x1):       
        if D > 0:
            for n, w in zip(range(y - HL + c, y - HL + c + L), AA): 
                Λ[x, Γ(n)] = w        
            y += 1
            D -= Δx << 1
        else:
            for n, w in zip(range(y - HL, y - HL + L), AA[::-1]): 
                Λ[x, Γ(n)] = w
      
        D += Δy << 1
    return Λ

#                       (1/3, 2/3, 1/1, 2/3, 1/3)   # Symmetric AA filters when L is odd...
#                       (1/2, 1/1, 2/3, 1/3)        # 'Odd' AAA (asymmetric AA) when L is not...
X, Y, AA = 0x161, randint(0o161), (1/2, 1/1, 1/2)   # A minimal AA example...
noa, aa = bresenham_line(0, 0, X, Y), bresenhamAAline(0, 0, X, Y, AA)

# A helper...
def subshow (data:tuple):
    tight_layout()
    for n, d in enumerate(data):
        subplot(len(data), 1, n + 1)
        imshow(d, cmap = 'gray', interpolation = 'none')
    show()
    
bresenhams = maximum.reduce((flipud(aa), noa))
subshow((1 - bresenhams.T, fliplr(bresenhams.T)))          # ... must go on and gone!