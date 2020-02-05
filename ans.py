from math import floor, ceil, log2;
x = 1; p = 1/11; y = '100000000000000000000000000000000000001000000000011' # p = P(Y = 1)

## J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
# Encoding
for i in y[:: -1]:
    if (i == '0'):
        x = ceil((x + 1)/(1 - p)) - 1
    else:
        x = floor(x/p)

# Decoding
xx, zz = x, ''
for _ in range(len(y)):
    z = ceil((x + 1) * p) - ceil(x * p); zz += str(z)
    if z == 0:
        x -= ceil(x * p)
    else:
        x = ceil(x * p)

## Presentation
msg = "Message:{0}\nCode:\t{1}\nBits:\t{2} vs {3}\nDecoded:{4}"
print(msg.format(y, xx, len(y), floor(log2(xx) + 1), zz))