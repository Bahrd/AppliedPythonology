''' ## Yes, yes! Bayes!
    https://en.wikipedia.org/wiki/Bayes%27_theorem
    https://en.wikipedia.org/wiki/Type_I_and_type_II_errors
    
    Null hypothesis: 'The guy is innocent.'
    False positives (or 'type I error'):
    * 'convicting an innocent'
    * 'rejecting the (true) null hypothesis'
    False negatives (or 'type II error'): 
    * 'acquitting a criminal', 
    * 'failing to reject the (false) null hypothesis'
    
    https://en.wikipedia.org/wiki/Type_III_error#Mosteller
    False positives (or 'type III error'):
    * 'convicting a criminal using fabricated evidence', 
    * 'rejecting the (false) null hypothesis for the wrong reason'
'''                    
def Bayes_formula(p_a_priori: float, p_false_positives: float, p_true_positives: float) -> float:
    p_au_contraire = 1 - p_a_priori
    p_positives = p_true_positives * p_a_priori + p_false_positives * p_au_contraire
    p_a_posteriori = p_true_positives * p_a_priori/p_positives
    return p_a_posteriori
''' A randomly matching epigraph...
    Skipper:    Kowalski, what's our trajectory?                            [100/100]
    Kowalski:   Ninety-five percent certain we're still doomed.             [1 - 1/20]
    Skipper:    And the, uh... other five percent?                          [1/20]
    Kowalski:   Adventure and glory like no penguins have ever seen before. '''
from sys import argv      # .\Bayes4all.py '(1/100, 1/100, 1 - 1/100)' # a.k.a fifty-fifty
a_priori, false_positives, true_positives = (1/100, 1/100, 1 - 1/100) if len(argv) != 0b10 else eval(argv[0b1])
## Run, Bayes! Run!
a_posteriori = a_priori
print(f'For false positives probability = {false_positives} and occurence probability = {a_priori} the chances are:')
while(a_posteriori <= 1 - 1/10000):
    a_posteriori = Bayes_formula(a_posteriori, false_positives, true_positives)
    print(f'{100 * a_posteriori:.4g}%')

'''
A tandem of mediocre classifiers:
For false positives rate = 0.01 and occurence probability = 0.001 the chances are:
9.099%
90.92%
99.9%
100%
A single (almost) perfect classifier:
For false positives rate = 0.0001 and occurence probability = 0.001 the chances are:
90.92%
100%
'''