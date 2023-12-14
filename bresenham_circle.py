## A Bresenham (flooded) circle... edu version!
#  http://members.chello.at/~easyfilter/bresenham.html

from numpy import ones, fliplr, flipud
from matplotlib.pyplot import imshow, show, figure, pause, subplot
from random import uniform

def bresenham_circle(r: int):
    Φ = ones((2*r + 1, 2*r + 1))
    ζ, ξ, x, y, ε = r, r , -r, 0, 2 - 2*r
    
    while x < 0:                           ## https://en.wikipedia.org/wiki/One_for_the_Money
        Φ[ζ-x, ξ+y], Φ[ζ-y, ξ-x] = .0, .25 # "One for the money, two for the show; 
        Φ[ζ+x, ξ-y], Φ[ζ+y, ξ+x] = .5, .75 #  Three to make ready, and four to go!"
        
        r = ε;
        if r <= y:
            y += 1
            ε += y*2 + 1
        if r > x or ε > y: 
            x += 1
            ε += x*2 + 1
    return Φ

r = 0o13; bc = bresenham_circle(r)

fig = figure()
subplot(211); imshow(bc, cmap = 'gray', interpolation = 'none')

## A bit of low-level bit-blitting...
# https://en.wikipedia.org/wiki/Blitter
v, w = 2*r + 4, 2*r + 1

canvas = ones((v, 2*v - 1))
canvas[:,  0] = canvas[:, -1] = 0   # "One for the money, two...
canvas[-1, :] = canvas[0,  :] = 0   # ... go!"

canvas[2:2 + w, 2:2 + w] = bc
canvas[1:1 + w, v:v + w] = flipud(fliplr(bc))
subplot(212); im = imshow(canvas, cmap = 'gray', interpolation = 'none')
# Fill the void(s)... A kindergarten version
# https://en.wikipedia.org/wiki/Flood_fill #Stack-based_recursive_implementation_(four-way)

def flood_fill(x:int, y:int, u = (0, 1)):
    global canvas 
    Φ = lambda x, y, u: flood_fill(x, y, u) # just a shortcut
    
    if canvas[x, y] != 1: return
    else: canvas[x, y] = uniform(*u)  
    
    # https://stackoverflow.com/questions/51520143/update-matplotlib-image-in-a-function 
    im.set_array(canvas), fig.canvas.draw_idle(), pause(0.001)
    
    Φ(x, y + 1, u), Φ(x + 1, y, u) # "One...
    Φ(x, y - 1, u), Φ(x - 1, y, u) # o°.°.o
    return

flood_fill(2, 2, u = (0, .33))
## ♪♫ When the levee breaks...♫♪ 
#  https://www.youtube.com/watch?v=JM3fodiK9rY
#flood_fill(25, 25, u = (.33, .66)), flood_fill(25, 50, u = (.66, 1))
show()