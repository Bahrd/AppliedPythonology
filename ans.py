from math import floor, ceil, log2 as lg2 
from random import randint

# A probability p = P(X = '1') is set quite arbitrarily
L = 0x10; p = 1/L
# The resulting entropy is just (an) average 'H = -∑ᵢpᵢ⋅lg₂pᵢ'  
H = -(1 - p) * lg2(1 - p) - p * lg2(p) #[bit/smbl]

# A 'random' message... (with a fair chance of having a single '1' somewhere...)
msg, ll = list(L * '0'), randint(0, L)
if ll < L: msg[ll] = '1' 
msg = ''.join(msg)

## J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
print('—' * 0o100, f"\nEncoding: '{msg}'")
# Encoding
enc = 0
for n in msg[:: -1]:
    enc = ceil((enc + 1)/(1 - p)) - 1 if n == '0' else floor(enc/p)
    print(f"'{n}' → {bin(enc):{L}}")        # Enlightening I

print('—' * 0o100, f'\nDecoding: {bin(enc)} ({enc})')
# Decoding
code, dec = enc, ''
l = ceil(lg2(enc)) + 0b10
for _ in msg:
    print(f'{bin(enc):{l}}', end = ' → ')   # Enlightening II.I
    z = ceil((enc + 1) * p) - ceil(enc * p)
    dec += str(z)
    enc = enc - ceil(enc * p) if z == 0 else ceil(enc * p)
    print(f"'{dec}'")                       # Enlightening II.II

# Presentation                              
ly, lc = len(msg), floor(lg2(code) + 1)
print('—' * 0o100, f'\nP(X = \'1\') = 1/{L} → Entropy = {H:.2f} [bit/symbol]')
print(f"Message: '{msg}'\nEncoded:  {bin(code)}")
print(f"Compression: {ly} → {lc} ({lc/ly:,.0%})\nDecoded: '{dec}'")