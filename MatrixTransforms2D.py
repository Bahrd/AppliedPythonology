'''
https://en.wikipedia.org/wiki/3D_rotation_group - SO(3) (a nonabelian [non-commutative] group)
A.k.a. "The special orthogonal group in 3 dimensions"
SO(2) is a commutative (abelian) group though...
'''
from numpy import array, identity as I
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import pi as π, cos, sin

# Transform all polygon vertices
transform = lambda P, points: array([P @ p for p in points])
# Homogeneous to Euclidean coordinates
h2e = lambda X: array([(x/x[-1])[:-1] for x in X])

# Set the stage!
# https://www.geeksforgeeks.org/how-to-draw-shapes-in-matplotlib-with-python/
fig, ax = plt.subplots()
ax.set_xlim(-1, 4); ax.set_ylim(-1, 4); ax.set_aspect('equal'); plt.grid(True)

# The original square (with a kink) at the origin
sqwk = array([[0, 0, 1], [1, 0, 1], [1, 1, 1], [.25, .75, 1], [0, 1, 1]])

# Identity transformation (a.k.a. "do nothing but with great style!")
sqwk = transform(I(3), sqwk); vertices = h2e(sqwk)
polygon = Polygon(vertices, ec = 'xkcd:navy blue', fc = 'xkcd:true blue', alpha = 0.75)
# https://stackoverflow.com/questions/44526364/fill-matplotlib-polygon-with-a-gradient-between-vertices
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:blue', s = 25)

# Our square after translation by K and L...
K, L = 2, 2
T = array([[1, 0, K],
           [0, 1, L],
           [0, 0, 1]])
# ... and after rotation by α degrees... https://en.wikipedia.org/wiki/Rotations_and_reflections_in_two_dimensions
# And don't bother about quaternions here, as they are for 3D rotations only.
# https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
# But remember that by definition i² = j² = k² = ijk = -1
α = 75*π/180
R = I(3); _R = array([[cos(α), -sin(α)],
                      [sin(α),  cos(α)]])
R[:2, :2] = _R

# ... and scaling...
s = 0.75
S = I(3); _S = array([[s, 0],
                      [0, s]])
S[:2, :2] = _S

## And so on... Procrustes would've been proud of us!
#  See https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:2D_affine_transformation_matrix.svg
#  and https://en.wikipedia.org/wiki/Transformation_matrix#/media/File:Perspective_transformation_matrix_2D.svg
# Stretching:
k, κ = 3, -2
S1 = array([[k, 0, 0],
            [0, κ, 0],
            [0, 0, 1]])
# Squeezing:
S2 = array([[1/κ, 0, 0],
            [0,   κ, 0],
            [0,   0, 1]])
# Shearing:
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
sqwk = transform(M@T@S@R@S3, sqwk); vertices = h2e(sqwk)
polygon = Polygon(h2e(sqwk), ec = 'xkcd:very dark blue', fc = 'xkcd:sky blue', alpha = 0.75)
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:royal blue', s = 25)

# ... and, eventually, the final projection (a.k.a. casting a shadow)...
# https://youtu.be/27vT-NWuw0M, https://youtu.be/JK-8XNIoAkI and https://youtu.be/cTyNpXB92bQ
# which is a linear operation too and can be represented by a matrix as well:
# https://wrfranklin.org/pmwiki/Main/HomogeneousCoords
# The shadow of the final shape on the line Ax + By = 1
A, B = 0, 2/3
P = array([[1, 0, 0],
           [0, 1, 0],
           [A, B, 0]])
shdw = transform(P, sqwk); vertices = h2e(shdw)
polygon = Polygon(vertices, ec = 'xkcd:dark navy blue', fc = 'xkcd:denim', alpha = 0.75)
ax.add_patch(polygon); ax.scatter(vertices[:, 0], vertices[:, 1], color = 'xkcd:dark blue', s = 25)

# And the ♪♫Moonlight shadows♫♪... https://youtu.be/ixExC-Zgyzc and https://youtu.be/e80qhyovOnA of the vertices.
# Is that song about Évariste Galois https://en.wikipedia.org/wiki/%C3%89variste_Galois#Final_days?
for v, w in zip(sqwk, shdw):
    # Homogeneous to Euclidean coordinates
    (x, y), (u, r) = v[:-1]/v[-1], w[:-1]/w[-1]
    ax.plot((0, x), (0, y), c = 'xkcd:deep blue', lw = .5, ls = 'dashed')
    ax.plot((0, u), (0, r), c = 'xkcd:navy blue', lw = .5, ls = 'dotted')
plt.title('2D transformations\nrigid, linear, affine & projective'); plt.show()
