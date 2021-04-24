from numpy import unique as unq
from numpy.random import randint
# Brute force is not the smartest way to check if p is a primitive root modulo q
# But in quantum computing version they call it the Grover's algorithm...
prm = lambda p, q: True if(p - len(unq([q**n % p for n in range(p)])) == 1) else False
hexen = lambda xeh: tuple([hex(n) for n in xeh])

## Diffie–Hellman–Merkle, 1976 & Cocks, 1969 
#  Private key public distribution
p, q = 0x61, 0x56                               # These numbers aren't arbitrary! 
                                                # Check if prm(p, q) == True

Alice, Bob = randint(0x2661), randint(0x221e)   # A pair of Alice and Bob's random secret values
A, B = (q ** Alice) % p, (q ** Bob) % p         # Public exchange messages

print(f'Take that {hexen((p, q, A, B))}, Eve!') # It's all public! Isn't it odd, even Eve knows 
sA, sB = (B ** Alice) % p, (A ** Bob) % p       # them all? Yet only Alice and Bob know their 
                                                # new secret (since sA == sB)...

print(f'Alice&Bob\'s secret key: {hex(sA)}.')   # Once they used the key, should they publish it?
print(f'Eve, ♫you still haven\'t found what you\'re looking for♫: {hex(sB)}?')    
                                                # ♫Ups, we did it again!♫ ;]
                                                # A.k.a the Midas' barber syndrome...