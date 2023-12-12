## Contiguos line plotting
#  https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
#  with our variations on an anti-aliasing theme...

from numpy import clip, concatenate, zeros, maximum, flipud
from matplotlib.pyplot import imshow, show

def bresenham_line(x0: int, y0: int, x1: int, y1: int, AA:tuple or list = None):
    def clp(y: int):
        return clip(y, y0, y1)

    dx, dy = x1 - x0, y1 - y0
    D = 2*dy - dx
    
    line = zeros((dx, dy + 1))
    y, L = y0, len(AA) if AA != None else 0
    c, HL = 1 - (L - 2*int(L/2)), int(L/2)
    for x in range(x0, x1):       
        if D > 0:
            if(AA != None):
                for n, w in zip(range(y - HL + c, y - HL + c + L), AA):
                    line[x, clp(n)] = w
            else:   line[x, y] = 1
        
            y = y + 1
            D = D - 2*dx
        else:
            if(AA != None):
                for n, w in zip(range(y - HL, y - HL + L), AA[::-1]):
                    line[x, clp(n)] = w
            else:   line[x, y] = 1
        
        D = D + 2*dy
    return line

#                       (1/3, 2/3, 1/1, 2/3, 1/3)   # Symmetric AA filters when L is odd...
X, Y, AA = 0x163, 0o61, (1/2, 1/1, 2/3, 1/3)        # 'Odd' AAA (asymmetric AA) when L is not...
noa, aa = bresenham_line(0, 0, X, Y, AA = AA), bresenham_line(0, 0, X, Y)

# A helper...
duo_show = lambda data:tuple ((imshow(d, cmap = 'gray', interpolation = 'none'), 
                               show()) for d in data)
bresenhams = maximum.reduce((flipud(noa), aa))
duo_show((1 - bresenhams.T, bresenhams.T))          # ... must go on and gone!