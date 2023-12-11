## Contiguos line plotting
#  https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
#  with our variations on an anti-aliasing theme...

from numpy import clip, zeros, maximum, flipud
from matplotlib.pyplot import imshow, show

def bresenham_line(x0: int, y0: int, x1: int, y1: int, antialiasing = True):
    def clp(y: int):
        return clip(y, y0, y1)

    dx, dy = x1 - x0, y1 - y0
    D = 2*dy - dx
    
    line = zeros((dx, dy + 1))
    y = y0
    for x in range(x0, x1):       
        if D > 0:
            if(antialiasing):
                for n, w in zip(range(y - 1, y + 3), (1/4, 1, 2/4, 1/4)):
                    line[x, clp(n)] = w
            else:
                line[x, y] = 1
            y = y + 1
            D = D - 2*dx
        else:
            if(antialiasing):
                for n, w in zip(range(y - 2, y + 2), (1/4, 2/4, 1, 1/4)):
                    line[x, clp(n)] = w
            else:
                line[x, y] = 1
        D = D + 2*dy
    return line

X, Y = 0x369, 0o137
noa, aa = bresenham_line(0, 0, X, Y, False), bresenham_line(0, 0, X, Y)
lines = maximum.reduce((flipud(noa), aa))

_ = imshow(1 - lines.T, cmap='gray', interpolation = 'none'), show() # ... must gone!