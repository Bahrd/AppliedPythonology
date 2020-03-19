from matplotlib.pyplot import plot, title, show
from random import randint as randy
from sys import argv

## The 'cc' is an acronym of the 'Collatz Conjecture': https://en.wikipedia.org/wiki/Collatz_conjecture
## There are three versions of the Collatz's sequence generators presented here:
# If one wants to put all stakes on a stack...
def cc_I(n): return [1] if n == 1 else [n] + (cc_I(3*n + 1) if n % 2 else cc_I(n >> 1))
# If one wants not to be stack-limited...
def cc_II(n):
    cs = []; 
    while(n != 1):
        cs += [n]; n = 3*n + 1 if(n % 2) else n >> 1
    return cs + [1]
# If one wants to look anonymously...
cc_III = lambda n : [1] if n == 1 else [n] + (cc_III(3*n + 1) if n % 2 else cc_III(n >> 1))


## ... and one of them is randomly picked to make a graph...
collatz = eval('cc_{0}'.format(randy(1, 3) * 'I'))
n = 27 if len(argv) != 2 else int(argv[1])
plot(collatz(n), 'ro'); title("Collatz's sequence for n = {0}".format(n)); show()

## The entire example matches the modeling and identification labs 
#  rather than the machine vision one... But it's just fun.

