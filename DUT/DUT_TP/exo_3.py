# coding=utf-8

"""l'attaque des titans"""

import random

titan1_name = ""
titan1_hp = 250


titan2_name = ""
titan2_hp = 250

random_attack = True
random_damage = 0

titan1_name = input("Joueur 1, choississez un pseudo: ")
print(f"{titan1_name} est le Joueur 1")
titan2_name = input("Joueur 2, choississez un pseudo: ")
print(f"{titan2_name} est le Joueur 2")

print("\nLE COMBAT COMMENCE !\n")

#-----------------------------------------------------------------------------
# Attaque 1

input() # permet de faire attendre le prochain tour
print(f"{titan1_name} A vous de commencer")
print(f"{titan1_name} : {titan1_hp} PV / {titan2_name} : {titan2_hp} PV")
random_attack = bool(random.randint(0, 1))

if random_attack == True:
    random_damage = random.randint(0, 100)
    print(f"{titan2_name} subit une attaque de {titan1_name} qui lui inflige {random_damage} points de degats")
    titan2_hp -= random_damage
else:
    print(f"{titan1_name} rate son attaque")

#-----------------------------------------------------------------------------
# Attaque 2

input() # permet de faire attendre le prochain tour
print(f"{titan2_name} A vous de commencer")
print(f"{titan1_name} : {titan1_hp} PV / {titan2_name} : {titan2_hp} PV")
random_attack = bool(random.randint(0, 1))

if random_attack == True:
    random_damage = random.randint(0, 100)
    print(f"{titan1_name} subit une attaque de {titan2_name} qui lui inflige {random_damage} points de degats")
    titan2_hp -= random_damage
else:
    print(f"{titan2_name} rate son attaque")

#-----------------------------------------------------------------------------
# Attaque 3

input() # permet de faire attendre le prochain tour
print(f"{titan1_name} A vous de commencer")
print(f"{titan1_name} : {titan1_hp} PV / {titan2_name} : {titan2_hp} PV")
random_attack = bool(random.randint(0, 1))

if random_attack == True:
    random_damage = random.randint(0, 100)
    print(f"{titan2_name} subit une attaque de {titan1_name} qui lui inflige {random_damage} points de degats")
    titan2_hp -= random_damage
else:
    print(f"{titan1_name} rate son attaque")

#-----------------------------------------------------------------------------
# Attaque 4

input() # permet de faire attendre le prochain tour
print(f"{titan2_name} A vous de commencer")
print(f"{titan1_name} : {titan1_hp} PV / {titan2_name} : {titan2_hp} PV")
random_attack = bool(random.randint(0, 1))

if random_attack == True:
    random_damage = random.randint(0, 100)
    print(f"{titan1_name} subit une attaque de {titan2_name} qui lui inflige {random_damage} points de degats")
    titan2_hp -= random_damage
else:
    print(f"{titan2_name} rate son attaque")

#-----------------------------------------------------------------------------
# Résultat final

input()
print("\nFIN DU COMBAT !\n")
print(f"{titan1_name} : {titan1_hp} PV / {titan2_name} : {titan2_hp} PV")

if(titan1_hp > titan2_hp):
    print(f"{titan1_name} remporte la victoire")

elif(titan1_hp < titan2_hp):
    print(f"{titan2_name} remporte la victoire")

else:
    print("Match nul")