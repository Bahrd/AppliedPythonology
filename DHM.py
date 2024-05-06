''' 
  Diffie–Hellman–Merkle, 1976 & Cocks, 1969 
  Private key public distribution (for e.g. a symmetric-key cipher)
  *  https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation
  *  https://youtu.be/NmM9HA2MQGI?t=52 and https://youtu.be/Yjrfm_oRO0w - Computerphile (they say it's unbelievable difficult [to understand or to crack?])
  *  https://www.youtube.com/watch?v=ESPT_36pUFc - PBS Infinite Series (neatly explained in a "one-way" fashion)
  *  https://youtu.be/F3zzNa42-tQ [or just go for what looks like a source of the video: https://link.springer.com/book/10.1007/978-3-642-04101-3]
  
  See also: https://www.youtube.com/watch?v=NCuiwCM-AQ8 "Why are periodic systems so unpredictable?"
'''
from numpy import unique as unq
from numpy.random import randint
# Brute force is not exactly the smartest way to check if p is a primitive root modulo q
# But in the quantum computing realm they call it the Grover's algorithm...
prm = lambda p, q: True if(p - len(unq([q ** n % p for n in range(p)])) == 1) else False
hexen = lambda xeh: tuple([hex(n) for n in xeh])

p, q = 0x61, 0x56 # These numbers aren't arbitrary:    https://en.wikipedia.org/wiki/Primitive_root_modulo_n
                  # YMMV so check if prm(p, q) == True https://math.stackexchange.com/a/4484127 

Alice, Bob = randint(0x2661), randint(0x221e)           # A pair of Alice and Bob's random secret values
A, B = (q ** Alice) % p, (q ** Bob) % p                 # Public exchange messages

print(f'Take that {hexen((p, q, A, B))}, Eve!')         # It's all public! Isn't it odd? Even Eve knows them!
sA, sB = (B ** Alice) % p, (A ** Bob) % p               # them all? Yet only Alice and Bob know their 
                                                        # new secret (since sA == sB)...
# «Roman à clef» [ ♫Ups, we did it again!♫ ;]
print(f'Eve, ♫... and you still haven\'t found what you\'re looking for♫?') # Once they've used the key, can they spill the beans?
print(f'Alice&Bob\'s secret keys: {hexen((sA, sB))}.')                      # The Midas' barber syndrome...