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

def afficherEspece(Espece,Coeff): #fonction purement esth??tique pour eviter d'afficher les coefficients lorsque ce sont des 1
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
    assert(nA==nB)      #verifier si on travaille bien avec deux vecteurs de m??me dimension
    K = A[0]/B[0]      #coefficient de proportionalit?? entre les premieres composantes
    k=0
    while k<nA and A[k]/B[k]==K: #tant que chaque couple de composantes respecte bien ce m??me coefficient de proportionalit??
        k+=1
    if k==nA:           #on est all?? au bout des composantes donc elles sont toutes proportionnelles au m??me coeff
        return(True)      #donc ils sont colin??aires
    else:          #au moins un n'est pas proportionnel
        return(False) #ils ne sont pas colin??aires

def checkingDoublon(A,L): #verifie si un vecteur A est colineaire ?? un des vecteurs d'une liste L
    nA=len(A)
    nL=len(L)
    i=0
    while i<nL and checkingColineaire(A,L[i])==False: #tant qu'aucun vecteur de la liste n'est colin??aire ?? A on poursuit la recherche
        i+=1
    if i==nL:        #on est arriv?? au bout de la liste
        return(False)  #donc aucun n'est colin??aire, A n'est donc pas un "doublon"
    else:            #on a trouv?? un vecteur colin??aire ?? A
        return(True)   # A est donc un "doublon"

def combinaisons(l,p): #creer toutes les combinaisons possibles d'element de l et de longueur p
    n=len(l)
    composantes=[]
    nb = n**p
    for k in range(1,p+1):
        aux=[]
        for u in range(n):
            aux += (  (n**(p-k))*[l[u]]  )          #c'est un kdo de romain, la flemme de comprendre, faut que je l'adapte de toute fa??on
        aux=(n**(k-1))*aux
        composantes.append(aux)
    aux_f=[]
    for k in range(nb):
        aux2 = []
        for i in range(p):
            aux2.append(composantes[i][k])
        aux_f.append(aux2)
    return(aux_f)

def ajoutListeElement(Element,ElementsPresents,Quantite): #ajouter un element dans la liste d'elements, soit en updatant une quantit?? si il y'est d??j??, soit en le rajoutant si il n'y est pas
        in_Elements=False          #on considere de base que l'element n'est pas dans notre liste
        for E in ElementsPresents:  #on teste chaque element d??j?? dans la liste
            if Element==E[0]:      #si le nom est reconnu pour un element de la liste
                in_Elements=True   #alors l'element est dans la liste
                E[1]+=int(Quantite) #on update la quantit?? d??j?? pr??sente en y ajoutant la quantit?? alg??brique
        if in_Elements==False: #si au bout du compte il n'est pas dans la liste
            ElementsPresents.append([Element,int(Quantite)]) #on l'ajoute ?? la liste et avec sa quantit?? alg??brique

def checkingEquilibre(ListeReactifs,ListeProduits,CoefficientsStoechiometriques): #v??rifier si une combinaison de coefficients, munies d'une liste de r??actifs et de produits permet d'obtenir une ??quation ??quilibr??e
    ChargesPresentes=[["+",0],["-",0]]
    ElementsPresents=[]  #initialiser la liste d'??l??ment pr??sent
    nCoeff=0  #initialiser l'indice du coefficient dans la liste de coefficients
    for Reactif in ListeReactifs:
        Statut='Reactif'
        Coeff = CoefficientsStoechiometriques[nCoeff] #on prend le coefficient qui correspond
        decompositionEspece(Reactif,-Coeff,ElementsPresents,ChargesPresentes) #on d??compose le r??actif
        nCoeff+=1 #on passe au coefficient suivant, pour le prochain r??actif
    for Produit in ListeProduits:  #idem pour les produits en changeant le statut
        Statut='Produit'
        Coeff = CoefficientsStoechiometriques[nCoeff]
        decompositionEspece(Produit,Coeff,ElementsPresents,ChargesPresentes)
        nCoeff+=1
    Equilibre=True #on initialise l'??quilibre comme v??rifi?? de base
    for E in ElementsPresents: #pour chaque ??l??ment de la liste des ??l??ments pr??sents
        if E[1]!=0: #on verifie si la quantit?? finale est nulle (??a voudrait dire que la quantit?? de produits est ??gale ?? la quantit?? de r??actifs
            Equilibre=False #si pour l'un ??a n'est pas le cas, alors l'??quilibre est rompu
    return(Equilibre) #si l'equilibre n'a pas ??t?? rompu cela renverra True, sinon ce sera False

#def affichageEspece

def rechercheCoefficientsEquilibre(ListeReactifs,ListeProduits,limite=10): #recherche la ou les mani??re(s) d'??quilibrer une r??action avec certains r??actifs et certains produits avec des coefficients inferieurs ou ??gaux ?? la limite choisie (10 par d??faut)
    T=time.time() #inutile, juste pour me donner le temps exact d'execution
    nReact=len(ListeReactifs) #quantit?? de r??actifs diff??rents
    nProd=len(ListeProduits) #quantit?? de produits diff??rents
    ListeCoefficientsEquilibres=[] #on initialise la liste de combinaisons de coefficients qui fonctionnent
    Possibilites=list(combinaisons(range(1,limite+1), nReact+nProd)) #on cr??e la liste de toutes les combinaisons possibles de coefficients de maximum la limite choisie et de taille correspondante ?? la quantit?? de coefficients n??cessaire
    for CoefficientsStoechiometriques in Possibilites: #on teste chaque combinaison cr????e
        if checkingEquilibre(ListeReactifs,ListeProduits,CoefficientsStoechiometriques)==True and checkingDoublon(CoefficientsStoechiometriques,ListeCoefficientsEquilibres)==False: #elle est bonne si l'equilibre est respect?? et que la combinaison trouv??e n'est pas juste un multiple d'un combinaison d??j?? trouv??e
            ListeCoefficientsEquilibres.append(CoefficientsStoechiometriques) #elle est bonne donc on l'a garde
            EquationReaction="" #on va l'afficher ??crite avec le formalisme habituel
            for a in range(0,nReact): #pour chaque r??actif
                EquationReaction+=afficherCoefficient(CoefficientsStoechiometriques[a]) #on affiche le coefficient
                EquationReaction+=" " #espace
                EquationReaction+=str(ListeReactifs[a]) #le nom de l'??l??ment
                if a!=nReact-1: # tant que ??a n'est pas le dernier r??actif
                    EquationReaction+=" " #espace
                    EquationReaction+="+" #signe plus
                    EquationReaction+=" " #espace
                else: #sinon c'??tait le dernier
                    EquationReaction+=" " #espace
                    EquationReaction+="=" #??gal
                    EquationReaction+=" " #espace
            for b in range(0,nProd): #idem pour les produits
                EquationReaction+=afficherCoefficient(CoefficientsStoechiometriques[b+nReact])
                EquationReaction+=" "
                EquationReaction+=str(ListeProduits[b])
                if b!=nProd-1:
                    EquationReaction+=" "
                    EquationReaction+="+"
                    EquationReaction+=" "
            print(EquationReaction) #on affiche l'??quation qu'on vient d'??crire
    print(time.time()-T) #on affiche le temps final d'execution
    return(ListeCoefficientsEquilibres) #on renvoie toutes les combinaisons de coefficients qui fonctionnent
