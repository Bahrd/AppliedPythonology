'''
It ain't easy to find the area of the circle on a screen...
https://mathworld.wolfram.com/GausssCircleProblem.html
'''
from matplotlib.pyplot import plot, show, MarkerStyle
from math import floor, sqrt, pi as π
from numpy import add

## \[
#   GCA\left(r\right) = 1 + 4\left\lfloor r\right\rfloor 
#                         + 4\sum_{i = 0}^{\left\lfloor r\right\rfloor}
#                           \left\lfloor \sqrt{r^2 - i^2} \right\rfloor
## \]

def Gauss_circle_area(r: float):
    r_floor = int(floor(r))
    rs = [floor(sqrt(r*r - i*i)) for i in range(1, r_floor)]
    area = 1 + 4*r_floor + 4*add.reduce(rs)
    return area

## \[
#   GCA\_II\left(r\right) = 1 + 4\sum_{i = 1}^{r^2}
#                               \left\lfloor \frac{r^2}{2i - 1} \right\rfloor
## \]
# Caveat: O(r²) 
def Gauss_circle_area_II(r: float):
    rs = [(1 if i%2 == 1 else -1)*floor(r*r/(2*i - 1)) for i in range(1, int(r*r))]
    area = 1 + 4*add.reduce(rs)
    return area

for r in range(10,12):
    print(f'{Gauss_circle_area_II(r)} sq. pixels vs. {π*r**2:.2f} sq. whatevers')   
plot([Gauss_circle_area(r) - π*r**2 for r in range(0x400)], 'ko', ls='-', ms = 0o4, markerfacecolor = 'r' ), show()
