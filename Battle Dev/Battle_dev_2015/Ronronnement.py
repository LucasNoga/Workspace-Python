Énoncé


Votre grand-mère est partie faire les courses, elle vous demande de surveiller son chat. Il n'est pas question de vous contenter de le caresser, il est bien plus intéressant d'étudier le signal de son ronronnement. Vous êtes parvenu à enregistrer le ronronnement du chat avec le microphone de votre ordinateur et à l'encoder sous la forme d'une séquence de valeurs comprises entre 0 et 9. À présent, vous aimeriez déterminer la plus petite période de ce signal, c'est-à-dire la longueur du plus petit motif tel que le signal soit une répétition de ce motif.

Par exemple, la plus petite période de 12121212 est 2 tandis que celle de 123123 est 3. En revanche, celle de 1231231 est 7 (car le motif 123 n'apparaît pas de façon complète à la fin de la séquence).

Format des données

Entrée
Ligne 1 : une série de chiffres (compris entre 0 et 9). La nombre de chiffres dans la série ne dépassera pas 1 000.

Sortie
Sur une ligne, un entier représentant la plus petite période du signal.




#********** solution by Isograd ******
signal = input()
#********** La solution tient en fait en une ligne ******
print((signal + signal).find(signal, 1))

