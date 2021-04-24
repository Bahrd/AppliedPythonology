## See the 3B1B's videos first... 
# https://youtu.be/X8jsijhllIA and # https://youtu.be/b3NxrZOu_CE

## A simple demonstration of the Hamming(2ⁿ - 1, 2ⁿ - n - 1) correction code
#  In the real world we would need to intertwin 2ⁿ - n bits of the message with 
#  2ⁿ parity bits (located at dyadic locations: 2⁰, 2¹, 2², …, 2ⁿ⁻¹).
#  Here we... don't! That's the trick (see the videos): 
#  1. Create a random 2ⁿ-bit block and
#  2. Make it a proper Hamming coded message (so that its Hamming 
#     syndrome is zero). If it is not, it shows a position of the fault bit. 
from numpy.random import choice
from functools import reduce

# 'Hamming the humming data channel bits' [ We just couldn't help but play with these homophones!;]
#  Hummingbird moth is left (Note a slew of other, rather questionable, «puns»!), however...

# The Hamming syndrome routine (Seen the video?):
# 1. The indices of 1's are collected
# 2. and XOR-ed to yield their Hamming syndrome (that is, the incorrect bit (a hatched cuckoo?) location)
syndrome = lambda nest: reduce(lambda x, y: x^y, [i for i, b in enumerate(nest) if b])

# An initially empty nest is filled with random bits (or birds...)
n = 0b101; m, r = (0b1 << n) - 1, (0b1 << n) - (n + 1)
nest = choice((0b0, 0b1), 0b1 << n)
                                       
cuckoo = syndrome(nest)                                            
nest[cuckoo] ^= 0b1   # Kill a mocking[cuckoo]bird... so that the 'nest' is now Hamming coded!
                      # Savvy? https://youtu.be/xG6RHY_WJpM?t=129
print(f'{nest} → this H{m, r} code block seems «correct»!')

# In order to emulate a humming-bit we flip a random bird (or vice-versa?)
brd = choice(0b1 << n); nest[brd] ^= 0b1
print(f'{nest} → this H{m, r} code block is «corrupted»!')  
# To reveal the 'One [that] Flew Over the Cuckoo's Nest' straight away!
hmmng = syndrome(nest); print(f'{hmmng} == {brd} → Yippee-Ki-Yay!')