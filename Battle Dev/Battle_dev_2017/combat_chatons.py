# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/kittenfight.pdf

Objectif

Après avoir passé trop de temps à regarder des vidéos de chat sur Internet, vous vous êtes pris d'une passion pour les félins qui vous a mené à découvrir un terrible secret : un trafic de petits chatons trop mignons qui sont modifiés génétiquement pour être envoyés au combat. Vous décidez donc… de participer vous aussi à l'exploitation des animaux, en vous constituant une petite équipe et en défiant d'autres dresseurs de chatons en duel !

Les chatons ont un type qui régit l'issue de leurs combats. Les chatons eau gagnent contre les chatons feu, qui battent les chatons plante, ces derniers l'emportant face aux chatons eau ; et si deux chatons ont le même type, le combat se solde par une égalité.

Un duel se déroule comme suit : vous et votre adversaire désignez chacun un chaton parmi vos équipes pour s'affronter. En cas d'égalité, les deux chatons finissent K.O. et doivent être remplacés : vous devez désigner un autre chaton qui prendra sa place, et de même pour votre adversaire. Sinon, seul le chaton perdant est mis K.O., et son maître doit le remplacer par un autre membre de son équipe, qui affrontera le chaton qui vient de gagner. Évidemment, le premier joueur dont toute l'équipe est K.O. a perdu, sauf si cela se produit simultanément pour les deux joueurs, auquel cas il y a ex-æquo.

En l'occurrence, vous avez un adversaire pas très malin, qui a décidé qu'il sortirait ses chatons dans un ordre fixe sans réagir à ce que vous faites. De plus, vous connaissez cet ordre. Pouvez-vous en tirer parti pour planifier dans quel ordre envoyer vos propres chatons afin de gagner ?

Indication : on pourra procéder par énumération exhaustive (force brute).

Données

Entrée
Ligne 1 : un entier N compris entre 1 et 5 indiquant la taille de votre équipe.
Ligne 2 : une chaîne de N caractères donnant les types de vos chatons. Par exemple FEFP signifie 2 chatons de type feu, 1 de type eau et 1 de type plante.
Ligne 3 : un entier M compris entre 1 et 10 indiquant la taille de l'équipe de votre adversaire.
Ligne 4 : une chaîne de M caractères donnant les types des chatons de votre adversaire. Votre adversaire présentera ses chatons dans l'ordre indiqué par cette chaîne.

Sortie
Une ligne dont le premier caractère indique le meilleur résultat qu'on peut obtenir avec une bonne stratégie : - pour une défaite, = pour une égalité et + pour une victoire. Ce caractère est suivi de N autres décrivant un ordre permettant d'accomplir ce résultat.
Par exemple, vous pouvez renvoyer +PFEF s'il est possible de gagner en envoyant au combat d'abord un chaton plante, puis un chaton feu, puis un chaton eau et enfin un chaton feu (à condition, bien entendu, que votre équipe comporte à la base 1 P, 1 E et 2 F).




from collections import Counter
from itertools import permutations

WIN = 2
EXAEQUO = 1
LOSE = 0


def simulate_battle(t1, t2):
    if t1 == t2:
        return EXAEQUO
    if ((t1 == 'F' and t2 == 'E') or
        (t1 == 'E' and t2 == 'P') or
            (t1 == 'P' and t2 == 'F')):
        return LOSE
    return WIN


def simulate(team1, team2):
    team1 = team1.copy()
    team2 = team2.copy()

    while team1 and team2:
        result_battle = simulate_battle(team1[0], team2[0])
        if result_battle == EXAEQUO or result_battle == LOSE:
            team1.pop(0)
        if result_battle == EXAEQUO or result_battle == WIN:
            team2.pop(0)

    if not team1 and not team2:
        return EXAEQUO
    elif not team1:
        return LOSE
    return WIN


def solve(own, other):
    other = list(other)
    own = list(own)
    best = LOSE
    best_team = own
    for possible_team in permutations(own, len(own)):
        possible_team = list(possible_team)
        possible_result = simulate(possible_team, other)
        if possible_result > best:
            best = possible_result
            best_team = possible_team
        if best == WIN:
            break

    best_team = ''.join(best_team)

    if best == LOSE:
        status = "-"
    if best == EXAEQUO:
        status = "="
    if best == WIN:
        status = "+"
    return (status + best_team)

if __name__ == "__main__":
    N = input()
    own_team = input()
    M = input()
    other_team = input()
    print(solve(own_team, other_team))

