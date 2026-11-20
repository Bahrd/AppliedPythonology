'''
https://en.wikipedia.org/wiki/3D_rotation_group - SO(3) (a non-abelian [non-commutative] group)
A.k.a. "The special orthogonal group in 3 dimensions"
SO(2) is a commutative (abelian) group though...

An eagle eye will surely notice that this script is a 2D version of the 3D virtual window... ;)
Let's call it a "virtual glimmer-gap" (ThnX Copilot for that term... ;)
'''
from numpy import array, identity as I
from numpy.linalg import inv
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import pi as π, cos, sin

from sys import argv as eye

# Transform all polygon vertices
文 = lambda P, points: array([P @ p for p in points])
# Homogeneous to Euclidean coordinates
# See e.g. videos: https://youtu.be/MQdm0Z_gNcw and https://youtu.be/PvEl63t-opM by Cyrill Stachniss
ζ2ε = lambda X: array([(x/x[-1])[:-1] for x in X])

# Set the stage!
# https://www.geeksforgeeks.org/how-to-draw-shapes-in-matplotlib-with-python/
fig, ax = plt.subplots()
ax.set_xlim(-1, 9); ax.set_ylim(-2, 8); ax.set_aspect('equal'); plt.grid(True)

# The original square (with a kink) at the origin (notice the homogeneous coordinates)
sqwk = array([[0, 0, 1], [1, 0, 1], [1, 1, 1], [.25, .75, 1], [0, 1, 1]])

# The ♪♫ eye of the beholder https://youtu.be/LbvdqjL-hJ0 ♫♪ (a.k.a. the observer)
# is at (ex, ey) in Euclidean coordinates
# e.g. python .\MatrixTransforms2D.py '(2*π, -1/π)'
ex, ey = (π, -1) if len(eye) < 2 else eval(eye[1])
E = array([[1, 0, ex],
           [0, 1, ey],
           [0, 0, 1]])

# Identity transformation (a.k.a. "do nothing but with great style!") - just to stretch the Python's cache legs... :D
sqwk = 文(I(3), sqwk); vertices = ζ2ε(sqwk)
polygon = Polygon(vertices, ec = 'xkcd:navy blue', fc = 'xkcd:true blue', alpha = 0.75)
# https://stackoverflow.com/questions/44526364/fill-matplotlib-polygon-with-a-gradient-between-vertices
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:blue', s = 25)

# Our kinked square after translation by a vector [K L]...
K, L = 3, 4
T = array([[1, 0, K],
           [0, 1, L],
           [0, 0, 1]])

# ... and after rotation by α degrees... https://en.wikipedia.org/wiki/Rotations_and_reflections_in_two_dimensions
# And don't bother about quaternions here, as they are merely for rotations in 3D...
# https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
# But remember that by definition i² = j² = k² = ijk = -1
α = 75*π/180
R = I(3); _R = array([[cos(α), -sin(α)],
                      [sin(α),  cos(α)]])
R[:2, :2] = _R

# ... and scaling...
s = 1.5
S = I(3); _S = array([[s, 0],
                      [0, s]])
S[:2, :2] = _S

## And so on... Procrustes would've been proud of us!
#  See https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:2D_affine_transformation_matrix.svg
#  and https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:Perspective_transformation_matrix_2D.svg
# Stretching:
k, κ = 3, 2
S1 = array([[k, 0, 0],
            [0, κ, 0],
            [0, 0, 1]])
# Squeezing:
S2 = array([[1/κ, 0, 0],
            [0,   κ, 0],
            [0,   0, 1]])
# Shearing: (try κ = -k some day (why so?!))
S3 = array([[1, k, 0],
            [κ, 1, 0],
            [0, 0, 1]])

# Reflection: https://en.wikipedia.org/wiki/Householder_transformation#Householder_matrix
#             https://upload.wikimedia.org/wikipedia/commons/f/f9/Householdertransformation.png
lx, ly = 1, 2   # ... about the line from the origin (0, 0) through (lx, ly)
M = I(3)
_M = array([[lx**2 - ly**2,     2*lx*ly  ],
            [    2*lx*ly  , ly**2 - lx**2]])
_M = _M/(lx**2 + ly**2)
M[:2, :2] = _M

# Feel free to further squeeze, stretch, shear the shape (and mix the order too)...
# as the ability to put all these transformations into a single matrix
# should blow you away out of the blue...

TM = M@T@S@R@S3
sqwk = 文(TM, sqwk); vertices = ζ2ε(sqwk)

polygon = Polygon(vertices, ec = 'xkcd:very dark blue', fc = 'xkcd:sky blue', alpha = 0.75)
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:royal blue', s = 25)

# ... and, eventually, the final projection (a.k.a. casting a shadow)...
# https://youtu.be/27vT-NWuw0M, https://youtu.be/JK-8XNIoAkI and https://youtu.be/cTyNpXB92bQ
# which is a linear operation too and can be represented by a matrix as well:
# https://wrfranklin.org/pmwiki/Main/HomogeneousCoords
# The shadow (a.k.a. the projection ;) of the final shape on the line Ax + By = 1
A, B = 0.5, -1.0
# ... altered when an observer is not at the origin (0, 0) but at somewhere else at (ex, ey) instead.
D = 1 - A*ex - B*ey
A /= D; B /= D
P = array([[1, 0, 0],
           [0, 1, 0],
           [A, B, 0]])
shdw = 文(E@P@inv(E), sqwk); vertices = ζ2ε(shdw)
polygon = Polygon(vertices, ec = 'xkcd:dark navy blue', fc = 'xkcd:denim', alpha = 0.75)
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:dark blue', s = 25)

# And the ♪♫Moonlight shadows♫♪... https://youtu.be/ixExC-Zgyzc and https://youtu.be/e80qhyovOnA of the vertices.
# Is that song about Évariste Galois https://en.wikipedia.org/wiki/%C3%89variste_Galois#Final_days?
for v, w in zip(sqwk, shdw):
    # Homogeneous to Euclidean coordinates
    (x, y), (u, r) = v[:-1]/v[-1], w[:-1]/w[-1]
    ax.plot((ex, x), (ey, y), c = 'xkcd:deep blue', lw = .5, ls = 'dashed')
    ax.plot((ex, u), (ey, r), c = 'xkcd:navy blue', lw = .5, ls = 'dotted')
plt.title('Virtual glimmer-gap\n2D transformations: rigid, linear, affine & projective'); plt.show() #... must go on!
