"Fichier gérant les collisions entre les pieèces"

class Manger():

    def __init__(self):
        self.manger_noir = []
        self.manger_blanc = []

    def manger(self, objet):
        if objet.couleur == "noir":
            self.manger_noir.append(objet)
        else:
            self.manger_blanc.append(objet)

    def effacer_blanc(self):
        self.manger_blanc = []

    def effacer_noir(self):
        self.manger_noir = []





"""Fonction qui gère les collisions en cas de déplacement
elle déplace la pièce s'il n'y a pas de pièce sur notre trajet,
s'il n'y pas de pièce de même couleur à l'endroit où on veut aller"""
"""Cette fonction supprime du plateau et stock les pièces mangées"""

def deplacement(plateau, piece, position_init, manger, objet, L_objet):

    pos_i = list(position_init) #on sauvegarde la position initiale
    if type(objet) == type(str()):
        return("")

    """Deplacement Pion"""
    if objet.nom == "Pion":
        dep = piece[0] - pos_i[0] #deplacement du pion

        """Si on se déplace de deux"""
        if abs(dep) == 2 and objet.départ == 0 and piece[1] == pos_i[1]:
            if dep < 0 and objet.couleur == "blanc": #On déplace un pion blanc
                """On regarde s'il n'y a pas un pion entre nous
                et notre nouvelle position
                On verifie aussi que la nouvelle position est libre"""
                if type(plateau.plateau[pos_i[0] - 1][pos_i[1]]) == type(str()) and \
                   type(plateau.plateau[piece[0]][piece[1]]) == type(str()):
                    objet.deplacement(piece[0], piece[1])
                    plateau.modifier(objet.position, objet)
                    plateau.modifier(pos_i, "O")

            elif dep > 0 and objet.couleur == "noir": #On déplace un pion noir
                if type(plateau.plateau[pos_i[0] + 1][pos_i[1]]) == type(str()) and \
                   type(plateau.plateau[piece[0]][piece[1]]) == type(str()): 
                    objet.deplacement(piece[0], piece[1])
                    plateau.modifier(objet.position, objet)
                    plateau.modifier(pos_i, "O")

            """Si on se déplace d'une case"""
        elif abs(dep) == 1 and piece[1] == pos_i[1] and \
             type(plateau.plateau[piece[0]][piece[1]]) == type(str()):
            objet.deplacement(piece[0], piece[1])
            plateau.modifier(objet.position, objet)
            plateau.modifier(pos_i, "O")

            """Si on mange une pièce"""
        elif abs(dep) == 1 and piece[1] != pos_i[1]:
            objet_mangé = plateau.plateau[piece[0]][piece[1]]

            """On vérifie deux choses:
            - L'objet mangé est d'une couleur différente de celle de notre pion
            - L'utilisateur ne triche pas et déplace son pion
            d'une case en diagonale"""

            if type(objet_mangé) != type(str()):
                if objet.couleur != objet_mangé.couleur and (piece[1] == \
                    pos_i[1] - 1 or piece[1] == pos_i[1] + 1):
                    manger.manger(objet_mangé)
                    objet.manger(piece[0], piece[1])
                    plateau.modifier(objet.position, objet)
                    plateau.modifier(pos_i, "O")

                """On mange une pièce "en passant" """
            else:
                if (piece[1] == pos_i[1] - 1 or piece[1] == pos_i[1] + 1) : #on se déplace bien d'une case en diagonale
                    objet_mangé = plateau.plateau[piece[0] - dep][piece[1]] #C'est  là la vraie pièce mangée
                    if objet_mangé.nom == "Pion" and \
                        objet_mangé.couleur != objet.couleur:
                        manger.manger(objet_mangé)
                        objet.manger(piece[0], piece[1])
                        plateau.modifier(objet.position, objet)
                        plateau.modifier(pos_i, "O")
                        plateau.modifier((piece[0] - dep, piece[1]), "O")




    """Déplacement Tour, Fou et Reine"""
    if objet.nom == "Tour" or objet.nom == "Dame" or objet.nom == "Fou":
        objet.deplacement(piece[0], piece[1])
        #Fonction qui regarde s'il y a des pièces sur notre trajet
        test = f_dep(objet, piece, pos_i, plateau) 
        if test == True: #Il y a une piece sur notre trajet
            objet.modifier(pos_i[0], pos_i[1])
        else:
            objet_plateau = plateau.plateau[piece[0]][piece[1]]
            if type(objet_plateau) != type(str()) and \
               objet_plateau.couleur != objet.couleur: #On se déplace et mange une pièce
                manger.manger(objet_plateau)
                plateau.modifier(objet.position, objet)
                plateau.modifier(pos_i, "O")
            elif type(objet_plateau) != type(str()) and \
               objet_plateau.couleur == objet.couleur: #On se déplace sur une pièce de la même couleur
                objet.modifier(pos_i[0], pos_i[1]) #On annule le déplacement
            else:
                plateau.modifier(objet.position, objet) #On se déplace sur un endroit vide
                plateau.modifier(pos_i, "O")




    """Déplacement du Cheval"""
    if objet.nom == "Cheval":
        objet.deplacement(piece[0], piece[1])
        objet_plateau = plateau.plateau[piece[0]][piece[1]]

        if type(objet_plateau) == type(str()) and objet.position[0] != pos_i[0]: #On se déplace sur une case vide
            plateau.modifier(objet.position, objet) 
            plateau.modifier(pos_i, "O")
        elif type(objet_plateau) != type(str()): #La case n'est pas vide
            if objet_plateau.couleur == objet.couleur: #Il y a déjà une pièce à nous
                objet.modifier(pos_i[0], pos_i[1])
            else: #Il y a une pièce de l'adversaire
                manger.manger(objet_plateau)
                plateau.modifier(objet.position, objet)
                plateau.modifier(pos_i, "O")



    """Déplacement du Roi"""
    if objet.nom == "Roi":
        objet_plateau = plateau.plateau[piece[0]][piece[1]]
        test = False
        
        """On regarde d'abord si on ne déplace pas notre roi sur une pièce
        à nous
        On créé ces deux if car ils nous servent lorsqu'on teste
        si notre roi n'est pas en position d'échec lorsqu'on le
        déplace"""
        if type(objet_plateau) != type(str()) and \
           objet_plateau.couleur != objet.couleur:
            objet.deplacement(piece[0], piece[1]) #Il y a une pièce ennemie
            plateau.modifier(pos_i, "O")
            test = echec_roi(plateau, objet, piece, pos_i, L_objet, manger)
        if type(objet_plateau) == type(str()):
            objet.deplacement(piece[0], piece[1]) #Pas de pièce à nous à manger
            plateau.modifier(pos_i, "O")
            test = echec_roi(plateau, objet, piece, pos_i, L_objet, manger)

                
        if test == False and objet.position != tuple(pos_i): #On n'est pas en échec
            if type(objet_plateau) == type(str()) and objet.position[0] != pos_i[0]: #On se déplace sur une case vide
                plateau.modifier(objet.position, objet) 
                plateau.modifier(pos_i, "O")
            elif type(objet_plateau) != type(str()): #La case n'est pas vide
                if objet_plateau.couleur == objet.couleur: #Il y a déjà une pièce à nous
                    objet.modifier(pos_i[0], pos_i[1])
                    plateau.modifier(pos_i, objet)
                else: #Il y a une pièce de l'adversaire
                    manger.manger(objet_plateau)
                    plateau.modifier(objet.position, objet)
                    plateau.modifier(pos_i, "O")
        elif test == True and type(objet_plateau) != type(str()) and\
             objet_plateau.couleur != objet.couleur:
            print("échec")




"""Fonction chargée de regarder s'il y a des pièces sur notre trajet"""
"""On l'utilise pour les tours, la dame et les fous"""
def f_dep(objet, piece, pos_i, plateau):

    """Pas de déplacement"""
    if objet.position[0] == pos_i[0] and objet.position[1] == pos_i[1]:
        return(True) #On ne déplace pas l'objet

        """Déplacement en ligne (on regarde tout sauf la position finale)"""
    elif objet.position[1] == pos_i[1]:
        for i in range(min(objet.position[0], pos_i[0]) + 1, \
                       max(objet.position[0], pos_i[0])):
            if type(plateau.plateau[i][pos_i[1]]) != type(str()):
                return(True) #Il y a une pièce sur notre parcours
        return(False)

        """Déplacement en colonne"""
    elif objet.position[0] == pos_i[0]:
        for i in range(min(objet.position[1], pos_i[1]) + 1, \
                       max(objet.position[1], pos_i[1])):
            if type(plateau.plateau[pos_i[0]][i]) != type(str()):
                return(True) #Il y a une pièce sur notre parcours
        return(False)

        """Déplacement en diagonale"""
    else:
        pos_init = list(pos_i)
        while piece[0] !=  pos_init[0] and piece[1] !=  pos_init[1]:
            if piece[0] >  pos_init[0]:
                 pos_init[0] += 1
            if piece[0] <  pos_init[0]:
                 pos_init[0] -= 1
            if piece[1] >  pos_init[1]:
                 pos_init[1] += 1
            if piece[1] <  pos_init[1]:
                 pos_init[1] -= 1

            if type(plateau.plateau[ pos_init[0]][ pos_init[1]]) != \
               type(str()) and piece[0] !=  pos_init[0]:
                return(True)
        return(False)




"""Fonction chargée de vérifier que le Roi ne se déplace pas sur une case
où il serait menacé par une pièce"""
def echec_roi(plateau, objet, piece, pos_i, L_objet, manger):

    L = list(L_objet)

    for i in L:
        if i.couleur != objet.couleur and i not in \
            (manger.manger_blanc or manger.manger_noir) and \
            i.nom != "Roi" and i.position != objet.position:
            #Si i.position = Roi.position alors le Roi mange la pièce
            
            """On simule le déplacement de chaque pièce adverse sauf
            le roi car c'est une fonction récursive"""
            pos_i_menace = list(i.position)
            deplacement(plateau, piece, i.position, manger, i, L_objet)
            
            if i.position == objet.position:
                objet.modifier(pos_i[0], pos_i[1])
                plateau.modifier(objet.position, objet)
                plateau.modifier(i.position, "O")
                i.modifier(pos_i_menace[0], pos_i_menace[1])
                plateau.modifier(i.position, i)
                print("impossible : position d'échec à cause d'une pièce", piece)
                return(True) #Le roi est en échec

        elif i.couleur != objet.couleur and i not in \
            (manger.manger_blanc or manger.manger_noir) and \
            i.nom == "Roi" and i.position != objet.position:
            """si on tombe sur le roi adverse"""
            if abs(i.position[0] - objet.position[0]) <= 1 and \
               abs(i.position[1] - objet.position[1]) <= 1:
                """Les Rois sont sur des cases qui se touchent"""
                objet.modifier(pos_i[0], pos_i[1])
                plateau.modifier(objet.position, objet)
                print("impossible : position d'échec à cause du roi")
                return(True)
                
    return(False)
                
                    
                
                


