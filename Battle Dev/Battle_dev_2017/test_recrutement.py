# coding=utf-8

Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/recruitmenttest2.pdf

Objectif

Une société de recrutement décide d'utiliser un test en ligne pour évaluer des candidats. Le test fournit une note entre 0 et 20.
Les recruteurs considèrent que si le candidat obtient au moins la moyenne, ils l'embauchent.

Données

Entrée
Ligne 1 : un entier N compris entre 0 et 20 représentant la note obtenue au test.

Sortie
La chaîne JOB si le candidat a une note supérieure ou égale à 10. La chaîne ECHEC sinon.

#Solution by Isograd
N = int(input())
if (N>=10):
    print ("JOB")
else:
    print ("ECHEC")

