## See the 3B1B's videos first... 
# https://youtu.be/X8jsijhllIA and # https://youtu.be/b3NxrZOu_CE
# 'Hamming the humming data channel bits' [ We just couldn't help but play with these homophones!;]
# Hummingbird moth is left...

## A simple demonstration of the Hamming correction code
# In the real world we would need to fit 2ⁿ - n bits of the message into 
# 2ⁿ ones in locations between the dyadic ones: 2⁰,2¹,2²,…, 2ⁿ⁻¹).
# Here we... don't! That's the trick (see the videos): 
# 1. Create a random 2ⁿ-bit block and
# 2. Make it a proper Hamming coded message (so that its Hamming syndrome is zero).
from random import choice
from functools import reduce

n = 0b101
# The 'nest' is initially a sequence of random bits...
nest = [choice((0b0, 0b1)) for _ in range(0b1 << n)]
# Hamming syndrome computation (the subblock parity bits)
idx =  [i for i, b in enumerate(nest) if b] # Here the indices of 1's are collected
cuckoo = reduce(lambda x, y: x^y, idx)      # and XOR-ed to yield their Hamming syndrome
                                            # aka the incorrect bit (cuckoo?) location
nest[cuckoo] ^= 0b1                         # Kill [cuckoo] a mocking bird ... 
# The 'nest' is now Hamming coded!          # Savvy? https://youtu.be/xG6RHY_WJpM?t=129
print(f'{nest} - the correct block!')



# In order to emulate a humming-bird we flip a random bit
brd = choice(range(0b1 << n)); nest[brd] ^= 0b1
print(f'{nest} - the corrupted block!')
# To reveal the 'One [that] Flew Over the Cuckoo's Nest' straight away!
idx = [i for i, b in enumerate(nest) if b]
hmmng = reduce(lambda x, y: x^y, idx); print(f'Yippee-Ki-Yay {hmmng} == {brd}!')