## Julia fractal (parametrized by the initial value c)
from matplotlib.widgets import Slider
from matplotlib.pyplot import subplots, subplots_adjust, axes, show, imshow
from numpy import linspace as lsp, power as pwr, mat as mt, isnan, any

## Presentation
N, M = 0x300, 0x150  # resolution
_Ω = mt([[complex(n, m) for n in lsp(-2, 2, N)] for m in lsp(-1, 1, M)])

## All Julias are essentially the same (mod c ;)...
def julia(_):
    global im, realEV, imagEV, _Ω
    # Unsettling settings
    Ω, c = _Ω, complex(realEV.val, imagEV.val)
    
    # The main loop
    for _ in range(0x40):
        Ω = pwr(Ω, 2) + c
        Ω[any([isnan(Ω), abs(Ω) > 0xff], axis = 0)] = 0xff # Julia's face-lifting...
        
    im.set_array(abs(Ω))

##  GUI elements
fig, _ = subplots(num = '♪♫ https://youtu.be/cIZ_tHZJjEs ♫♪'); subplots_adjust(left = .1, bottom = .25)
im = imshow(abs(_Ω), interpolation = 'none', cmap = 'Blues')
## A popular choice is c = -.8 + .156j, nevertheless, 
#  even with c = .15 + .6j Julia still looks nice (not to mention c = 0 + 0j... ;)
kwargs = ({'ax': axes(( .1,  .1,  .8, .03)), 'label': 'Re(c)', 'valmin': -1, 'valmax': .3, 'valstep': .02,
           'valinit':  -.8}, 
          {'ax': axes((.92, .25, .03, .65)), 'label': 'Im(c)', 'valmin':  0, 'valmax': .6, 'valstep': .02, 
           'orientation': 'vertical',
           'valinit': .156})
realEV, imagEV = (Slider(**kwarg) for kwarg in kwargs)
realEV.on_changed(julia), imagEV.on_changed(julia)

julia(_), show()
''' A plain old Julia...
from numpy import linspace as lsp, power as pwr, mat as mt, isnan, any, log, e
from auxiliary import displayImages as DI; 

## An approximate Julia set function (resolution grows with ν)
#       J = {ω ∈ Ω: julia(ω, ∞) < 2}
# see e.g. https://en.wikipedia.org/wiki/Julia_set for some nicer c's
def julia(ω, ν = 0x40, c = -.8 + .156j, p = 2):
    for _ in range(ν):
        ω = pwr(ω, p) + c
        # Julia's face-lifting...
        ω[any([isnan(ω), abs(ω) > 0xff], axis = 0)] = 0xf
    return log(e + abs(ω))  # Not exactly a set function (like it would've been with 'return abs(ω) > 2')
                            # but looks somehow fancier...

## Presentation
# Unsettling settings
N, M = 0x800, 0x400  # resolution
Ω = mt([[complex(n, m) for n in lsp(-2, 2, N)] 
                       for m in lsp(-1, 1, M)])
# ... and a show off!
c = -.8 + .156j; J = julia(Ω, c = c)

DI(J, 'Julia set for c = {}'.format(c), cmp = 'Blues')
'''