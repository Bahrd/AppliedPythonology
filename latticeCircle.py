'''
It ain't easy to find the area of the circle on a screen...
https://mathworld.wolfram.com/GausssCircleProblem.html
'''
from matplotlib.pyplot import plot, show
from math import floor, sqrt, pi as π
from numpy import add

r'''
$$
   GCA\left(r\right) = 1 + 4\left\lfloor r\right\rfloor
                         + 4\sum_{i = 1}^{\left\lfloor r\right\rfloor}\left\lfloor \sqrt{r^2 - i^2} \right\rfloor
$$
'''

def Gauss_circle_area(r: float):
    r_floor = int(floor(r))
    rs = [floor(sqrt(r*r - i*i)) for i in range(1, r_floor)]
    area = 1 + 4*r_floor + 4*add.reduce(rs)
    return area

for r in (10, 13):
    print(f'{Gauss_circle_area(r) = } sq. pixels vs. {π*r**2 = :.2f} sq. whatevers')   
plot([Gauss_circle_area(r) - π*r**2 for r in range(0x400)], 'ko', ls='-', ms = 0o4, markerfacecolor = 'r' ), show()

