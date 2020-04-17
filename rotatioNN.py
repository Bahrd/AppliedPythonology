from interpolation import eddie
from auxiliary import displayImages as DI
from random import randrange as RR
from numpy import array, clip, empty
from math import sin, cos, pi
from sys import argv
## 2D rotation - a canonical version with an implicit NN interpolation
#  Be careful however, because ("Timeo Danaos et dona ferentes!"?) Python 
#  thinks that 'ϑ is θ == True' (and so are 'ϱ' and 'ρ', see ll. 39-40)!

## Setting... 
#  A rotation angle α...
ϱ = eval(argv[1]) if len(argv) > 1 else RR(-180, 180) #°
α, Cu = ϱ * pi/180.0, 'copper' # Main and auxiliary variables

#  ... and a source image...  (cf. './rotation2D.py')
img = eddie; M = len(img); N = int(argv[2]) if len(argv) > 2 else M << 0b1
out = empty((N, N)) 
# ... and rotation of ϑ = [x, y].T, w.r.t. OXY and through that angle
OXY, Rα = array([M/2, M/2]), array([[cos(α), -sin(α)], 
                                    [sin(α),  cos(α)]]) # '+' clockwise

for n in range(N):
    for m in range(N):
        ϑ = array([n/N, m/N]) * M - OXY
        ϑ = Rα @ ϑ + OXY
        x, y = clip(ϑ, 0, M - 1).astype(int) # where the NNs dwell
        out[n, m] = img[x, y]                # cf. rotation2D.py's '... = f(x, y, img, λ)'
                                                      #(ϱ)
DI((img, out), ('Original', 'NN-rotated by {0}°'.format(ρ)), cmp = Cu)
