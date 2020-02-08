##Finalement, la seule fonction de la librairie networkx dont on a eu besoin pour
##programmer les algorithmes de parcours est celle de calcul des voisins.
##Du coup, on peut se passer de cette librairie en bricolant soi-même une
##structure de données "graphe" et une fonction "voisins", comme ci-dessous.
##Le résultat est certainement moins optimisé que la librairie networkx, et
##surtout on doit programmer tout ce dont on a besoin...





#Création du graphe exemple
GNodes=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
                  "P"]
#print(GNodes)
GEdges=[["A","B"],["A","E"],["F","A"],["B","D"],["B","H"],["C","G"],
                  ["D","F"],["D","J"],["E","H"],["F","I"],["G","K"],["I","P"],
                  ["J","O"],["K","N"],["K","O"],["L","M"],["L","P"],["M","N"],
                  ["M","O"],["N","O"]]
#print(GEdges)
G=[GNodes,GEdges]
#On récupère les sommets du graphe G à l'indice 0
#print(G[0])
#On récupère les arêtes du graphe G à l'indice 1
#print(G[1])





#Récupérer la liste des voisins d'un sommet x dans un graphe H (non orienté)
def Voisins(H,x):
    L=[]
    for [a,b] in H[1]:
        if a==x:
            L.append(b)
        if b==x:
            L.append(a)
    return(L)

#print(Voisins(G,"A"))






#Parcours en profondeur avec calcul de l'arbre de parcours
def ParcoursProfondeur(H,x):
    # D'abord l'initialisation
    TNodes=[]
    TEdges=[]
    TNodes.append(x)
    P=[x]
    # Ensuite le parcours en profondeur proprement dit
    while not(P==[]):
        v=P[len(P)-1]
        L=[]
        for y in Voisins(H,v):
            if not(y in TNodes):
                L.append(y)
        if not(L==[]):
            u=L[0]
            TNodes.append(u)
            TEdges.append([v,u])
            P.append(u)
        else:
            P.pop()
    T=[TNodes,TEdges]
    return(T)

##A=ParcoursProfondeur(G,"E")
##print(A[0])
##print(A[1])
