#La librairie networkx peut être téléchargée à l'adresse http=//networkx.lanl.gov/ 
#(choisir la version adaptée à la version de python que vous utilisez)
#Le fichier .egg obtenu doit être décompressé, par exemple avec sevenzip (http=//www.7-zip.org/)
#et placé à un endroit où python va le trouver, par exemple dans le même répertoire que le programme
import networkx as nx




#Création du graphe exemple
#C'est un graphe valué : chaque arête possède un poids (positif)
G=nx.Graph()
G.add_nodes_from(["A","B","C","D","E","F","G","H","I"])
#print(G.nodes())
G.add_weighted_edges_from([("A","B",2),("A","C",1),("B","C",2),
                  ("B","D",1),("B","G",3),("C","E",5),
                  ("D","E",3),("D","F",3),("E","F",1),
                  ("F","G",4),("F","H",1),("F","I",3),
                  ("G","H",5),("H","I",2)])
#print(G.edges(data=True))







#Je ne garantis pas que c'est un code optimal
def Dijkstra(H,x):
    #Initialisation
    #Pour remplacer +infini, je prends la somme des poids des arêtes + 1...
    max=0
    for (a,b) in H.edges():
        max=max+H[a][b]["weight"]
    max=max+1
    #Création du dictionnaire des distances
    distance={}
    for y in H.nodes():
        distance[y]=max
    distance[x]=0
    #Créer la liste des sommets marqués
    marque=[x]
    #Pour entrer au moins une fois dans la boucle
    test=True
    #Début de l'algorithme proprement dit:
    #Tant qu'il y a des sommets non marqués
    while test:
        #Calcul de la liste des arêtes reliant un sommet marqué et un sommet
        #non marqué
        L=[]
        for (a,b) in H.edges():
            if (a in marque) and (not b in marque):
                L.append([a,b])
            else:
                if (not a in marque) and (b in marque):
                    L.append([b,a])
        #Mise à jour des distances
        for [a,b] in L:
            w=distance[a]+H[a][b]["weight"]
            if w<distance[b]:
                distance[b]=w
        #Calcul de la liste des sommets non marqués
        L=list(set(H.nodes())-set(marque))
        #On marque un sommet de distance la plus faible
        s=L[0]
        for y in L:
            if distance[y]<distance[s]:
                s=y
        marque.append(s)
        L.remove(s)
        #On teste s'il reste des sommets à marquer
        if L==[]:
            test=False
    #On renvoie le dictionnaire des distances
    return(distance)




result=Dijkstra(G,"A")
print(result)


