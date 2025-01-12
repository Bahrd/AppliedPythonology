## See this first and foremost: https://www.youtube.com/watch?v=Rqv3cXt8ZNU

# Yet another formatting subroutine - nothing to see here, move along!
def show(expression):
    global V
    p, lv = lambda _: print(_, end = ''), list(V)
    c = 0

    for i, x in enumerate(expression):
        if x > 0:
            if c > 0:
                p('+')
            if x != 1:
                p(f'{x:.0f}')
            p(f'{lv[i]}')
            c += 1
        if x < 0:
            if x != -1:
                p(f'{x:.0f}')
            else:
                p('-')
            p(f'{lv[i]}')
            c += 1
    print()

from numpy import array as A
from numpy.linalg import inv
# Mapping functions to vectors
V = {'x⋅sin(x)': A([1, 0, 0, 0]),
     'x⋅cos(x)': A([0, 1, 0, 0]),
       'sin(x)': A([0, 0, 1, 0]),
       'cos(x)': A([0, 0, 0, 1])}

# Embedding differentiation into a matrix...
D = A([[0, -1, 0,  0],
       [1,  0, 0,  0],
       [1,  0, 0, -1],
       [0,  1, 1,  0]])
# ... and integration as its inverse (of course!)
ID = inv(D)

## Elementary educational example
w = 7*V['sin(x)'] + 3*V['x⋅sin(x)'] - 5*V['x⋅cos(x)']
show(w)

# Differentiation is so easy...
derivative = D@w
show(derivative)

# ... and so is double integration!
integral = ID@ID@derivative
show(integral)

# Checkpoint: the derivative of the integral should yield the original expression
original = D@integral
show(original)

if (original == w).all():
    print('Yippee ki-yay!')
