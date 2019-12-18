from math import floor, ceil;
x = 1; p = 1/11; y = '1000000000000000000010'

## J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
# Encoding
for i in y:
    #print(i)
    if (i == '0'):
        x = ceil((x + 1)/(1 - p)) - 1
    else:
        x = floor(x/p)
    #print(x)
print(x)
# Decoding
for i in range(len(y)):
    z = ceil((x + 1) * p) - ceil(x * p) 
    #print(z)
    if z == 0:
        x -= ceil(x * p)
    else:
        x = ceil(x * p)
    #print(x)
print(x)