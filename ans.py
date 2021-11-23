from math import floor, ceil, log2 as lg2
from random import choice

# A probability p = P(X = '1') and the resulting entropy 'H = -∑ pi⋅lg2(pi)'  
p = 1/0o10; H = (p - 1) * lg2(1 - p) - p * lg2(p) #[bit/smbl]
# A 'random' message...
msg = '1' + 0o10 * '0'; msg = msg[:: choice([-0o1, 0o1])]
print(f'P(X = \'1\') = 1/{1/p:,.0f}\nEntropy:{H:,.2f} [bit/symbol]\n\nMessage:{msg}')

## J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
# Encoding
enc = 0
for n in msg[:: -1]:
    enc = ceil((enc + 1)/(1 - p)) - 1 if n == '0' else floor(enc/p)
    print(bin(enc))     # Enlightening I

# Decoding
code, dec = enc, ''
for _ in range(len(msg)):
    z = ceil((enc + 1) * p) - ceil(enc * p)
    dec += str(z)
    enc = enc - ceil(enc * p) if z == 0 else ceil(enc * p)
    print(bin(enc))     # Enlightening II

## Presentation         # Enlightening III
ly, lc = len(msg), floor(lg2(code) + 1); rly = lc/ly
print(f'Encoded:{bin(code)}\nBits:\t{ly} vs {lc} ({rly:,.0%})\nDecoded:{dec}')