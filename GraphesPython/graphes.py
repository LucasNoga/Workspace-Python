#La librairie networkx peut être téléchargée à l'adresse http://networkx.lanl.gov/ 
#(choisir la version adaptée à la version de python que vous utilisez)
#Le fichier .egg obtenu doit être décompressé, par exemple avec sevenzip (http://www.7-zip.org/)
#et placé à un endroit où python va le trouver, par exemple dans le même répertoire que le programme
import networkx as nx




#Création du graphe exemple
G=nx.Graph()
G.add_nodes_from(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
                  "P"])
#print(G.nodes())
G.add_edges_from([("A","B"),("A","E"),("A","F"),("B","D"),("B","H"),("C","G"),
                  ("D","F"),("D","J"),("E","H"),("F","I"),("G","K"),("I","P"),
                  ("J","O"),("K","N"),("K","O"),("L","M"),("L","P"),("M","N"),
                  ("M","O"),("N","O")])
#print(G.edges())









#Parcours en largeur
#H est le graphe à parcourir et x est le sommet de départ
def ParcoursLargeur(H,x):
    #D'abord l'initialisation
    #Sommets connus
    S=[x]
    #Frontière (file d'attente)
    F=[x]
    #Ensuite le parcours en largeur proprement dit
    while not(F==[]):
        #v est le premier élément de la file d'attente
        v=F[0]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(S))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u aux sommets connus
            S.append(u)
            #Ajouter u à la fin de la file d'attente
            F.append(u)
        else:
            #Supprimer v de la file d'attente
            F.remove(v)
    #Retourner les sommets connus
    return(S)


#Utilisation de la fonction ParcoursLargeur
##R=ParcoursLargeur(G,"O")
##print("Sommets visités par la fonction ParcoursLargeur à partir du sommet O : ",R)









#######################
##NOUVEAUTÉS CI-DESSOUS
#######################





#Parcours en largeur avec calcul de l'arbre de parcours
#H est le graphe à parcourir et x est le sommet de départ
def ArbreParcoursLargeur(H,x):
    # D'abord l'initialisation
    #L'arbre de parcours sera un graphe orienté
    T=nx.DiGraph()
    T.add_node(x)
    #Frontière (file d'attente)
    F=[x]
    #Ensuite le parcours en largeur proprement dit
    while not(F==[]):
        #v est le premier élément de la file d'attente
        v=F[0]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(T.nodes()))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u comme nouveau sommet de T et l'arête (v,u) comme nouvelle
            #arête de T
            T.add_node(u)
            T.add_edge(v,u)
            #Ajouter u à la fin de la file d'attente
            F.append(u)
        else:
            #Supprimer v de la file d'attente
            F.remove(v)
    #Retourner l'arbre de parcours
    return(T)




###Utilisation de la fonction ArbreParcoursLargeur
##A=ArbreParcoursLargeur(G,"E")
##print("Arêtes de l'arbre de parcours en largeur à partir du sommet E : ",A.edges())









#Parcours en largeur avec calcul des distances à la source
#H est le graphe à parcourir et x est le sommet de départ
def DistanceParcoursLargeur(H,x):
    # D'abord l'initialisation
    #Arbre de parcours
    T=nx.DiGraph()
    #La distance de x à x est 0
    T.add_node(x,distance=0)
    #Frontière (file d'attente)
    F=[x]
    #Ensuite le parcours en largeur proprement dit
    while not(F==[]):
        #v est le premier élément de la file d'attente
        v=F[0]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(T.nodes()))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u comme nouveau sommet de T et l'arête (v,u) comme nouvelle
            #arête de T
            #La distance de la source à u est égale à la distance de x à v +1
            T.add_node(u,distance=T.node[v]["distance"]+1)
            T.add_edge(v,u)
            #Ajouter u à la fin de la file d'attente
            F.append(u)
        else:
            #Supprimer v de la file d'attente
            F.remove(v)
    #Retourner l'arbre de parcours
    return(T)





###Utilisation de la fonction DistanceParcoursLargeur
##B=DistanceParcoursLargeur(G,"E")
##print("Distance entre E et les autres sommets du graphe : ",B.nodes(data=True))









#Parcours en profondeur
#H est le graphe à parcourir et x est le sommet de départ
def ParcoursLargeur(H,x):
    #D'abord l'initialisation
    #Sommets connus
    S=[x]
    #Frontière (pile d'attente)
    P=[x]
    #Ensuite le parcours en profondeur proprement dit
    while not(P==[]):
        #v est le premier élément de la pile d'attente
        v=P[len(P)-1]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(S))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u aux sommets connus
            S.append(u)
            #Ajouter u à la fin de la file d'attente
            P.append(u)
        else:
            #Supprimer v de la file d'attente
            P.remove(v)
    #Retourner les sommets connus
    return(S)


###Utilisation de la fonction ParcoursProfondeur
##R=ParcoursProfondeur(G,"O")
##print("Sommets visités par la fonction ParcoursProfondeur à partir du sommet O : ",R)






#Parcours en profondeur avec calcul de l'arbre de parcours
#H est le graphe à parcourir et x est le sommet de départ
def ArbreParcoursProfondeur(H,x):
    # D'abord l'initialisation
    #L'arbre de parcours sera un graphe orienté
    T=nx.DiGraph()
    T.add_node(x)
    #Frontière (pile d'attente)
    P=[x]
    #Ensuite le parcours en profondeur proprement dit
    while not(P==[]):
        #v est le premier élément de la pile d'attente
        v=P[len(P)-1]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(T.nodes()))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u comme nouveau sommet de T et l'arête (v,u) comme nouvelle
            #arête de T
            T.add_node(u)
            T.add_edge(v,u)
            #Ajouter u à la fin de la file d'attente
            P.append(u)
        else:
            #Supprimer v de la file d'attente
            P.remove(v)
    #Retourner l'arbre de parcours
    return(T)




###Utilisation de la fonction ArbreParcoursProfondeur
##A=ArbreParcoursProfondeur(G,"E")
##print("Arêtes de l'arbre de parcours en profondeur à partir du sommet E : ",A.edges())








#Parcours en profondeur avec calcul des instants de découverte et de cloture
#pour chaque sommet
#H est le graphe à parcourir et x est le sommet de départ
def InstantsParcoursProfondeur(H,x):
    # D'abord l'initialisation
    #L'arbre de parcours sera un graphe orienté
    T=nx.DiGraph()
    #la source est découverte à l'instant 0
    T.add_node(x,debut=0)
    #Frontière (pile d'attente)
    P=[x]
    #Ensuite le parcours en profondeur proprement dit
    #l'indice i sera incrémenté à chaque tour dans la boucle
    i=1
    while not(P==[]):
        #v est le premier élément de la pile d'attente
        v=P[len(P)-1]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(T.nodes()))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u comme nouveau sommet de T à l'instant i
            #et l'arête (v,u) comme nouvelle arête de T
            T.add_node(u,debut=i)
            T.add_edge(v,u)
            #Ajouter u à la fin de la file d'attente
            P.append(u)
        else:
            #On termine de traiter le sommet v à l'instant i
            T.node[v]["fin"]=i
            #Supprimer v de la file d'attente
            P.remove(v)
        #il reste à incrémenter i
        i=i+1
    #Retourner l'arbre de parcours
    return(T)




###Utilisation de la fonction InstantsParcoursProfondeur
##B=InstantsParcoursProfondeur(G,"E")
##print("Parcours en profondeur à partir du sommet E : ",B.nodes(data=True))













#Création du graphe orienté exemple avec ajout d'un sommet source artificiel
J=nx.DiGraph()
J.add_nodes_from(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
                  "P","S"])
#print(J.nodes())
J.add_edges_from([("A","B"),("A","E"),("A","F"),("B","D"),("B","H"),("C","G"),
                  ("D","F"),("D","J"),("E","H"),("F","I"),("G","K"),("I","P"),
                  ("J","O"),("K","N"),("K","O"),("L","M"),("L","P"),("M","N"),
                  ("M","O"),("N","O"),("S","A"),("S","B"),("S","C"),("S","D"),
                  ("S","E"),("S","F"),("S","G"),("S","H"),("S","I"),("S","J"),
                  ("S","K"),("S","L"),("S","M"),("S","N"),("S","O"),("S","P")])
#print(J.edges())










#Tri topologique version 1 : en utilisant la fonction InstantsParcoursProfondeur
#H est le graphe à parcourir et x est le sommet de départ
def TriTopoV1(H,x):
    #Calcul des instants de découverte et de cloture des sommets
    A=InstantsParcoursProfondeur(H,x)
    Result=[]
    for x in A.nodes():
        #Création d'une liste contenant les couples (instant de cloture, nom du
        #sommet
        Result.append([A.node[x]["fin"],x])
    #Tri de la liste selon le premier élément des couples
    Result.sort()
    #Retournement de la liste
    Result.reverse()
    L=[]
    for [a,b] in Result:
        #Création d'une liste composée des deuxièmes éléments des couples triés
        L.append(b)
    #On obtient les noms des sommets ordonnées selon un tri topologique
    return(L)





###Utilisation de la fonction TriTopoV1
##C=TriTopoV1(J,"S")
##print("Tri topologique version 1 à partir du sommet artificiel S : ",C)









#Tri topologique version 2 : en réécrivant le parcours en profondeur
#H est le graphe à parcourir et x est le sommet de départ
def TriTopoV2(H,x):
    # D'abord l'initialisation
    #Sommets connus
    S=[x]
    #Frontière (pile d'attente)
    P=[x]
    #Sommets terminés
    Fin=[]
    #Ensuite le parcours en profondeur proprement dit
    while not(P==[]):
        #v est le premier élément de la pile d'attente
        v=P[len(P)-1]
        #Chercher les voisins de v encore inconnus
        #J'ai utilisé la différence ensembliste, mais il y a bien sûr d'autres façons de le faire
        L=list(set(H.neighbors(v))-set(S))
        #Si v a des voisins encore inconnus, la liste L n'est pas vide
        if not(L==[]):
            #u est le premier voisin inconnu de v
            u=L[0]
            #Ajouter u comme nouveau sommet connu
            S.append(u)
            #Ajouter u à la fin de la file d'attente
            P.append(u)
        else:
            #On termine de traiter le sommet v 
            Fin.append(v)
            #Supprimer v de la file d'attente
            P.remove(v)
    #Renverser la liste Fin
    Fin.reverse()
    #Retourner la liste obtenue
    return(Fin)




###Utilisation de la fonction TriTopoV2
##C=TriTopoV2(J,"S")
##print("Tri topologique version 1 à partir du sommet artificiel S : ",C)










####################################################################
#COMPLÉMENT : le parcours en profondeur se prête naturellement à une
#implémentation récursive
####################################################################



#La fonction ParcoursRecursif effectue un parcours en profondeur récursif
#en calculant l'arbre de parcours et les instant de découverte et de
#cloture pour chaque sommet visité
#H est le graphe à parcourir, x est le sommet courant et A est l'arbre de
#parcours en profondeur
#Cette fonction ne renvoie aucun résultat, elle se contente de modifier l'arbre
#de parcours
def ParcoursRecursif(H,x,A):
    #l'indice i représente le nombre d'étapes, c'est une variable globale
    global i
    #On traite successivement chaque voisin de x
    for u in H.neighbors(x):
        if not(u in A.nodes()):
            #u est un voisin de x qui n'a pas encore été découvert : on le
            #traite maintenant
            i=i+1
            A.add_node(u,debut=i)
            A.add_edge(x,u)
            #L'appel récursif est ici : on va traiter les voisins de u
            ParcoursRecursif(H,u,A)
            #On a fini de traiter u et tous ses voisins : on peut cloturer u
            i=i+1
            A.node[u]["fin"]=i
            

#La fonction EncapsuleParcoursRecursif ne sert qu'à lancer la fonction
#ParcoursRecursif avec les bons paramètres
def EncapsuleParcoursRecursif(H,x):
    global i
    #initialisation de l'indice global i
    i=0
    #initialisation de l'arbre de parcours
    T=nx.DiGraph()
    T.add_node(x,début=i)
    #Appel de la fonction principale
    ParcoursRecursif(G,x,T)
    #À la sortie de la fonction principale, il ne reste plus qu'à cloturer
    #l'exploration du sommet initial
    i=i+1
    T.node[x]["fin"]=i
    #On retourne l'arbre de parcours
    return(T)




###Utilisation de la fonction EncapsulePArcoursRecursif
##D=EncapsuleParcoursRecursif(G,"O")
##print("Parcours en profondeur à partir du sommet O : ",D.nodes(data=True))
