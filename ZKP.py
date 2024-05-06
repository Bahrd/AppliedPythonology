## Zero-knowledge-proof (not a mathematical one!)
#  Discrete logarithm application ($p$ is prime and $g$ is a generator of the multiplicative group $mod p$)
#  https://en.wikipedia.org/wiki/Zero-knowledge_proof#Discrete_log_of_a_given_value
#  https://www.youtube.com/watch?v=FfeXX6OLq8w
#  https://www.youtube.com/watch?v=HUs1bH85X9I - Computerphile

from numpy import unique as unq
from numpy.random import randint, choice

## A brute force (thus good enough for small $p$'s) test for $g$:
prm = lambda p, g: True if(p - len(unq([g ** n % p for n in range(p)])) == 1) else False
# However, https://math.stackexchange.com/a/4484127 - and you can always find out if you are a lucky punk...

#  Both p and g are public... These numbers aren't arbitrary, so check if prm(p, g) == True
p, g = 0x61, 0x56 

# Alice's secret password x and its public 'signature' y
x = 101; y = g ** x % p

## Proof's loop (Victor verifies Alice's knowledge of the secret (more than) a few times)
for _ in range(0x10):
    #  Alice pick a random r
    r = randint(p - 1)
    # ... and publishes equally random C
    C = g ** r % p
    #  Each time Victor 'vehemently' questions Alice's credibility 
    #  with a random choice of the question...
    flip = choice(['trick', 'threat'])
    if(flip == 'trick'):
        #  Alice 
        c = (x + r) % (p - 1)
        v, V = (C * y) % p, g ** c % p
        #  Victor
        print(f"{v} == {V}. Trick's OK!" if (v == V) else f"{v} != {V}. Ain't OK!")
    else:
        v, V = C, g ** r % p
        #  Victor
        print(f"{v} == {V}. Threat's OK!" if (v == V) else f"{v} != {V}. Ain't OK!")

## Now Alice knows in advance that (silly) Victor will always (love her and) ask for r only... 
#  So she (being mischievously smart) prepares r' (rr) and yy = y⁻¹, publishes C' (CC) 
#  and provides Victors with c' (cc)...

#  Alice
rr, yy = randint(p - 1), pow(y, -1, p) 
cc, CC = g ** rr * yy % p, g ** rr % p
#  Victor
v, V = cc,  CC * yy % p
print(f"{v} == {V}. And Victor believes Alice every time..." if (v == V) else f"{v} != {V}. Whoa!!! Alice's caught!")