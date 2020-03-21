from auxiliary import displayImages as DI
from random import randrange, random
from numpy import array, clip, empty
from math import sin, cos, pi
from sys import argv
## 2D rotation - a canonical version with an implicit NN interpolation

## Be careful ("Timeo Danaos et dona ferentes!")
#  Python thinks that 'ϑ == θ' and 'ϱ == ρ'!

# A shortcut... ;)
randbin = lambda: randrange(0b10)
# A source image... 
s = randbin(); g = s ^ 0b1; img = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                                         [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 
                                         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0], 
                                         [0, 0, 0, 1, 0, 0, 1, g, g, 1, 0, 0], 
                                         [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0], 
                                         [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0], 
                                         [0, 0, 0, 1, s, 1, 1, 1, s, 1, 0, 0], 
                                         [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
                                         [0, 0, 0, 0, 1, g, g, g, 1, 0, 0, 0], 
                                         [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],])
M = len(img); N = M << 0b11; out = empty((N, N)) 

α = float(argv[1]) if len(argv) == 2 else 360.0 * random() - 180.0 #°
ϱ = round(α, 1) # an auxiliary variable
α *= pi/180

# Rotation of the vector ϑ of coordinates through an angle α w.r.t. OXY
OXY, Rα = array([M/2, M/2]), array([[cos(α), -sin(α)], 
                                    [sin(α),  cos(α)]]) # clockwise
for n in range(N):
    for m in range(N):
        ϑ = array([n/N, m/N]) * M - OXY
        ϑ = Rα @ ϑ + OXY
        x, y = clip(ϑ, 0, M - 1).astype(int) # where the NNs dwell
        out[n, m] = img[x, y]
DI((img, out), ('Original', 'NN-rotated by {0}°'.format(ϱ)), cmp = 'copper')
