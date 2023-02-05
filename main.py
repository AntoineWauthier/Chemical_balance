import random
import time
import numpy as np
import math as m
import matplotlib.pyplot as plt
import itertools

ListeTest='CO2(CH4)3'
ETest=[]
Reac=['CH4','O2']
Prod=['CO2','H2O']
ChargesPresentes=[['+',0],['+',0]]

def decompositionEspece(Espece,Coefficient,ElementsPresents,ChargesPresentes,Text=False):
    n=len(Espece)
    k=0
    while k<n:
        if n==1:
            Element=Espece
            ajoutListeElement(Element,ElementsPresents,Coefficient)
            k+=1
        else:
            if k<n and Espece[k]=="(":
                indicateurParenthese=1
                longueurComplexe=1
                Quantite=1
                lq=0
                k+=1
                while k<n and indicateurParenthese!=0:
                    if Espece[k]=="(":
                        indicateurParenthese+=1
                        longueurComplexe+=1
                        k+=1
                    if Espece[k]==")":
                        indicateurParenthese-=1
                        longueurComplexe+=1
                        k+=1
                    else:
                        longueurComplexe+=1
                        k+=1
                if k<n and Espece[k].isdigit():
                    Quantite=Espece[k]
                    k+=1
                    lq+=1
                    while k<n and Espece[k].isdigit():
                        Quantite+=Espece[k]
                        k+=1
                        lq+=1
                decompositionEspece(Espece[1:k-lq-1],Coefficient*int(Quantite),ElementsPresents,ChargesPresentes)
                decompositionEspece(Espece[k:],Coefficient*int(Quantite),ElementsPresents,ChargesPresentes)
                n-=k
                k=0
                if Text==True:
                    print(Espece)
            elif k<n and Espece[k].isupper():
                Element=Espece[k]
                Quantite=1
                k+=1
                while k<n and Espece[k].islower():
                    Element+=Espece[k]
                    k+=1
                if k<n and Espece[k].isdigit():
                    Quantite=str(Espece[k])
                    k+=1
                    while k<n and Espece[k].isdigit():
                        Quantite+=str(Espece[k])
                        k+=1
                    ajoutListeElement(Element,ElementsPresents,Coefficient*int(Quantite))
                else:
                    ajoutListeElement(Element,ElementsPresents,Coefficient*int(Quantite))
                Espece=Espece[k:]
                n-=k
                k=0
                if Text==True:
                    print(Espece)
            elif k<n and Espece[k]=="=":
                k+=1
                Espece=Espece[k:]
                n-=k
                k=0
                if Text==True:
                    print(Espece)
            elif k<n and Espece[k]=="^":
                k+=1
                QuantiteCharge=1
                if k<n and Espece[k].isdigit():
                    QuantiteCharge=str(Espece[k])
                    k+=1
                    while k<n and Espece[k].isdigit():
                        QuantiteCharge+=str(Espece[k])
                        k+=1
                    ajoutListeElement(Espece[k+1],ChargesPresentes,Coefficient*int(QuantiteCharge))
                else:
                    ajoutListeElement(Espece[k+1],ChargesPresentes,Coefficient*int(QuantiteCharge))
                Espece=Espece[k+1:]
                n-=k+1
                k=0

def afficherEspece(Espece,Coeff): #fonction purement esthétique pour eviter d'afficher les coefficients lorsque ce sont des 1
    if Coeff==0:
        Affichage = None
    if Coeff==1:
        Affichage = Espece #si c'est un on ne l'affiche pas
    else:
        Affichage=str(Coeff)+" "+Espece
    return Affichage #sinon on l'affiche

def checkingColineaire(A,B): #fonction permettant de verifier si deux vecteurs sont colineaires
    nA=len(A)
    nB=len(B)
    assert(nA==nB)      #verifier si on travaille bien avec deux vecteurs de même dimension
    K = A[0]/B[0]      #coefficient de proportionalité entre les premieres composantes
    k=0
    while k<nA and A[k]/B[k]==K: #tant que chaque couple de composantes respecte bien ce même coefficient de proportionalité
        k+=1
    if k==nA:           #on est allé au bout des composantes donc elles sont toutes proportionnelles au même coeff
        return(True)      #donc ils sont colinéaires
    else:          #au moins un n'est pas proportionnel
        return(False) #ils ne sont pas colinéaires

def checkingDoublon(A,L): #verifie si un vecteur A est colineaire à un des vecteurs d'une liste L
    nA=len(A)
    nL=len(L)
    i=0
    while i<nL and checkingColineaire(A,L[i])==False: #tant qu'aucun vecteur de la liste n'est colinéaire à A on poursuit la recherche
        i+=1
    if i==nL:        #on est arrivé au bout de la liste
        return(False)  #donc aucun n'est colinéaire, A n'est donc pas un "doublon"
    else:            #on a trouvé un vecteur colinéaire à A
        return(True)   # A est donc un "doublon"

def combinaisons(l,p): #creer toutes les combinaisons possibles d'element de l et de longueur p
    n=len(l)
    composantes=[]
    nb = n**p
    for k in range(1,p+1):
        aux=[]
        for u in range(n):
            aux += (  (n**(p-k))*[l[u]]  )          #c'est un kdo de romain, la flemme de comprendre, faut que je l'adapte de toute façon
        aux=(n**(k-1))*aux
        composantes.append(aux)
    aux_f=[]
    for k in range(nb):
        aux2 = []
        for i in range(p):
            aux2.append(composantes[i][k])
        aux_f.append(aux2)
    return(aux_f)

def ajoutListeElement(Element,ElementsPresents,Quantite): #ajouter un element dans la liste d'elements, soit en updatant une quantité si il y'est déjà, soit en le rajoutant si il n'y est pas
        in_Elements=False          #on considere de base que l'element n'est pas dans notre liste
        for E in ElementsPresents:  #on teste chaque element déjà dans la liste
            if Element==E[0]:      #si le nom est reconnu pour un element de la liste
                in_Elements=True   #alors l'element est dans la liste
                E[1]+=int(Quantite) #on update la quantité déjà présente en y ajoutant la quantité algébrique
        if in_Elements==False: #si au bout du compte il n'est pas dans la liste
            ElementsPresents.append([Element,int(Quantite)]) #on l'ajoute à la liste et avec sa quantité algébrique

def checkingEquilibre(ListeReactifs,ListeProduits,CoefficientsStoechiometriques): #vérifier si une combinaison de coefficients, munies d'une liste de réactifs et de produits permet d'obtenir une équation équilibrée
    ChargesPresentes=[["+",0],["-",0]]
    ElementsPresents=[]  #initialiser la liste d'élément présent
    nCoeff=0  #initialiser l'indice du coefficient dans la liste de coefficients
    for Reactif in ListeReactifs:
        Statut='Reactif'
        Coeff = CoefficientsStoechiometriques[nCoeff] #on prend le coefficient qui correspond
        decompositionEspece(Reactif,-Coeff,ElementsPresents,ChargesPresentes) #on décompose le réactif
        nCoeff+=1 #on passe au coefficient suivant, pour le prochain réactif
    for Produit in ListeProduits:  #idem pour les produits en changeant le statut
        Statut='Produit'
        Coeff = CoefficientsStoechiometriques[nCoeff]
        decompositionEspece(Produit,Coeff,ElementsPresents,ChargesPresentes)
        nCoeff+=1
    Equilibre=True #on initialise l'équilibre comme vérifié de base
    for E in ElementsPresents: #pour chaque élément de la liste des éléments présents
        if E[1]!=0: #on verifie si la quantité finale est nulle (ça voudrait dire que la quantité de produits est égale à la quantité de réactifs
            Equilibre=False #si pour l'un ça n'est pas le cas, alors l'équilibre est rompu
    return(Equilibre) #si l'equilibre n'a pas été rompu cela renverra True, sinon ce sera False

#def affichageEspece

def rechercheCoefficientsEquilibre(ListeReactifs,ListeProduits,limite=10): #recherche la ou les manière(s) d'équilibrer une réaction avec certains réactifs et certains produits avec des coefficients inferieurs ou égaux à la limite choisie (10 par défaut)
    T=time.time() #inutile, juste pour me donner le temps exact d'execution
    nReact=len(ListeReactifs) #quantité de réactifs différents
    nProd=len(ListeProduits) #quantité de produits différents
    ListeCoefficientsEquilibres=[] #on initialise la liste de combinaisons de coefficients qui fonctionnent
    Possibilites=list(combinaisons(range(1,limite+1), nReact+nProd)) #on crée la liste de toutes les combinaisons possibles de coefficients de maximum la limite choisie et de taille correspondante à la quantité de coefficients nécessaire
    for CoefficientsStoechiometriques in Possibilites: #on teste chaque combinaison créée
        if checkingEquilibre(ListeReactifs,ListeProduits,CoefficientsStoechiometriques)==True and checkingDoublon(CoefficientsStoechiometriques,ListeCoefficientsEquilibres)==False: #elle est bonne si l'equilibre est respecté et que la combinaison trouvée n'est pas juste un multiple d'un combinaison déjà trouvée
            ListeCoefficientsEquilibres.append(CoefficientsStoechiometriques) #elle est bonne donc on l'a garde
            EquationReaction="" #on va l'afficher écrite avec le formalisme habituel
            for a in range(0,nReact): #pour chaque réactif
                EquationReaction+=afficherCoefficient(CoefficientsStoechiometriques[a]) #on affiche le coefficient
                EquationReaction+=" " #espace
                EquationReaction+=str(ListeReactifs[a]) #le nom de l'élément
                if a!=nReact-1: # tant que ça n'est pas le dernier réactif
                    EquationReaction+=" " #espace
                    EquationReaction+="+" #signe plus
                    EquationReaction+=" " #espace
                else: #sinon c'était le dernier
                    EquationReaction+=" " #espace
                    EquationReaction+="=" #égal
                    EquationReaction+=" " #espace
            for b in range(0,nProd): #idem pour les produits
                EquationReaction+=afficherCoefficient(CoefficientsStoechiometriques[b+nReact])
                EquationReaction+=" "
                EquationReaction+=str(ListeProduits[b])
                if b!=nProd-1:
                    EquationReaction+=" "
                    EquationReaction+="+"
                    EquationReaction+=" "
            print(EquationReaction) #on affiche l'équation qu'on vient d'écrire
    print(time.time()-T) #on affiche le temps final d'execution
    return(ListeCoefficientsEquilibres) #on renvoie toutes les combinaisons de coefficients qui fonctionnent
