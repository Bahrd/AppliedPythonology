from auxiliary import displayImages as DI
from random import randrange
from numpy import array, clip, empty
from math import sin, cos, pi
from sys import argv
## 2D rotation - a canonical version with an implicit NN interpolation

## Be careful ("Timeo Danaos et dona ferentes!")
#  Python thinks that 'ϑ is θ == True' (so are 'ϱ' and 'ρ')!

# A source image... 
s = randrange(0b10); g = s ^ 0b1; img = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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

# Setting a rotation angle α
α = int(argv[1]) if len(argv) == 2 else randrange(-180, 180) #°
ϱ = α # an auxiliary variable
α *= pi/180.0

# Rotation of the vector ϑ of the pixel coordinates through an angle α w.r.t. OXY
OXY, Rα = array([M/2, M/2]), array([[cos(α), -sin(α)], 
                                    [sin(α),  cos(α)]]) # '+' clockwise
for n in range(N):
    for m in range(N):
        ϑ = array([n/N, m/N]) * M - OXY
        ϑ = Rα @ ϑ + OXY
        x, y = clip(ϑ, 0, M - 1).astype(int) # where the NNs dwell
        out[n, m] = img[x, y]
DI((img, out), ('Original', 'NN-rotated by {0}°'.format(ϱ)), cmp = 'copper')
