# -*-coding:Utf-8 -*


"""Ce module contient plusieurs fonctions indispensables
au fonctionnement du labyrinthe"""
"""Toutes sauf la prmeière servent à gérer les sauvegardes"""

from Classes_obstacles import *
import os
import pickle


#Permet de convertir la liste contenant le labyrinthe en chaine de caractères pour pouvoir l'afficher ensuite
def convertir_liste(liste):
    chaine=''
    for i, valeur1 in enumerate(liste):
        for j, valeur2 in enumerate(liste[i]):
            chaine+=valeur2
            if j==len(liste[i])-1 and i!=len(liste)-1:
                chaine+='\n'
    return(chaine)



def convertir_chaine(chaine):

    liste1 = chaine.split('\n')
    a = 0
    b = 0
    L=[]
    for i, elt in enumerate(liste1):
        L.append([])
        for j in range(len(elt)):
            if elt[j] == 'O':
                cel = Mur(i, j)
            elif elt[j] == 'U':
                if a>0:
                    return("Il ne peut avoir qu'une seule sortie")
                else:
                    cel = Sortie(i, j)
                    a+=1
            elif elt[j] == '.':
                cel=Porte(i, j)

            elif elt[j] == 'X'.lower():
                if b>0:
                    return("Il ne peut avoir qu'un seul robot")
                else:
                    robot = Robot(i, j)
                    b+=1
            L[i].append(elt[j])
        


    for i in L[0]:
        if i != 'O' and i!='U':
            print("Il manque un mur sur la première ligne")
            raise ValueError

    for i in L[len(L)-1]:
        if i!= 'O' and i!='U':
            print("Il manque un mur sur la dernière ligne")
            raise ValueError

    for i in range(len(L)):
        if L[i][0] != 'O' and L[i][0]!='U':
            print("Il manque un mur sur le bord gauche")
            raise ValueError
        elif L[i][len(L[0])-1] != 'O' and L[i][len(L[0])-1] != 'U':
            print("Il manque un mur sur le bord droit")
            raise ValueError

    return(L, len(L[0]), len(L), robot)


def deplacement_rob(laby, robot, i, j, obstacle_avant):
    
    if Mur(i, j):
        return(False, obstacle_avant, laby)
    elif Porte(i, j):
        laby[robot.x][robot.y]=obstacle_avant
        obstacle_avant=Porte(i, j)
        laby[i][j] = robot
        return(True, obstacle_avant, laby)
    else:
        laby[robot.x][robot.y]=obstacle_avant
        obstacle_avant = " "
        laby[i][j]= robot
        return(True, obstacle_avant, laby)
    
        
    

        
