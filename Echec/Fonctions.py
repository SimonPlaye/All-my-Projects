from Collisions import *

"""Fichier regroupant des fonctions quelconques"""



"""Fonction chargée de gérer l'évènement échec et mat"""
def echec_et_mat(plateau, Rn, Rb):

    """On doit avoir trois conditions vérifiées:
        - Le Roi est menacé par une pièce
        - On ne peut pas manger cette pièce
        - On ne peut pas interposer une pièce entre lui et l'autre pièce"""

    lpmrN = [] #Soit la liste des pièces qui menacent le Roi noi
    lpmrB = []

    return(lpmrN)


#Comment coder une fonction pour voir si on peut déplacer le roi
#en cas d'échec
"""On regarde si on peut déplacer le roi:
- On lance une boucle qu'on repète autant qu'il y a de cases autour
du roi
- Dans cette boucle on lance la fonction déplacement pour le Roi
- S'il y a une menace, la fonction ne déplace le Roi que sur les cases
où il sera à l'abri et peut laisser le Roi manger la menace
- On enregistre dans une liste ces cases libres
- Si la liste est vide on regarde si on peut déplacer une pièce, si elle ne
l'est  pas, il n'y a pas échec et mat"""

def roi_en_echec(plateau, objet_roi, L):

    pos_i = list(objet_roi.position)
    dep_possible = []
    test_manger_bis = Manger()

    """On simule le déplacement du roi sur les cases autour"""
    for i in range(3):
        piece = list(pos_i)

        #On se fixe sur une ligne
        piece[0] = pos_i[0] + i - 1
        for j in range(3):
            piece[1] = pos_i[1] + j - 1
            if piece[0] > -1 and piece[0] < 8 and piece[1] > -1 \
               and piece[1] < 8:
                deplacement(plateau, piece, pos_i, test_manger_bis, objet_roi, L)
                if objet_roi.position != tuple(pos_i):#On peut déplacer le roi sur cette case
                    dep_possible.append(objet_roi.position)
                    objet_roi.modifier(pos_i[0], pos_i[1])
                    plateau.modifier(objet_roi.position, objet_roi)
                    plateau.modifier(piece, "O")

                    """En testant le déplacement du Roi, on a potentiellement
                    manger une pièce adverse car la fonction déplacement
                    déplace le Roi en mangeant des pièces"""
                    if not test_manger_bis.manger_blanc == False:
                        print(test_manger_bis.manger_blanc)
                    if objet_roi.couleur == "noir":
                        for i in test_manger_bis.manger_blanc:
                            plateau.modifier(i.position, i)
                        test_manger_bis.effacer_blanc()
                    else:
                        for i in test_manger_bis.manger_noir:
                            plateau.modifier(i.position, i)
                        test_manger_bis.manger_noir()
                    

    print(dep_possible)
    if not dep_possible == True:
        return(True)
    else:
        return(False)
        



#Comment coder une fonction pour voir si on peut déplacer une pièce
#en cas d'échec
"""Si on ne peut pas déplacer le roi:
-Noter la position de la menace qui créé l'échec
-Noter la position du Roi
-Lister toutes les positions sur le plateau entre le roi et la menace
en comptant la position de la menace
-Faire une boucle qui regarde s'il existe une de nos pièces qui peut se rendre
sur une de ces positions
- Lister ces pièces
- Si cette liste est vide alors il y a échec et mat"""




"""Fonctions chargées de gérer l'évènement échec"""


"""On déclenche cette fonction quand l'adversaire bouge une pièce:
après que l'adversaire ait déplacé sa pièce on regarde s'il est possible
que, le coup d'après, cette pièce puisse se déplacer sur la case du Roi"""
def echec_1(plateau, Rn, Rb, objet, L):

    test_manger = Manger()
    pos_i = list(objet.position)
    if objet.couleur == "blanc":
        piece = Rn.position
        deplacement(plateau, piece, pos_i, test_manger, objet, L)
        objet.modifier(pos_i[0], pos_i[1])
        plateau.modifier(objet.position, objet)
        plateau.modifier(piece, Rn)
        if Rn in test_manger.manger_noir:
            return(True)
        else:
            return(False)
    else:
        piece = Rb.position
        deplacement(plateau, piece, pos_i, test_manger, objet, L)
        objet.modifier(pos_i[0], pos_i[1])
        plateau.modifier(objet.position, objet)
        plateau.modifier(piece, Rb)
        if Rb in test_manger.manger_blanc:
            return(True)
        else:
            return(False)
    

    
