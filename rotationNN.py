﻿from interpolation import Π, ψ, ϕ, interpolate
from auxiliary import displayImages
import numpy as np; import matplotlib.pyplot as plt
from random import randrange
from math import sin, cos, pi

# Same shortcuts... ;)
randbin = lambda: randrange(0b10)
# A source image... 
s = randbin(); g = s ^ 0b1; img = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
M = len(img); N = M << 0b10 #13 #
out = np.empty((N, N)) 

# 2D rotation - a canonical version with an implicit NN interpolation
α = pi/180 * 150 #°
Rα = np.array([[cos(α), -sin(α)], [sin(α), cos(α)]])

# Rotation of the vector ϑ of coordinates through an angle α 
# w.r.t. the center of an image
for n in range(N):
    for m in range(N):
        ϑ = np.array([n/N, m/N]) * M - M/2
        ϑ = Rα @ ϑ + M/2
        x, y = np.clip(ϑ, 0, M - 1).astype(int) # where the NNs dwell
        out[n, m] = img[x, y]
displayImages((img, out), ('Original', 'Rotated by {0}°'.format(round(α*180/pi, 1))), cmp = 'copper')
