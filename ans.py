from math import floor, ceil, log2 as lg2
from random import randint

# A probability p = P(X = '1') and the resulting entropy 'H = -∑pi⋅lg2(pi)'  

p = 1/4; H = (p - 1)*lg2(1 - p) - p*lg2(p) #[bit/smbl]

# A 'random' message...
prefix, suffix = ('11', '00') if randint(0, 1) else ('00', '11')
msg = prefix + 0x4 * '0' + suffix
print(f'P(X = \'1\') = 1/{1/p:,.0f}\nEntropy:{H:,.2f} [bit/symbol]\n\nMessage:{msg}')

## J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
# Encoding
enc = 0
for n in msg[:: -1]:
    enc = ceil((enc + 1)/(1 - p)) - 1 if n == '0' else floor(enc/p)

# Decoding
code, dec = enc, ''
for _ in range(len(msg)):
    z = ceil((enc + 1) * p) - ceil(enc * p)
    dec += str(z)
    enc = enc - ceil(enc * p) if z == 0 else ceil(enc * p)

## Presentation
ly, lc = len(msg), floor(lg2(code) + 1); rlc = 0o144 * lc/ly
rprt = 'Encoded:{}\nBits:\t{} vs {} ({:,.0f}%)\n\nDecoded:{}'
print(rprt.format(code, ly, lc, rlc, dec))