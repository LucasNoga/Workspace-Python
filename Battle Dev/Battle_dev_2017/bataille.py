# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/warriors.pdf

Objectif

Vous habitez une île sur laquelle une guerre tribale est sur le point d'éclater. Pour vous assurer d'être du côté du vainqueur, vous voulez prédire l'issue du massacre. Par chance, vous connaissez bien chaque tribu et vous savez que seule la quantité de combattants déterminera l'issue de la bataille.

Chaque tribu est dirigée par un chef de guerre. Il peut avoir à sa botte un ou plusieurs autres chefs de guerre, qui sont prêts à lui apporter leurs combattants pour la guerre. Un chef de guerre peut être le vassal de plusieurs supérieurs à la fois (par exemple le chef la tribu P peut prêter allégeance aux tribus Q et R), mais il va de soi qu'il n'y a pas de cycles dans la hiérarchie : par exemple, si A est le supérieur de B qui à son tour est le supérieur de C, C ne saurait être le supérieur de A.


Données

Entrée
Ligne 1 : un entier N compris entre 1 et 1000 représentant le nombre de tribus.
Lignes 2 à N+1 : Une suite de nombre entiers séparés par des espaces pour décrire une tribu. La première étant numérotée 0 la ligne i définit la tribu numéro i-2. Le premier nombre sur la ligne représente le nombre de combattants dans la tribu, compris entre 1 et 1000, et les autres nombres (s'il y en a) représentent la liste des autres tribus dont le chef de guerre a juré allégeance au dirigeant de la tribu i-2.

Sortie
Un entier représentant le nombre de combattants dont dispose le chef de guerre qui en a le plus, en comptant les combattants de sa tribu mais aussi des tribus de ses vassaux, ainsi que de ceux des vassaux de ces vassaux, etc.


def read_input():
    n = int(input())
    vassals = []
    power = []
    roots = set(range(n))
    for i in range(n):
        men, *line = map(int, input().split())
        power.append(men)
        vassals.append(line)
        roots -= set(line)
    return n, power, vassals, roots


def make_solver(power, vassals):
    def solve_for_one(i, visited):
        if i in visited:
            return 0
        visited.add(i)
        return power[i] + sum(solve_for_one(vassal, visited)
                              for vassal in vassals[i])
    return solve_for_one


def main():
    n, power, vassals, roots = read_input()
    solver = make_solver(power, vassals)
    return max(solver(root, set()) for root in roots)


print(main())
