## A Bresenham (flooded) circle... edu version!
#  http://members.chello.at/~easyfilter/bresenham.html

from numpy import ones, fliplr, flipud
from matplotlib.pyplot import imshow, show, figure, pause 
from random import uniform

def bresenham_circle(r: int):
    circle = ones((2*r + 1, 2*r + 1))
    xm, ym, x, y, err = r, r , -r, 0, 2 - 2*r

    while x <= 0:
        circle[xm-x, ym+y] = .0
        circle[xm-y, ym-x] = .2
        circle[xm+x, ym-y] = .4
        circle[xm+y, ym+x] = .6

        r = err;
        if r <= y:
            y += 1
            err += y*2 + 1
        if r > x or err > y: 
            x += 1
            err += x*2 + 1
    return circle

r = 0o10; bc = bresenham_circle(r)
fig = figure()
imshow(bc, cmap = 'gray', interpolation = 'none'), show()

# A bit of low-level bit-blitting...
# https://en.wikipedia.org/wiki/Blitter
v, w = 2*r + 4, 2*r + 1

canvas = ones((v, 2*v - 1))
canvas[:,  0] = canvas[:, -1] = 0
canvas[-1, :] = canvas[0,  :] = 0

canvas[2:2 + w, 2:2 + w] = bc
canvas[1:1 + w, v:v + w] = flipud(fliplr(bc))

im = imshow(canvas, cmap = 'gray', interpolation = 'none')
# Fill the void(s)...
# https://en.wikipedia.org/wiki/Flood_fill #Stack-based_recursive_implementation_(four-way)
def flood_fill(x:int, y:int, u = (0, 1)):
    if canvas[x, y] != 1: return
    canvas[x, y] = uniform(*u)  
    
    # https://stackoverflow.com/questions/51520143/update-matplotlib-image-in-a-function 
    im.set_array(canvas), fig.canvas.draw_idle(), pause(0.001)
    
    flood_fill(x - 1, y, u), flood_fill(x + 1, y, u)
    flood_fill(x, y - 1, u), flood_fill(x, y + 1, u)
    return

flood_fill(2, 2, u = (0, .33))
## ♪♫ When the levee breaks...♫♪ 
#  https://www.youtube.com/watch?v=JM3fodiK9rY
#flood_fill(25, 25, u = (.33, .66)), flood_fill(25, 50, u = (.66, 1))
show()