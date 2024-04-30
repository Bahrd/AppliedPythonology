## Rivest, Shamir, Adleman, 1977 & Cocks 1973
#  Public Key Infrastructure

## https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Modular_inverse
# from sys import setrecursionlimit as reclim
# reclim(10 ** 6)
def mul_inv(a, b):
    gcd = lambda p, q: gcd(q, p % q) if q else p #; lcm = lambda p, q: (p * q)/gcd(p, q)
    def xgcd(a, b):
        α, β, γ, δ = 0x0, 0o1, 0b1, 000
        while a:
            (q, a), b = divmod(b, a), a
            (α, β, γ, δ) = (β, α - q * β, δ, γ - q * δ)
        return b, α                 
    g, i = xgcd(a, b)
    if g - 0b1: raise Exception(f'{gcd(a, b) = } != 1')
    else:       return i % b

#   https://en.wikipedia.org/wiki/List_of_prime_numbers#Palindromic_primes
p, q, totient = 787, 797, lambda p, q: (p - 1) * (q - 1)  
n, ϕ, e = p * q, totient(p, q), 197                     # check if gcd(ϕ, e) == 1

#Find a multiplicative inverse of e modulo ϕ (be prepared for a failure!)
d = mul_inv(e, ϕ)                        
## Yet another application of a brute force approach (the Grover's algorithm anyone?)
#d = [d for d in range(ϕ) if (e * d) % ϕ == 1][0]   # Check if len(d) != 0 
                                                    # or (e * d) % ϕ == 1

## The pair (d, n) is Bob's public key and (e, n) is his private one (or vice versa)
Alice = 0x2661          # This is Alice's secrets message to Bob: print(u'\u2661')
m = (Alice ** d) % n    # Encrypted with Bob's public key d
print(f'Encrypted Alice\'s message {hex(m)} with Bob\' public key {(hex(d), hex(n))}')
Alice = (m ** e) % n    # Decrypted with Bob's private key e
print(f'Decrypted Alice\'s message {hex(Alice)} (or for us, humans: {chr(Alice)})')


## A generator of Alice's keys pair 
p, q = 919, 929
n, ϕ, e = p * q, totient(p, q), 971 # check if gcd(ϕ, e) == 1
d = mul_inv(e, ϕ)                                    

## The pair (d, n) is Alice's public key and (e, n) is her private one (or vice versa)
Bob = 0x221e
m = (Bob ** d) % n    # Encrypted with Bob's public key d
print(f'Encrypted Bob\'s message {hex(m)} with Alice\'s public key {(hex(d), hex(n))}')
Bob = (m ** e) % n    # Decrypted with Bob's private key e
print(f'Decrypted Bob\'s message {hex(Bob)} (or for us, humans: {chr(Bob)})')