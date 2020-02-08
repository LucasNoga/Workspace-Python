Enoncé
Dans ce challenge, on utilise un format de données qui est une version simplifiée du XML. Les noms des balises ne sont composés que d'une lettre minuscule, une balise ouvrante étant représentée par cette lettre seule et la balise fermante étant représentée par le caractère -, suivi de la lettre.

Par exemple, la chaîne ab-bcd-d-c-ae-e est l'équivalent de <a><b></b><c><d></d></c></a><e></e> en XML. La chaîne fournie sera toujours correctement formée.

On définit à présent la profondeur d'une balise comme 1 + le nombre de balises dans lesquelles elle est incluse.

Dans l'exemple précédent : a et e ont une profondeur de 1,
b et c ont une profondeur de 2
et d a une profondeur de 3.

On définit enfin le poids d'un nom de balise par la somme des inverses des profondeurs de chacune de ses occurrences.

Par exemple, dans la chaine a-abab-b-a-b, il y a : - deux balises a de profondeur 1 et 2
- deux balises b de profondeurs 1 et 3.
Le poids de a est donc de (1/1)+(1/2) = 1.5 et le poids de b est donc (1/1)+(1/3)=1.33.

Dans ce challenge vous devez déterminer la lettre correspondant à la balise de plus grand poids de la chaîne passée en paramètre.

Format des données

Entrée
Sur une seule ligne, une chaîne correctement formée d'au maximum 1024 caractères représentant une imbrication de balises.

Sortie
La lettre correspondant au nom de balise de plus grand poids. Si deux noms de balises ont le même poids, affichez le plus petit dans l'ordre alphabétique.


#**************Solution by Isograd ************************/
from collections import Counter

s = input()
n = len(s)
letters = []
c = Counter()
i = 0
while i < n:
    if s[i] == '-':
        i += 1
        letters.pop()
    else:
        letters.append(s[i])
        c[s[i]] += 1 / len(letters)
    i += 1
print(min((-v, k) for k, v in c.items())[1])