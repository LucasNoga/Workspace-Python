#La librairie networkx peut être téléchargée à l'adresse http://networkx.lanl.gov/ 
#(choisir la version adaptée à la version de python que vous utilisez)
#Le fichier .egg obtenu doit être décompressé, par exemple avec sevenzip (http://www.7-zip.org/)
#et placé à un endroit où python va le trouver, par exemple dans le même répertoire que le programme
import networkx as nx




#Création de l'arbre exemple
A=nx.DiGraph()
A.add_nodes_from(["A","B","C","D","E","F","G","H","I","J"])
A.node["A"]["etiq"]=6
A.node["B"]["etiq"]=1
A.node["C"]["etiq"]=7
A.node["D"]["etiq"]=2
A.node["E"]["etiq"]=6
A.node["F"]["etiq"]=3
A.node["G"]["etiq"]=5
A.node["H"]["etiq"]=8
A.node["I"]["etiq"]=3
A.node["J"]["etiq"]=6
#print(A.nodes(data=True))
A.add_edges_from([("A","B",{"fils":"gauche"}),("A","C",{"fils":"droit"}),
                  ("B","D",{"fils":"gauche"}),("B","E",{"fils":"droit"}),
                  ("C","F",{"fils":"gauche"}),("C","G",{"fils":"droit"}),
                  ("D","H",{"fils":"gauche"}),("D","I",{"fils":"droit"}),
                  ("F","J",{"fils":"droit"})])
#print(A.edges(data=True))



####################################
#Fonctions techniques : trouver la racine d'un arbre, trouver le fils gauche et
#le fils droit d'un noeud
######################################


#La racine de l'arbre est le seul noeud qui n'a pas de prédécesseur
def TrouveRacine(T):
    for x in T.nodes():
        if T.in_degree(x)==0:
            return(x)

#print(TrouveRacine(A))






def FilsGauche(T,x):
    for y in T.successors(x):
        if T.edge[x][y]["fils"]=="gauche":
            return(y)
    #Si on sort de la boucle sans avoir trouvé le fils gauche, c'est qu'il
    #n'existe pas : par convention, on renvoie "NULL"
    return("NULL")

#print(FilsGauche(A,"A"))
#print(FilsGauche(A,"J"))




def FilsDroit(T,x):
    for y in T.successors(x):
        if T.edge[x][y]["fils"]=="droit":
            return(y)
    #Si on sort de la boucle sans avoir trouvé le fils droit, c'est qu'il
    #n'existe pas : par convention, on renvoie "NULL"
    return("NULL")

#print(FilsDroit(A,"A"))
#print(FilsDroit(A,"J"))







################################
#Traitement à effectuer pendant le parcours
################################



#Le contenu de la fonction Traiter dépend du traitement à effectuer : ici, on
#veut seulement afficher l'étiquette du noeud
def Traiter(T,x):
    print(T.node[x]["etiq"])

#Traiter(A,"A")
#Traiter(A,"B")






#################################
#Les différents parcours d'arbres
#################################





#Parcours préfixe
def Prefixe(T,x):
  if not x=="NULL":
      Traiter(T,x)
      y=FilsGauche(T,x)
      z=FilsDroit(T,x)
      Prefixe(T,y)
      Prefixe(T,z)

#Prefixe(A,TrouveRacine(A))
        
    

#Parcours infixe
def Infixe(T,x):
  if not x=="NULL":
      y=FilsGauche(T,x)
      z=FilsDroit(T,x)
      Infixe(T,y)
      Traiter(T,x)
      Infixe(T,z)

#Infixe(A,TrouveRacine(A))



#Parcours postfixe
def Postfixe(T,x):
  if not x=="NULL":
      y=FilsGauche(T,x)
      z=FilsDroit(T,x)
      Postfixe(T,y)
      Postfixe(T,z)
      Traiter(T,x)

#Postfixe(A,TrouveRacine(A))





#Parcours en largeur : pas de récursivité, mais utilisation d'une file d'attente
def Largeur(T,x):
    file=[x]
    while not file==[]:
        y=file[0]
        Traiter(T,y)
        z=FilsGauche(T,y)
        if not z=="NULL":
            file.append(z)
        z=FilsDroit(T,y)
        if not z=="NULL":
            file.append(z)
        file.remove(y)

#Largeur(A,TrouveRacine(A))
        
