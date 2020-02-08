# Énoncé
#
# Vous décidez de faire une petite pause dans votre carrière de développeur et de vous reconvertir dans l'installation de pylônes. Votre premier boulot consiste à installer des pylônes le long d'une vallée.
#
# Soucieux du paysage, vous vous demandez depuis chaque pylône combien de pylônes sont visibles. Pour simplifier, un pylône A voit un pylône B s'il n'existe pas de pylône plus grand ou de la même taille que le pylône B entre le pylône A et le pylône B.
#
# Exemple
#
# Sur cette figure, les pylônes visibles depuis le 2e ont été indiqués en traits solides. Il y en a 4.
# La réponse à cette entrée devra être, répartis sur 7 lignes, les entiers 3 4 5 5 6 3 2.
#
#
# Format des données
#
# Entrée
# Ligne 1 : un entier N compris entre 1 et 1000, indiquant le nombre de pylônes le long de la vallée.
# Lignes 2 à N+1 : la hauteur d'un pylône, un entier compris entre 1 et 100.
#
# Sortie
# N entiers séparés par des espaces représentant le nombre de pylônes visibles depuis chaque pylône.

lines = open("/home/admin/Documents/trainBattleDev/ex4/input1.txt", "r").read()

data = [int(x) for x in lines.split()]
print(data)


def prev_list(i):
    index = i
    list1 = []
    while index > 0:
        index -= 1
        list1.append(data[index])
    return list1


def for_list(i):
    index = i
    list1 = []
    while index < len(data) - 1:
        index += 1
        list1.append(data[index])
    return list1


listPrev = []
listFor = []

for i in range(0, len(data)):
    listPrev.append(prev_list(i))
    listFor.append(for_list(i))

print(listPrev)
print(listFor)


def pyloneCounter(listTest, i):
    count = 0
    for elem in listTest:
        if elem < i:
            count += 1
        else:
            break
    return count


countBack = []
for i, listInterne in enumerate(listPrev):
    countBack.append(pyloneCounter(listInterne, data[i]))
print(countBack)

countForward = []
for i, listInterne in enumerate(listFor):
    countForward.append(pyloneCounter(listInterne, data[i]))
print(countForward)

finalCount = [countBack[x] + countForward[x] for x in range(0, len(countForward))]
print(finalCount)
