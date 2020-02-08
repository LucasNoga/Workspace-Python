Énoncé



La notation usuelle pour les expressions arithmétiques nécessite des parenthèses afin de lever les ambiguïtés. Une autre convention (nommée polonaise préfixée) consiste à préciser l'opérateur (+, -, x ou /) avant les opérandes. Ainsi :- 3 + 4 devient + 3 4 ;

- (2 + 3) * 7 devient * + 2 3 7 ;

- 7 * (4 + 7) devient * 7 + 4 7 ;

- (1 + 2) * (3 - 4) devient * + 1 2 - 3 4.Les parenthèses ne sont alors plus nécessaires.



Plus formellement, voici une définition récursive. Une expression est une chaîne de caractères de la forme :- N où N est un nombre compris entre 0 et 42 ;

- ou bien OP EXPR1 EXPR2 où OP est un opérateur parmi +, -, * ou / et EXPR1, EXPR2 sont des expressions.

Vous devez déterminer le résultat de l'opération arithmétique correspondante.



Les résultats des divisions devront être arrondis à l'entier inférieur, par exemple le résultat de l'expression / 8 5 sera 1 et non 1,6.



Format des données



Entrée

Ligne 1 : une expression arithmétique sous la forme définie ci-dessus. Les différents éléments composants l'expression sont séparés par des espaces. Il n'y a pas de division par zéro dans l'expression.



Sortie

Un entier représentant le résultat de l'évaluation de l'expression.



#*****
# Solution de Gangrene
#**/

import sys

equation = input().split()
cache = []
result = 0

for s in equation:
    if s.isnumeric():
        v = int(s)
        while cache and isinstance(cache[-1],(int,float)):
            v2 = cache.pop()
            op = cache.pop()
            v = int(eval("%s %s %s" % (v2,op,v)))
        cache.append(v)
    else:
        cache.append(s)

print(cache[0])


