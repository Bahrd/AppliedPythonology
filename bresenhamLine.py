## Contiguos line plotting
#  https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
#  with our variations on an anti-aliasing theme...

from typing import Iterable
from numpy.random import randint
from numpy import clip, fliplr, flipud, zeros, maximum
from matplotlib.pyplot import imshow, show, subplot, tight_layout

## See this "esplanation": https://youtu.be/CceepU1vIKo?t=20 first!
def bresenham_line(x0: int, y0: int, x1: int, y1: int):   
    dx, dy = x1 - x0, y1 - y0
    D = (dy << 1) - dx
    
    Λ = zeros((dx, dy + 1))
    y = y0
    dx <<= 1; dy <<= 1
    for x in range(x0, x1):       
        Λ[x, y] = 1
        if D > 0:
            y += 1
            D -= dx
        D += dy
    return Λ

def bresenhamAAline(x0: int, y0: int, x1: int, y1: int, AA:Iterable):
    def Γ(y: int):
        return clip(y, y0, y1)
    
    dx, dy = x1 - x0, y1 - y0
    D = 2*dy - dx
    
    Λ = zeros((dx, dy + 1))
    y, L = y0, len(AA)
    c, HL = 1 - (L - 2*(L//2)), (L//2)
    for x in range(x0, x1):       
        if D > 0:
            for n, w in zip(range(y - HL + c, y - HL + c + L), AA): Λ[x, Γ(n)] = w        
            y = y + 1
            D = D - (dx << 1)
        else:
            for n, w in zip(range(y - HL, y - HL + L), AA[::-1]): Λ[x, Γ(n)] = w
      
        D = D + (dy << 1)
    return Λ

#                       (1/3, 2/3, 1/1, 2/3, 1/3)   # Symmetric AA filters when L is odd...
#                       (1/2, 1/1, 2/3, 1/3)        # 'Odd' AAA (asymmetric AA) when L is not...
X, Y, AA = 0x161, randint(0o161), (1/2, 1/1, 1/2)   # A minimal AA example...
noa, aa = bresenhamAAline(0, 0, X, Y, AA = AA), bresenham_line(0, 0, X, Y)

# A helper...
def subshow (data:tuple):
    tight_layout()
    for n, d in enumerate(data):
        subplot(len(data), 1, n + 1)
        imshow(d, cmap = 'gray', interpolation = 'none')
    show()
    
bresenhams = maximum.reduce((flipud(noa), aa))
subshow((1 - bresenhams.T, fliplr(bresenhams.T)))          # ... must go on and gone!