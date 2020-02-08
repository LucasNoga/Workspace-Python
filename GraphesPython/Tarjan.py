#La librairie networkx peut être téléchargée à l'adresse http://networkx.lanl.gov/ 
#(choisir la version adaptée à la version de python que vous utilisez)
#Le fichier .egg obtenu doit être décompressé, par exemple avec sevenzip (http://www.7-zip.org/)
#et placé à un endroit où python va le trouver, par exemple dans le même répertoire que le programme
import networkx as nx




#Création du graphe exemple
G=nx.DiGraph()
G.add_nodes_from(["A","B","C","D","E","F","G","H","I","J"])
#print(G.nodes())
G.add_edges_from([("A","B"),("A","J"),("B","A"),("B","C"),("C","D"),("C","F"),
                  ("C","G"),("D","C"),("E","D"),("F","E"),("F","G"),("G","E"),
                  ("H","C"),("H","I"),("I","J"),("J","H"),("J","I")])
#print(G.edges())











def Tarjan(H):
    #initialisation des instants de découverte
    for u in H.nodes():
        H.node[u]["decouverte"]=0
    #ensemble des sommets déjà visités
    S=[]
    #Pile pour le parcours
    Parcours=[]
    #Pile supplémentaire pour Tarjan
    Tarjan=[]
    #Compteur des instants de découverte
    count=0
    #La boucle extérieure peut-être utile si le sommet initial ne permet pas
    #d'atteindre tous les sommets
    for x in H.nodes():
        #s'il y a encore un sommet qui n'a pas été découvert
        if not x in S:
            #Initialisation du parcours proprement dit
            count=count+1
            S.append(x)
            #Instant de découverte de x
            H.node[x]["decouverte"]=count
            #Initialisation de l'index de x
            H.node[x]["index"]=count
            Parcours.append(x)
            #La pile Tarjan se remplit comme la pile Parcours
            Tarjan.append(x)
            while not(Parcours==[]):
                v=Parcours[len(Parcours)-1]
                L=list(set(H.successors(v))-set(S))
                #Pour tenir compte de notre convention de parcours dans l'ordre
                #alphabétique, on trie la liste des successeurs
                L.sort()
                if not(L==[]):
                    count=count+1
                    u=L[0]
                    S.append(u)
                    #Instant de découverte de u
                    H.node[u]["decouverte"]=count
                    #Initialisation de l'index de u
                    H.node[u]["index"]=count
                    Parcours.append(u)
                    #La pile Tarjan se remplit comme la pile Parcours
                    Tarjan.append(u)
                else:
                    #Si v n'a plus de voisins qui n'ont pas encore été visités,
                    #on s'occupe de la mise à jour des index au moment de
                    #supprimer v
                    for u in H.successors(v):
                        #Si (v,u) est un arc arrière
                        if (H.node[u]["index"]<H.node[v]["index"]) and (u in Parcours):
                            H.node[v]["index"]=H.node[u]["index"]
                    for u in H.successors(v):
                        #Si (v,u) est un arc transverse
                        if (H.node[u]["index"]<H.node[v]["index"]) and (u in Tarjan):
                            H.node[v]["index"]=H.node[u]["index"]
                    Parcours.remove(v)
                    if not Parcours==[]:
                        #Si u est le père de v
                        u=Parcours[len(Parcours)-1]
                        if H.node[v]["index"]<H.node[u]["index"]:
                            H.node[u]["index"]=H.node[v]["index"]
                    #Si on a trouvé l'entrée d'une composante fortement connexe
                    if H.node[v]["index"]==H.node[v]["decouverte"]:
                        #C'est ici qu'on dépile Tarjan
                        u=Tarjan[len(Tarjan)-1]
                        while not u==v:
                            Tarjan.remove(u)
                            u=Tarjan[len(Tarjan)-1]
                        Tarjan.remove(v)
    #Traitement pour récupérer les composantes fortement connexes
    comp={}
    for x in H.nodes():
        comp[H.node[x]["index"]]=[]
    for x in H.nodes():
        comp[H.node[x]["index"]].append(x)
    return(comp)



A=Tarjan(G)
print(A)
