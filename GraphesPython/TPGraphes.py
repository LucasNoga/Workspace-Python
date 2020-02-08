#La librairie networkx peut être téléchargée à l'adresse http://networkx.lanl.gov/ 
#(choisir la version adaptée à la version de python que vous utilisez)
#Le fichier .egg obtenu doit être décompressé, par exemple avec sevenzip (http://www.7-zip.org/)
#et placé à un endroit où python va le trouver, par exemple dans le même répertoire que le programme
import networkx as nx








#Création du graphe exemple
G=nx.Graph()
G.add_nodes_from(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
                  "P"])
#print("Sommets du graphe G : ",G.nodes())
G.add_edges_from([("A","B"),("A","E"),("A","F"),("B","D"),("B","H"),("C","G"),
                  ("D","F"),("D","J"),("E","H"),("F","I"),("G","K"),("I","P"),
                  ("J","O"),("K","N"),("K","O"),("L","M"),("L","P"),("M","N"),
                  ("M","O"),("N","O")])
#print("Arêtes du graphe G : ",G.edges())










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
R=ParcoursLargeur(G,"O")
print("Sommets visités par la fonction ParcoursLargeur à partir du sommet O: ",R)


#La librairie networkx contient de nombreuses fonctions déjà programmées réalisant la plupart des
#algorithmes de graphes classiques. En particulier, la fonction utilisée ci-dessous calcule l'arbre
#de parcours en profondeur
N=nx.bfs_tree(G,"O")
print("Sommets visités par l'algorithme de parcours en largeur de la librairie networkx à partir du sommet O: ",N.nodes())
