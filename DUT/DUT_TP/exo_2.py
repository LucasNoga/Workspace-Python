# coding=utf-8

"""terminal de commande"""

import time

terminal_launched = True
terminal_name = "Defaut"
user_command = ""
while terminal_launched:
    user_command =  input("[{}]> ".format(terminal_name))
    if(user_command == "run"):
        for i in range(0,5):
            print(".")
            time.sleep(1)
    elif(user_command == "name"):
        terminal_name = input("Choisir un nouveau nom : ")
    elif(user_command == "help"):
        print("""
----------------------------------
LISTE DES COMMANDES DISPONIBLES
----------------------------------
run : Execute la boucle
name : modifier le nom du terminal
help : affiche la liste des commandes
quit : quitte le terminal
""")

    elif(user_command == "quit"):
        terminal_launched = False
    else:
       print("commande introuvable...")

