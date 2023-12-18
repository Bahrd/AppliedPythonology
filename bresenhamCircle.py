## A Bresenham (flooded) circle... a random edu version!
#  http://members.chello.at/~easyfilter/bresenham.html

from numpy import ones, fliplr, flipud
from matplotlib.pyplot import imshow, show, pause, subplot, figure
from numpy.random import choice, uniform, permutation as rpr

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

r = choice(range(0o3, 0o17)); bc = bresenham_circle(r)
fig = figure(figsize = (10, 3))
subplot(1, 3, 1); imshow(bc, cmap = 'gray', interpolation = 'none')

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

## Fill the void(s)... - a kindergarten random walk version
#  https://en.wikipedia.org/wiki/Flood_fill #Stack-based_recursive_implementation_(four-way)
def flood_fill(x:int, y:int):
    global im, canvas, u
    
    canvas[x, y] = uniform(*u)  # Each pixel is changed once    
    im.set_array(canvas), fig.canvas.draw_idle(), pause(0.001)
        
    # A fourfold (↑, ←, ↓, →) randomly ordered recurrence
    for (x, y) in rpr(((x - 1, y), (x, y - 1),   # ♪♫ [Never] the same, playin' your game.
                       (x + 1, y), (x, y + 1))): # Drive me insane, trouble is gonna come to you... ♫♪
        if canvas[x, y] == 1: flood_fill(x , y)            
    

## "Sī fuerīs Rōmae, Rōmānō vīvitō mōre; sī fuerīs alibī, vīvitō sīcut ibī..."
#  Or... just make sure the starting point (x, y) is inside the area
flood_fill(x = 2, y = 2) 
## ... and ♪♫ when the levee breaks...♫♪ 
#  https://www.youtube.com/watch?v=JM3fodiK9rY
#flood_fill(25, 25), flood_fill(25, 50)
show()

''' #'Run with the hare and hunt with the hounds'
    # https://sl.bing.net/hmIR3ZJE4a
    
def flood_fill(x:int, y:int):
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