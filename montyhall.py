from random import randint, choice

## There is a famous and (supposedly) counterintuitive no-problem: 
#   https://en.wikipedia.org/wiki/Monty_Hall_problem
#   "El sueño de la razón produce experimentos!" F. Goya would have said...

trialsNo, trial, wins = 100, 0, 0

## To switch or not to switch...  # bool(random.getrandbits(1)) 
switch = choice([True, False])

while trial < trialsNo:
## Selecting a gate with an award and a player's guess
    award, guess = choice([1, 2, 3]), choice([1, 2, 3])
    if award == guess:      ## You'd been correct (P = 1/3)
        if switch:
            ...
            #print('Lose!') #  But since you changed that decision...
        else:
            #print('Win!')   
            wins += 1
    else:                   ## You'd been incorrect (P = 2/3)
        if switch:          #  But you'd always win should you switch now!
            #print('Win!')  #  Because you'd selected a wrong one and the host revealed
            wins += 1       #  the other wrong one. So you always switch to the right one!
        else:
            ...             ## And you remain so...
    trial += 1

print('Win ratio = {}% if switch = {}'.format(round(wins/trialsNo*100, 1), switch))
## Move along, nothing to see here...