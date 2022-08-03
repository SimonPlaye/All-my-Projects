import os
from classes import *

def afficher_laby(nom_laby):
    chemin = os.path.join("cartes", nom_laby+".txt")
    with open(chemin, "r") as fichier:
        contenu = fichier.read()
        return contenu

def convertir_laby_list(nom_laby):
    a = nom_laby.split("\n")
    L=[]
    L1=[]
    b = len(a)
    c = len(a[0])

    i=0
    j=0
    while i <b:
        while j<c:
            L1.append(a[i][j])
            j+=1
        L.append(L1)
        L1=[]
        j=0
        i+=1
    return L, c, b
            
