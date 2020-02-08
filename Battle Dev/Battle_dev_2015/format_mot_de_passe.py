Énoncé



Dans ce challenge vous devez vérifier si des mots de passe sont valides. Pour être valide, un mot de passe doit :- contenir 6 caractères

- être composé d'une lettre, d'un chiffre, puis de 4 lettres.

On entend par lettre un caractère non accentué minuscule ou majuscule compris entre a et z.



Format des données



Entrée

Ligne 1 : un entier N compris entre 1 et 2 000 indiquant le nombre de mots de passe à vérifier.

Lignes 2 à N+1 : une chaîne contenant au plus 10 caractères représentant un mot de passe.



Sortie

Un entier représentant le nombre de mots de passe valides.


#*****
# Solution de Naca
#**/

import sys

def getInput() :
	n = int(input())
	tab = []
	for i in range(n) :
		tab.append(input())

	return n, tab

def solve(mdp) :
	alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	chiffre = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	for v in range(10) :
		if mdp[1] == str(chiffre[v]) :
			if mdp[0] in alphabet and mdp[2] in alphabet and mdp[3] in alphabet and mdp[4] in alphabet and mdp[5] in alphabet :
				return True
	return False


(n, tab) = getInput()
compteur = 0
for i in range(n) :
	if len(tab[i]) == 6 :
		if solve(tab[i]) :
			compteur += 1
print(compteur)

