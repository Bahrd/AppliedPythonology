## A Bresenh`am (flooded) circle... a random edu version!
#  http://members.chello.at/~easyfilter/bresenham.html

from numpy import ones, fliplr, flipud, arange
from matplotlib.pyplot import imshow, show, pause, subplot, figure, grid
from numpy.random import choice, uniform, permutation as rpr

## A plain version
def bresenham_circle(_r: int):
    Φ = ones((2*_r + 1, 2*_r + 1))
    ζ, ξ, x, y, ε = _r, _r , -_r, 0, 2 - 2*_r
    
    while x <= 0:                                       
        for n, m, o in ((ζ - x, ξ + y, 0),   (ζ - y, ξ - x, .75),   # "One for the money, two for the show; 
                        (ζ + x, ξ - y, .25), (ζ + y, ξ + x, .5)):   #  Three to make ready, and four to go!"
            Φ[n, m] = o                                   # https://en.wikipedia.org/wiki/One_for_the_Money
        r = ε
        if r <= y:
            y += 1; ε += y*2 + 1
        if r > x or ε > y: 
            x += 1; ε += x*2 + 1
    return Φ

## A version obscured by debuggin' code (inactive if '-O' option is on)
def dbresenham_circle(_r: int):
    Φ = ones((2*_r + 1, 2*_r + 1))
    ζ, ξ, x, y, ε = _r, _r , -_r, 0, 2 - 2*_r
    
    c, _c = 0, False                        #  Bookkeeping Q1 [counting points of a circumference]
    while x <= 0:                                       
        for n, m, o in ((ζ - x, ξ + y, 0),   (ζ - y, ξ - x, .75),   # "One for the money, two for the show; 
                        (ζ + x, ξ - y, .25), (ζ + y, ξ + x, .5)):   #  Three to make ready, and four to go!"
            Φ[n, m] = o                                   # https://en.wikipedia.org/wiki/One_for_the_Money

        r = ε
        c += _c; _c = False                #  Bookkeeping Q2 
        if r <= y:
            y += 1; ε += y*2 + 1
        _c = True                       #  Bookkeeping Q3
        if r > x or ε > y: 
            x += 1; ε += x*2 + 1
        _c = True                       #  Bookkeeping Q4
            
    ## And the annual balance... [circumference/diameter = π, right?]
    # https://youtu.be/yAEveAH2KwI?t=96 - where π == 4...
    print(f'For r = {_r}, we have 2πr = {4*c} and π = {2*c/_r:.2f}...',
            f'(or d = {2*_r + 1}, πd = {4*c} and thus π = {4*c/(2*_r + 1):.2f} ;)')  
    return Φ

r = choice(range(0o1, 0o17))
bc = dbresenham_circle(r) if __debug__ else bresenham_circle(r)

fig = figure(figsize = (10, 3))
subplot(1, 3, 1); 

## Drawing on a grid...
#  https://www.tutorialspoint.com/remove-the-x-axis-ticks-while-keeping-the-grids-matplotlib    
ax = fig.gca()
ax.set_xticks(arange(.5, 2*r + 1, 1)), ax.set_yticks(arange(.5, 2*r + 1, 1))
ax.set_xticklabels([]), ax.set_yticklabels([])
ax.grid(True)

imshow(bc, cmap = 'gray', interpolation = 'none')

## A bit of low-level bit-blitting...
#  https://en.wikipedia.org/wiki/Blitter
v, w = 2*r + 4, 2*r + 1

canvas = ones((v, 2*v - 1))
canvas[:,  0] = canvas[:, -1] = 0   # "One for the money, two...
canvas[-1, :] = canvas[0,  :] = 0   # ... go!"

canvas[2:2 + w, 2:2 + w] = bc
canvas[1:1 + w, v:v + w] = flipud(fliplr(bc))

subplot(1, 3, (2, 3)); im = imshow(canvas, cmap = 'gray', interpolation = 'none')
u = 0, .33

## Fill the void(s)... (kinda exhaustive search?)
#  https://en.wikipedia.org/wiki/Flood_fill #Stack-based_recursive_implementation_(four-way)
#  A kindergarten random walk version: ♪♫Viva, Las Vegas!♫♪ https://youtu.be/uxmx9AV1GKU
#  https://www.pbr-book.org/4ed/Monte_Carlo_Integration
def flood_fill(x: int, y: int):
    global im, canvas, u
    
    canvas[x, y] = uniform(*u)  # Each pixel is "drowned" once    
    im.set_array(canvas), fig.canvas.draw_idle(), pause(0.001)
        
    # A fourfold (↑, ←, ↓, →) randomly ordered recurrence
    for (x, y) in rpr(((x - 1, y), (x, y - 1),   # ♪♫ [Never] the same, playin' your game.
                       (x + 1, y), (x, y + 1))): # Drive me insane, trouble is gonna come to you... ♫♪
        if canvas[x, y] == 1: flood_fill(x , y)            
    

## "Sī fuerīs Rōmae, Rōmānō vīvitō mōre; sī fuerīs alibī, vīvitō sīcut ibī..."
#  Or... just make sure the starting point (x, y) is inside the area
flood_fill(x = 0b10, y = 0o10) 

## ... and ♪♫ when the levee breaks...♫♪ 
#  https://youtu.be/JM3fodiK9rY
#flood_fill(25, 25), flood_fill(25, 50)
show()

''' #'Run with the hare and hunt with the hounds'
    # https://sl.bing.net/hmIR3ZJE4a
    
def flood_fill(x: int, y: int):
    global canvas, u
    Φ = lambda x, y: flood_fill(x, y) # just a shortcut
    
    if canvas[x, y] != 1: return
    canvas[x, y] = uniform(*u)
    
    # https://stackoverflow.com/questions/51520143/update-matplotlib-image-in-a-function 
    im.set_array(canvas), fig.canvas.draw_idle(), pause(0.01)
    Φ(x, y + 1) # →
    Φ(x, y - 1) # ←
    Φ(x + 1, y) # ↓
    Φ(x - 1, y) # ↑
 '''