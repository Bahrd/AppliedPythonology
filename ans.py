from math import floor, ceil, log2 as lg2
from random import randint

# A probability p = P(X = '1') and the resulting entropy 'H = -∑ pᵢ⋅lg₂pᵢ'  
L = 0x10; p = 1/L; H = -(1 - p) * lg2(1 - p) - p * lg2(p) #[bit/smbl]
# A 'random' message... (with a 100% chance of having '1' somewhere...)
msg = L * '0'; msg = list(msg)
msg[randint(0, L - 1)] = '1'
msg = ''.join(msg)

print(f'\nP(X = \'1\') = 1/{1/p:,.0f} → Entropy = {H:,.2f} [bit/symbol]')
print(f'\nMessage: {msg}')

## J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
# Encoding
enc = 0
for n in msg[:: -1]:
    enc = ceil((enc + 1)/(1 - p)) - 1 if n == '0' else floor(enc/p)
    print(enc, '→', bin(enc))     # Enlightening I

print()
# Decoding
code, dec = enc, ''
for _ in range(len(msg)):
    print(enc, end = ' → ')
    z = ceil((enc + 1) * p) - ceil(enc * p)
    dec += str(z)
    enc = enc - ceil(enc * p) if z == 0 else ceil(enc * p)
    print(dec)          # Enlightening II
## Presentation         # Enlightening III
ly, lc = len(msg), floor(lg2(code) + 1); rlcy = lc/ly
print(f'emmonP(X = \'1\') = 1/{1/p:,.0f} → Entropy = {H:,.2f} [bit/symbol]')
print(f'Message: {msg}\nEncoded: {bin(code)}\nBits:\t {ly} vs {lc} ({rlcy:,.0%})\nDecoded: {dec}')