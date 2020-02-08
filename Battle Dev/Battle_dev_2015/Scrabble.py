Énoncé





Votre grand-mère vous invite à jouer au Scrabble.



Pour simplifier, on va considérer qu'au Scrabble un mot a pour valeur la somme des valeurs des lettres qui le composent. Vous souhaitez réaliser un outil qui vous aidera à jouer et qui calcule la valeur des mots contenus dans un dictionnaire.



Format des données



Entrée

Ligne 1 : un entier N compris entre 1 et 100 représentant le nombre de mots du dictionnaire.

Ligne 2 : 26 entiers séparés par des espaces représentant pour chaque lettre de A à Z le nombre de points qu'elle rapporte.

Lignes 3 à N + 2 : un mot en lettres capitales contenant au plus 7 lettres.



Sortie

Deux entiers S et L séparés par un espace. S représente le score maximal des mots contenus dans le dictionnaire. L représente la longueur du mot le plus court contenu dans le dictionnaire réalisant ce score maximal.


N = int(input())
values = list(map(int, input().split()))
words = []
for _ in range(N):
    words.append(input())
candidates = []
for word in words:
    score = 0
    for letter in word:
        score += values[ord(letter) - ord('A')]
    candidates.append((-score, len(word)))
candidates.sort()
mscore, length = candidates[0]
score = -mscore
print(score, length)