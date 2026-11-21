'''
https://en.wikipedia.org/wiki/3D_rotation_group - SO(3) (a non-abelian [non-commutative] group)
A.k.a. "The special orthogonal group in 3 dimensions"
SO(2) is a commutative (abelian) group though...

An eagle eye will surely notice that this script is a 2D version of the 3D virtual window... ;)
Let's call it a "virtual glimmer-gap" (ThnX Copilot for that term... ;)
'''
from numpy import array as A, identity as I
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import pi as π, cos, sin

from sys import argv as eye

# Transform a polygon, that is, apply a transformation matrix to all its vertices
文 = lambda P, vertices: A([P@V for V in vertices])
# Homogeneous to Euclidean coordinates conversion (a.k.a. "casting a shadow" or "projecting a 2D object onto a 1D line")
# See e.g. videos: https://youtu.be/MQdm0Z_gNcw and https://youtu.be/PvEl63t-opM by Cyrill Stachniss
ζ2ε = lambda X: A([(x/x[-1])[:-1] for x in X])

# Set the stage!
# https://www.geeksforgeeks.org/how-to-draw-shapes-in-matplotlib-with-python/
fig, ax = plt.subplots()
ax.set_xlim(-2, 6); ax.set_ylim(-1, 4); ax.set_aspect('equal'); plt.grid(True)

# The original square (with a kink) at the origin (notice the homogeneous coordinates)
sqwk = A([[0, 0, 1], [.75, .25, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])

# The ♪♫ eye of the beholder https://youtu.be/LbvdqjL-hJ0 ♫♪ (a.k.a. the observer)
# is at (ξ, θ) in Euclidean coordinates
# e.g. Start-Process PowerShell -WindowStyle Hidden -ArgumentList "<python path> .\MatrixTransforms2D.py '(π, -1/π)'"
ξ, θ = (π, -1/π) if len(eye) < 2 else eval(eye[1])

# https://en.wikipedia.org/wiki/Affine_transformation#Augmented_matrix
E = A([[1, 0, ξ],
       [0, 1, θ],
       [0, 0, 1]]) # It should be easy to create the inverse of E by hand

## The rigid transformation section (where the shape is preserved, i.e. no scaling, stretching, squeezing or shearing)
# Identity transformation (a.k.a. "do nothing but with great style!") - just to stretch the Python's cache legs... :D
sqwk = 文(I(3), sqwk); vertices = ζ2ε(sqwk)
polygon = Polygon(vertices, ec = 'xkcd:navy blue', fc = 'xkcd:true blue', alpha = 0.25)
# https://stackoverflow.com/questions/44526364/fill-matplotlib-polygon-with-a-gradient-between-vertices
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:blue', s = 25, alpha = 0.25)

# Translation by a vector [K L]...
K, L = π, π/3
T = I(3); T[:2, 2] = [K, L]

# ... and rotation by α degrees... https://en.wikipedia.org/wiki/Rotations_and_reflections_in_two_dimensions
# And don't bother about quaternions here, as they are merely for rotations in 3D...
# https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
# i² = j² = k² = ijk = -1 ← ad perpetuam rei memoriam... ;)
# https://en.wikipedia.org/wiki/Rotation_matrix#Decomposition_into_shears - if you think about it, a rotation
# is just a shear in disguise... ;)
α = 75*π/180
R = I(3); _R = A([[cos(α), -sin(α)],
                  [sin(α),  cos(α)]])
R[:2, :2] = _R

# ... and reflection: https://en.wikipedia.org/wiki/Householder_transformation#Householder_matrix
#                     https://upload.wikimedia.org/wikipedia/commons/f/f9/Householdertransformation.png
lx, ly = π/3, 2  # ... about the line from the origin (0, 0) through (lx, ly)
D, AD, DD = lx**2 - ly**2, 2*lx*ly, lx**2 + ly**2

M = I(3); _M = A([[ D, AD],
                  [AD, -D]])/DD
M[:2, :2] = _M

## Non-rigid transformation section
# Like scaling...
s = π/2
S = I(3); _S = A([[s, 0],
                  [0, s]])
S[:2, :2] = _S

## And so on... Procrustes would've been proud of us!
#  See https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:2D_affine_transformation_matrix.svg
#  and https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:Perspective_transformation_matrix_2D.svg

# ... or stretching
k, κ = π/2, π/3
ST = A([[k, 0, 0],
        [0, κ, 0],
        [0, 0, 1]])
# ... or squeezing

SQ = A([[1/k, 0, 0],
        [0,   κ, 0],
        [0,   0, 1]])
# ... and shearing (try κ = -k some day (why so?!))
SR = A([[1, κ, 0],
        [k, 1, 0],
        [0, 0, 1]])

# Feel free to further squeeze, stretch & shear the shape (and mix their order too)...
# as the ability to put all these transformations into a single matrix
# should blow you away out of the blue water... ;)

TM = M@T@R @ S@SQ@SR@ST
sqwk = 文(TM, sqwk); vertices = ζ2ε(sqwk)

polygon = Polygon(vertices, ec = 'xkcd:very dark blue', fc = 'xkcd:sky blue', alpha = 0.75)
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:royal blue', s = 25)

# ... and, eventually, the final projection (a.k.a. casting a shadow)...
# https://youtu.be/27vT-NWuw0M, https://youtu.be/JK-8XNIoAkI and https://youtu.be/cTyNpXB92bQ
# which is a linear operation too and can be represented by a matrix as well:
# https://wrfranklin.org/pmwiki/Main/HomogeneousCoords
# The shadow (a.k.a. the projection ;) of the final shape on the line Ax + By = 1
a, b = 0.5, -1.0
# ... altered when an observer is not at the origin (0, 0) but somewhere else (ThnX, GPT Astra 6.2..;)
D = 1 - a*ξ - b*θ
a /= D; b /= D
P = A([[1, 0, 0],
       [0, 1, 0],
       [a, b, 0]])

# Note that we can invoke the numpy.linalg.inv() function to compute the inverse of a matrix:
# from numpy.linalg import inv
# invE = inv(E)
# but here we can do it in a pure napkin and envelope math way:
invE = I(3); invE[:2, 2] = [-ξ, -θ]

TM = E@P@invE
shdw = 文(TM, sqwk); vertices = ζ2ε(shdw)
polygon = Polygon(vertices, ec = 'xkcd:dark navy blue', fc = 'xkcd:denim', alpha = 0.75)
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:dark blue', s = 25)

# And the ♪♫Moonlight shadows♫♪... https://youtu.be/ixExC-Zgyzc and https://youtu.be/e80qhyovOnA of the vertices.
# Is that song about Évariste Galois https://en.wikipedia.org/wiki/%C3%89variste_Galois#Final_days?
for v, w in zip(sqwk, shdw):
    # Homogeneous to Euclidean coordinates
    (x, y), (u, r) = v[:-1]/v[-1], w[:-1]/w[-1]
    ax.plot((ξ, x), (θ, y), c = 'xkcd:deep blue', lw = .5, ls = 'dashed')
    ax.plot((ξ, u), (θ, r), c = 'xkcd:navy blue', lw = .5, ls = 'dotted')
plt.title('Virtual glimmer-gap\n2D affine (incl. rigid & projective) transformations'); plt.show() #... must go on!

# See also https://en.wikipedia.org/wiki/Affine_transformation#/media/File:2D_affine_transformation_matrix.svg