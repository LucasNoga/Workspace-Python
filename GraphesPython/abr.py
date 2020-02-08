#La librairie networkx peut être téléchargée à l'adresse http://networkx.lanl.gov/ 
#(choisir la version adaptée à la version de python que vous utilisez)
#Le fichier .egg obtenu doit être décompressé, par exemple avec sevenzip (http://www.7-zip.org/)
#et placé à un endroit où python va le trouver, par exemple dans le même répertoire que le programme
import networkx as nx




#Création de l'ABR exemple
A=nx.DiGraph()
A.add_nodes_from([2,3,4,6,7,9,13,15,17,18,20])
#print(A.nodes())
A.add_edges_from([(15,6,{"fils":"gauche"}),(15,18,{"fils":"droit"}),
                  (6,3,{"fils":"gauche"}),(6,7,{"fils":"droit"}),
                  (18,17,{"fils":"gauche"}),(18,20,{"fils":"droit"}),
                  (3,2,{"fils":"gauche"}),(3,4,{"fils":"droit"}),
                  (7,13,{"fils":"droit"}),
                  (13,9,{"fils":"gauche"}),])
#print(A.edges(data=True))


#Pour vérifier que le cas particulier d'un arbre vide est bien traité
B=nx.DiGraph()


#Pour vérifier que le cas particulier d'un arbre réduit à sa racine est bien
#traité
C=nx.DiGraph()
C.add_node(6)


####################################
#Fonctions techniques : trouver la racine d'un arbre, trouver le fils gauche et
#le fils droit d'un noeud
#(ce sont les mêmes que pour un arbre binaire quelconque)
######################################


#La racine de l'arbre est le seul noeud qui n'a pas de prédécesseur
def TrouveRacine(T):
    for x in T.nodes():
        if T.in_degree(x)==0:
            return(x)
    #Si l'arbre n'a pas de racine, c'est qu'il est vide : par convention, on
    #renvoie "NULL"
    return("NULL")

#print(TrouveRacine(A))
#print(TrouveRacine(B))
#print(TrouveRacine(C))




def FilsGauche(T,x):
    if x in T.nodes():
        for y in T.successors(x):
            if T.edge[x][y]["fils"]=="gauche":
                return(y)
        #Si on sort de la boucle sans avoir trouvé le fils gauche, c'est qu'il
        #n'existe pas : par convention, on renvoie "NULL"
    return("NULL")

#print(FilsGauche(A,15))
#print(FilsGauche(A,7))
#print(FilsGauche(B,7))
#print(FilsGauche(C,7))
#print(FilsGauche(C,6))




def FilsDroit(T,x):
    if x in T.nodes():
        for y in T.successors(x):
            if T.edge[x][y]["fils"]=="droit":
                return(y)
    #Si on sort de la boucle sans avoir trouvé le fils droit, c'est qu'il
    #n'existe pas : par convention, on renvoie "NULL"
    return("NULL")

#print(FilsDroit(A,15))
#print(FilsDroit(A,13))
#print(FilsDroit(B,13))
#print(FilsDroit(C,13))
#print(FilsDroit(C,6))




def Pere(T,x):
    if x in T.nodes():
        y=T.predecessors(x)
        if not y==[]:
            return(y[0])
    return("NULL")

#print(Pere(A,13))
#print(Pere(A,15))
#print(Pere(B,15))
#print(Pere(C,15))
#print(Pere(C,6))




################################
#Traitement à effectuer pendant le parcours
################################



#Le contenu de la fonction Traiter dépend du traitement à effectuer : ici, on
#veut seulement afficher l'étiquette du noeud
def Traiter(T,x):
    print(x)

#Traiter(A,15)
#Traiter(A,7)
#Traiter(A,8)
#Traiter(B,8)
#Traiter(C,8)
#Traiter(C,6)






######################################
#Algorithmes ABR
######################################




#Recherche d'une valeur dans un ABR
def Rech(x,T,rac):
    if x==rac or rac=="NULL":
        Traiter(T,rac)
    else:
        if x<rac:
            y=FilsGauche(T,rac)
            Rech(x,T,y)
        else:
            y=FilsDroit(T,rac)
            Rech(x,T,y)


#Rech(13,A,TrouveRacine(A))
#Rech(8,A,TrouveRacine(A))
#Rech(8,B,TrouveRacine(B))
#Rech(8,C,TrouveRacine(C))
#Rech(6,C,TrouveRacine(C))




#Recherche du minimum d'un ABR
#Cette fonction retourne une valeur pour pouvoir être réutilisée dans la
#fonction Delete
def Min(T,rac):
    y=FilsGauche(T,rac)
    if y=="NULL":
        res=rac
    else:
        res=Min(T,y)
    return(res)

#print(Min(A,TrouveRacine(A)))
#print(Min(B,TrouveRacine(B)))
#print(Min(C,TrouveRacine(C)))



#Recherche du maximum d'un ABR
def Max(T,rac):
    y=FilsDroit(T,rac)
    if y=="NULL":
        Traiter(T,rac)
    else:
        Max(T,y)

#Max(A,TrouveRacine(A))
#Max(B,TrouveRacine(B))
#Max(C,TrouveRacine(C))





#Parcours infixe (d'un arbre binaire quelconque)
def Infixe(T,x):
  if not x=="NULL":
      y=FilsGauche(T,x)
      z=FilsDroit(T,x)
      Infixe(T,y)
      Traiter(T,x)
      Infixe(T,z)

#Infixe(A,TrouveRacine(A))
#Infixe(B,TrouveRacine(B))
#Infixe(C,TrouveRacine(C))




#Recherche du successeur d'un noeud dans un ABR
#Cette fonction retourne une valeur pour pouvoir être réutilisée dans la
#fonction Delete
def Succ(x,T):
    y=FilsDroit(T,x)
    if not y=="NULL":
        res=Min(T,y)
    else:
        z=Pere(T,x)
        t=FilsDroit(T,z)
        while ((not z=="NULL") and (x==t)):
            x=z
            z=Pere(T,x)
            if not z=="NULL":
                t=FilsDroit(T,z)
        res=z
    return(res)


#print(Succ(15,A))
#print(Succ(13,A))
#print(Succ(20,A))
#print(Succ(8,A))
#print(Succ(8,B))
#print(Succ(8,C))
#print(Succ(6,C))




#Recherche du prédécesseur d'un noeud dans un ABR
def Pred(x,T):
    y=FilsGauche(T,x)
    if not y=="NULL":
        Max(T,y)
    else:
        z=Pere(T,x)
        t=FilsGauche(T,z)
        while ((not z=="NULL") and (x==t)):
            x=z
            z=Pere(T,x)
            if not z=="NULL":
                t=FilsGauche(T,z)
        Traiter(T,z)

#Pred(15,A)
#Pred(7,A)
#Pred(2,A)
#Pred(15,B)
#Pred(15,C)
#Pred(6,C)





#Insertion d'un noeud dans un ABR
def Insert(x,T,y,z):
    if y=="NULL":
        if z=="NULL":
            T.add_node(x)
        else:
            if x<z:
                T.add_node(x)
                T.add_edge(z,x,{"fils":"gauche"})
            else:
                if x>z:
                    T.add_node(x)
                    T.add_edge(z,x,{"fils":"droit"})
    else:
        if x<y:
            t=FilsGauche(T,y)
            Insert(x,T,t,y)
        else:
            if x>y:
                t=FilsDroit(T,y)
                Insert(x,T,t,y)


#Insert(16,A,TrouveRacine(A),"NULL")
#Insert(16,A,TrouveRacine(A),"NULL")
#print(A.nodes())
#print(A.edges(data=True))
#Insert(16,B,TrouveRacine(B),"NULL")
#print(B.nodes())
#print(B.edges(data=True))
#Insert(16,C,TrouveRacine(C),"NULL")
#print(C.nodes())
#print(C.edges(data=True))




#Construction d'un ABR à partir d'une liste de valeurs
def Build(L):
    T=nx.DiGraph()
    y="NULL"
    z="NULL"
    for x in L:
        Insert(x,T,y,z)
        y=TrouveRacine(T)
        z="NULL"
    return(T)


#D=Build([2, 3, 4, 6, 7, 9, 13, 15, 17, 18, 20])
#print(D.nodes())
#print(D.edges(data=True))
#print(TrouveRacine(D))







#Suppression d'une valeur dans un ABR : plus difficile...
def Delete(x,T):
    if x in T.nodes():
        fg=FilsGauche(T,x)
        fd=FilsDroit(T,x)
        p=Pere(T,x)
        u=FilsGauche(T,p)
        #Si x n'a pas de fils gauche, c'est facile
        if fg=="NULL":
            T.remove_node(x)
            if (not fd=="NULL") and (not p=="NULL"):
                #Si x est un fils gauche
                if x==u:
                    T.add_edge(p,fd,{"fils":"gauche"})
                else:
                    T.add_edge(p,fd,{"fils":"droit"})
        else:
            #Ou bien si x a un fils gauche mais pas de fils droit, c'est facile
            if fd=="NULL":
                T.remove_node(x)
                if not p=="NULL":
                    #Si x est un fils gauche
                    if x==u:
                        T.add_edge(p,fg,{"fils":"gauche"})
                    else:
                        T.add_edge(p,fg,{"fils":"droit"})
            else:
                #Si x a un fils gauche et un fils droit, ça se complique
                #On fait intervenir le successeur de x, qui n'a pas de fils
                #gauche (on peut le démontrer)
                suc=Succ(x,T)
                fdsuc=FilsDroit(T,suc)
                psuc=Pere(T,suc)
                v=FilsGauche(T,psuc)
                T.remove_node(suc)
                #On relie le père du successeur de x au fils (droit) du
                #successeur de x
                if (not fdsuc=="NULL") and (not psuc=="NULL"):
                    #Si le successeur de x est un fils gauche
                    if suc==v:
                        T.add_edge(psuc,fdsuc,{"fils":"gauche"})
                    else:
                        T.add_edge(psuc,fdsuc,{"fils":"droit"})
                #On remplace x par son successeur
                #Une subtilité ici : x peut être le père de son successeur, donc
                #après l'étape ci-dessus, le fils droit de x peut avoir changé,
                #c'est pourquoi on le recalcule
                fd=FilsDroit(T,x)
                T.remove_node(x)
                T.add_node(suc)
                T.add_edge(suc,fg,{"fils":"gauche"})
                T.add_edge(suc,fd,{"fils":"droit"})
                if not p=="NULL":
                    #Si x est un fils gauche
                    if x==u:
                        T.add_edge(p,suc,{"fils":"gauche"})
                    else:
                        T.add_edge(p,suc,{"fils":"droit"})



#Delete(4,A)
#Delete(13,A)
#Delete(7,A)
#Delete(6,A)
#Delete(15,A)
#print(A.nodes())
#print(A.edges(data=True))
