from numpy import unique as unq
from numpy.random import randint, choice

# A brute force (thus good enough for small $p$'s) test for $g$
prm = lambda p, g: True if(p - len(unq([g ** n % p for n in range(p)])) == 1) else False

## Zero-knowledge-proof 
#  Discrete logarithm application ($p$ is prime and $g$ is a generator of the multiplicative group $mod p$)
#  https://en.wikipedia.org/wiki/Zero-knowledge_proof#Discrete_log_of_a_given_value
p, g = 0x61, 0x56 # These numbers aren't arbitrary, so check if prm(p, g) == True


# Peggy's password and its 'signature'
x = 101
y = g ** x % p


## Proof loop
for _ in range(0x10):
    #  Peggy 
    r = randint(p - 1)

    C = g ** r % p
    #  Victor
    flip = choice(['trick', 'threat'])
    if(flip == 'trick'):
        #  Peggy 
        m = (x + r) % (p - 1)
        v, V = (C * y) % p, g ** m % p
        
        #  Victor
        print("Trick's OK!" if (v == V) else "Ain't OK!")
    else:
        m = r
        v, V = C, g ** r % p
        #  Victor
        print("Threat's OK!" if (v == V) else "Ain't OK!")