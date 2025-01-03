﻿## A Bresenh`am (flooded) circle... a bunch of random edu versions!
from numpy import ones, fliplr, flipud, arange
from matplotlib.pyplot import imshow, show, pause, subplot, figure
from numpy.random import choice, permutation as rpr

# A shortcut for a square matrix of ones
_sqm = lambda _r: ones((_r + 1, _r + 1))
## Shades of gray... (or pale, if you like Procol Harum): https://www.youtube.com/watch?v=xM_N2O-gzP4
shades = (0/0x100, 0x69/0x100, 0x80/0x100, 0xd3/0x100,    # black, dimgray, gray, lightgray, etc: https://en.wikipedia.org/wiki/Grey#Optics
          0xc0/0x100, 0xdc/0x100, 0xa9/0x100, 0xbb/0x100) # silver, gainsboro, darkgray, and "pale"...

## A plain (but hardly pale!) quadrant version
#  ... Quartet, quadcopter, quaternion, quarter, quadruped, QB, quartz... 
#  http://members.chello.at/~easyfilter/bresenham.html
def bresenham_quadrant_circle(_r: int):
    Φ = _sqm(2*_r)
    ζ, ξ, x, y, ε = _r, _r , -_r, 0, 2 - 2*_r
    
    _rp = lambda Φ: rpr(Φ) if _r % 2 else Φ # A random order of quadrants (if the (randomy drawn) radius is odd!)
    while x <= 0:           
        for (n, m), o in zip(_rp(((ζ - x, ξ + y), (ζ - y, ξ - x),   
                                  (ζ + x, ξ - y), (ζ + y, ξ + x))), shades):   
            Φ[n, m] = o                           
        r = ε                               
        if r <= y:                          
            y += 1; ε += 2*y + 1            
        if r > x or ε > y:                  
            x += 1; ε += 2*x + 1            
    return Φ                                
## A version obscured by debuggin' code (inactive if '-O' option is on)
def dbresenham_quadrant_circle(_r: int):
    Φ = ones((2*_r + 1, 2*_r + 1))
    ζ, ξ, x, y, ε = _r, _r , -_r, 0, 2 - 2*_r
    
    c, _c = 0, False                #  Bookkeeping Q1 [counting points of a circumference]
    while x <= 0:                                       
        for (n, m), o in zip(((ζ - x, ξ + y), (ζ - y, ξ - x),           # ♪♫ One for the money, two for the show;  
                              (ζ + x, ξ - y), (ζ + y, ξ + x)), shades): #    Three to make ready, and four to go! ♫♪ https://genius.com/Carl-perkins-blue-suede-shoes-lyrics
            Φ[n, m] = o                                                 # https://en.wikipedia.org/wiki/One_for_the_Money
                                                                        # https://youtu.be/Bm5HKlQ6nGM?t=8 - by E. Presley '65
        r = ε                                                           # https://www.youtube.com/watch?v=O6BbL4DrrBo      '68
        c += _c; _c = False         #  Bookkeeping Q2                     https://www.youtube.com/watch?v=RX7hBaoMuT0      '70
        if r <= y:                                                      # https://www.youtube.com/watch?v=VJFz8zZCJZg      '77
            y += 1; ε += y*2 + 1                                        # https://www.youtube.com/watch?v=oKQj-RXg3Dk - Carl Perkins 
        _c = True                   #  Bookkeeping Q3                     https://www.youtube.com/watch?v=aSCP_UnzKDk - ... with Johnny Cash
        if r > x or ε > y: 
            x += 1; ε += x*2 + 1
        _c = True                   #  Bookkeeping Q4
            
    ## And the annual (periodic anyway!) balance... [circumference/diameter = π, right?]
    # https://youtu.be/yAEveAH2KwI?t=96 - where π == 4...
    print(f'For r = {_r}, we have 2πr = {4*c} and π = {2*c/_r:.2f}...',
            f'(or d = {2*_r + 1}, πd = {4*c} and thus π = {4*c/(2*_r + 1):.2f} ;)')  
    return Φ
# And an even smarter (octant) one (written in a "binary" style! ;): 
# ... Octavian, octant, octopus, octet (a.k.a. byte), October(!) for octo(genarians?!)... 
# https://www.youtube.com/watch?v=hpiILbMkF9w
def bresenham_octant_circle(_r: int):
    # A canvas 0b100 the circle centered at Ø = (_r, _r)
    Φ, Ø = _sqm(_r << 1), _r 
    
    #... and the actual algorithm
    x, y, ε = 0, _r, _r
    while x < y:
        if ε < 0:
            y -= 1
            ε -= x - y << 1
        else:
            ε -= x << 1
        for (n, m), ø in zip(((Ø + x, Ø + y), (Ø - x, Ø - y), (Ø + x, Ø - y), (Ø - x, Ø + y), 
                              (Ø + y, Ø + x), (Ø - y, Ø - x), (Ø + y, Ø - x), (Ø - y, Ø + x)), shades):
            Φ[n, m] = ø 
        x += 1; ε -= 1
    return Φ
    
## ♪♫ Che sarà sarà... ♫♪ https://youtu.be/i9nWB5XifBI (a terrific induction/recursion...)
# Primus aleus..
r = choice(range(0o1, 0o17)) 
# ... et aleus secundus!
bresenham_circle = dbresenham_quadrant_circle if __debug__ else choice((bresenham_quadrant_circle, 
                                                                        bresenham_octant_circle))
# Alea iacta est! 
bc = bresenham_circle(r)

## Drawing on a grid...
fig = figure(figsize = (10, 3));subplot(1, 3, 1); 
#  https://www.tutorialspoint.com/remove-the-x-axis-ticks-while-keeping-the-grids-matplotlib    
ax = fig.gca()
ax.set_xticks(arange(.5, 2*r + 1, 1)), ax.set_yticks(arange(.5, 2*r + 1, 1))
ax.set_xticklabels([]), ax.set_yticklabels([])
ax.grid(True)

imshow(bc, cmap = 'gray', interpolation = 'none')

## A bit of 3L2B (low-level-like bit-blitting)...
#  https://en.wikipedia.org/wiki/Blitter
v, w = 2*r + 4, 2*r + 1

# A canvas, and its borders...
canvas = ones((v, 2*v - 1))         
canvas[ :, 0] = canvas[:, -1] = canvas[-1, :] = canvas[0,  :] = 0 
# ... and the actual blitting
canvas[2:2 + w, 2:2 + w], canvas[1:1 + w, v:v + w] = bc, flipud(fliplr(bc))

subplot(1, 3, (2, 3)); im = imshow(canvas, cmap = 'gray', interpolation = 'none')
u = 0, .33

r''' Fill the void(s)... (kinda exhaustive search?)
  https://en.wikipedia.org/wiki/Flood_fill #Stack-based_recursive_implementation_(four-way)
  Had I been you, I would've used a quad-tree... https://en.wikipedia.org/wiki/Quadtree
  A kindergarten random walk version: ♪♫Viva, Las Vegas!♫♪ https://youtu.be/uxmx9AV1GKU
  https://www.pbr-book.org/4ed/Monte_Carlo_Integration '''
def flood_fill(x: int, y: int):
    global im, canvas, u
    
    canvas[x, y] = choice(shades)   # For each pixel is "drowned" once    
    im.set_array(canvas), fig.canvas.draw_idle(), pause(0.001)
        
    # A fourfold (↑, ←, ↓, →) randomly ordered recurrence
    for (x, y) in rpr(((x - 1, y), (x, y - 1),   # ♪♫ [Never] the same, playin' your game.
                       (x + 1, y), (x, y + 1))): #    Drive me insane, trouble is gonna come to you... ♫♪
        if canvas[x, y] == 1: flood_fill(x , y)  # https://youtu.be/PNk8NBqCEN8          
    
## "Sī fuerīs Rōmae, Rōmānō vīvitō mōre; sī fuerīs alibī, vīvitō sīcut ibī..."
#  Or... just make sure the starting point (x, y) is inside the area
flood_fill(x = 0b10, y = 0o10) 

## ... and ♪♫ when the levee breaks...♫♪ 
# https://youtu.be/JM3fodiK9rY
#flood_fill(25, 25), flood_fill(25, 50)
show()

r''' #'Run with the hare and hunt with the hounds'
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