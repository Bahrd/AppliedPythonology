﻿''' J. Duda 2007 ANS/ABC (see: http://mattmahoney.net/dc/dce.html#Section_33)
    
    You should still be careful - the conversion from ints to floats has
    its limitations (if 'enc > 2^53', it will not be converted correctly since
    float(9007199254740992 + n) - 9007199254740992 = 0, for any non-negative n
  
'''
from decimal import Decimal as DeX, getcontext as gctx
from math import floor, ceil, log2 as lg2 
import sys

#    Using Decimals instead helps a little bit (or two, or even more ;) 
#    to alleviate the limitation, though...
#    https://docs.python.org/3/library/decimal.html
gctx().prec = 0x100

# A probability p = P(X = 1) can be set quite arbitrarily
p = 1/2 if len(sys.argv) < 0b10 else eval(sys.argv[1])

# The resulting entropy is just (an) average information 
#            'H = ∑ᵢpᵢ⋅I(pᵢ) = -∑ᵢpᵢ⋅lg₂pᵢ'  
H = (p - 1) * lg2(1 - p) - p * lg2(p)        #[bit/smbl]
print('—' * 0o100, f'\nP(X = 1) = {p}', 
                   f' → Entropy = {round(H, 4)} [bit/symbol]')

while True:
    msg = input()
    if msg in ('EOC', ''): 
        break
    # For format's sake!
    L = len(msg)    
    # Encoding (Note that it amounts to the standard binary system 
    #           (with 0 and 1 inverted) when p = 2⁻¹)
    #           https://en.wikipedia.org/wiki/Asymmetric_numeral_systems
    print('—' * 0o100, f'\nEncoding: {msg}')
    
    p, enc = DeX(p), DeX(0o0)
    for n in msg:
        enc = ceil((enc + 1)/(1 - p)) - 1 if n == '0' else floor(enc/p)
        # Enlightening I
        print(f'{n} → {bin(enc):{L}}')
    
    print('—' * 0o100, f'\nDecoding: {bin(enc)} ({enc})')
    # Decoding
    code, dec = enc, ''
    l = ceil(lg2(enc)) + 0b10 if enc else 0o1
    for _ in msg:
        # Enlightening II.I
        print(' ' * 0b11, f'{bin(enc):{l}}', end = ' → ')    
        
        z = ceil((enc + 1) * p) - ceil(enc * p)
        dec = str(z) + dec
        enc = enc - ceil(enc * p) if z == 0 else ceil(enc * p)
        # Enlightening II.II
        print(f'{dec}')

    # Presentation                              
    ly, lc = len(msg), floor(lg2(code) + 1) if code else 1
    print('—' * 0o100, f'\nMessage:   {msg}\nEncoded: {bin(code)}')
    print(f'Decoded:   {dec}\n\nRatio:     {ly} → {lc} ({lc/ly:,.0%})')