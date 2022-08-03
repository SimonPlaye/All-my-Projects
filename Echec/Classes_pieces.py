"Classes pieces"
"Fichier contenant toutes les pièces avec leurs caractéristiques ainsi que"
"le plateau"
import math
import pygame as py
from pygame.locals import *


class Plateau:

    def __init__(self):
        L = []
        for i in range(8):
            L.append([])
            for j in range(8):
                L[i].append("O")
        self.plateau = L
        self.image = py.image.load("Images\\Echequier.png").convert_alpha()

    def __repr__(self):
        a = ""
        for i in range(8):
            a+="\n"
            for j in range(8):
                if type(self.plateau[i][j])!= type(str()):
                    a+=self.plateau[i][j].symbole
                else:     
                    a+=self.plateau[i][j]
        return(a)

    def modifier(self, position, objet):
        self.plateau[position[0]][position[1]] = objet
            
        

class Pion_noir(Plateau):

    def __init__(self,nom, y):
        self.nom = "Pion"
        self.symbole = nom
        self.position = (1,y)
        self.départ = 0
        self.couleur = "noir"
        self.image = py.image.load("Images\\Pion_noir.png").convert_alpha()
        self.pos_py = (90, 90*y)

    def __repr__(self):
        return("{}".format(self.symbole))

    def deplacement(self, posx, *posy):
        if self.départ == 0 and (posx-self.position[0] == 1 or posx-self.position[0] == 2):
            self.position = (posx, self.position[1])
            self.départ = 1
            self.pos_py = (posx*90, self.pos_py[1])
        elif posx-self.position[0] == 1:
            self.position = (posx, self.position[1])
            self.pos_py = (posx*90, self.pos_py[1])
        else:
            return(False)

    def manger(self, posx, posy):
        self.position = (posx, posy)
        self.pos_py = (posx*90, posy*90)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)


        
class Pion_blanc(Plateau):

    def __init__(self, nom, y):
        self.nom = "Pion"
        self.symbole = nom
        self.position = (6,y)
        self.départ = 0
        self.couleur = "blanc"
        self.image = py.image.load("Images\\Pion_blanc.png").convert_alpha()
        self.pos_py = (540, 90*y)

    def __repr__(self):
        return(self.symbole)

    def deplacement(self, posx, *posy):
        if self.départ == 0 and (self.position[0]-posx == 1 or self.position[0]-posx == 2):
            self.position = (posx, self.position[1])
            self.départ = 1
            self.pos_py = (posx*90, self.pos_py[1])
        elif self.position[0]-posx == 1:
            self.position = (posx, self.position[1])
            self.pos_py = (posx*90, self.pos_py[1])
        else:
            return(False)

    def modifier(self, posx, posy):
        self.position = (posx, posy)
        self.pos_py = (posx*90, posy*90)

    def manger(self, posx, posy):
        self.position = (posx, posy)
        self.pos_py = (posx*90, posy*90)


class Roi_noir(Plateau):

    def __init__(self):
        self.nom = "Roi"
        self.symbole = "Rn"
        self.position = (0,4)
        self.couleur = "noir"
        self.image = py.image.load("Images\\Roi_noir.png").convert_alpha()
        self.pos_py = (0, 360)

    def __repr__(self):
        return(self.symbole)

    def deplacement(self, posx, posy):
        if abs(self.position[0]-posx)<=1 and abs(self.position[1]-posy)<=1:
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)

        
class Roi_blanc(Plateau):

    def __init__(self):
        self.nom = "Roi"
        self.symbole = "Rb"
        self.position = (7,4)
        self.couleur = "blanc"
        self.image = py.image.load("Images\\Roi_blanc.png").convert_alpha()
        self.pos_py = (630, 360)

    def __repr__(self):
        return(self.symbole)

    def deplacement(self, posx, posy):
        if abs(self.position[0]-posx)<=1 and abs(self.position[1]-posy)<=1:
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)



class Dame_noire(Plateau):

    def __init__(self):
        self.nom = "Dame"
        self.symbole = "Dn"
        self.position = (0,3)
        self.couleur = "noir"
        self.image = py.image.load("Images\\Dame_noir.png").convert_alpha()
        self.pos_py = (0, 270)

    def __repr__(self):
        return(self.symbole)

    def deplacement(self, posx, posy):
        if (posx - self.position[0] == 0 and posy - self.position[1]!=0) or \
           (posx - self.position[0] != 0 and posy - self.position[1]==0) or \
           (abs(posx - self.position[0]) == abs(posy - self.position[1])):
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)


        

class Dame_blanche(Plateau):

    def __init__(self):
        self.nom = "Dame"
        self.symbole = "Db"
        self.position = (7,3)
        self.couleur = "blanc"
        self.image = py.image.load("Images\\Dame_blanc.png").convert_alpha()
        self.pos_py = (630, 270)

    def __repr__(self):
        return(self.symbole)

    def deplacement(self, posx, posy):
        if (posx - self.position[0] == 0 and posy - self.position[1]!=0) or \
           (posx - self.position[0] != 0 and posy - self.position[1]==0) or \
           (abs(posx - self.position[0]) == abs(posy - self.position[1])):
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)



class Tour_noire(Plateau):

    def __init__(self, nom, y):
        self.nom="Tour"
        self.symbole = nom
        self.position = (0,y)
        self.couleur = "noir"
        self.image = py.image.load("Images\\Tour_noir.png").convert_alpha()
        self.pos_py = (0, y*90)

    def __repr__(self):
        return self.symbole

    def deplacement(self, posx, posy):
        if (posx - self.position[0] == 0 and posy - self.position[1]!=0) or \
           (posx - self.position[0] != 0 and posy - self.position[1]==0):
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)

    

class Tour_blanche(Plateau):

    def __init__(self, nom, y):
        self.nom="Tour"
        self.symbole = nom
        self.position = (7, y)
        self.couleur = "blanc"
        self.image = py.image.load("Images\\Tour_blanc.png").convert_alpha()
        self.pos_py = (630, y*90)
        

    def __repr__(self):
        return self.symbole

    def deplacement(self, posx, posy):
        if (posx - self.position[0] == 0 and posy - self.position[1]!=0) or \
           (posx - self.position[0] != 0 and posy - self.position[1]==0):
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)


class Cheval_noir(Plateau):

    def __init__(self, nom, y):
        self.nom="Cheval"
        self.symbole = nom
        self.position = (0,y)
        self.couleur = "noir"
        self.image = py.image.load("Images\\Cheval_noir.png").convert_alpha()
        self.pos_py = (0, y*90)

    def __repr__(self):
        return self.symbole

    def deplacement(self, posx, posy):
        if (abs(posx - self.position[0]) == 2 and abs(posy - self.position[1]) ==1)\
            or (abs(posx - self.position[0]) == 1 and abs(posy - self.position[1]) ==2):
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)



class Cheval_blanc(Plateau):

    def __init__(self, nom, y):
        self.nom="Cheval"
        self.symbole = nom
        self.position = (7,y)
        self.couleur = "blanc"
        self.image = py.image.load("Images\\Cheval_blanc.png").convert_alpha()
        self.pos_py = (630, y*90)

    def __repr__(self):
        return self.symbole

    def deplacement(self, posx, posy):
        if (abs(posx - self.position[0]) == 2 and abs(posy - self.position[1])==1)\
            or (abs(posx - self.position[0]) == 1 and abs(posy - self.position[1])==2):
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)



class Fou_noir(Plateau):
    def __init__(self, nom, y):
        self.nom="Fou"
        self.symbole = nom
        self.position = (0,y)
        self.couleur = "noir"
        self.image = py.image.load("Images\\Fou_noir.png").convert_alpha()
        self.pos_py = (0, y*90)

    def __repr__(self):
        return self.symbole

    def deplacement(self, posx, posy):
        if abs(posx - self.position[0]) == abs(posy - self.position[1]):           
            self.position = (posx, posy)
            self.pos_py = (posx*90, posy*90)
        else:
            return(False)
        
    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)

        

class Fou_blanc(Plateau):
    def __init__(self, nom, y):
        self.nom="Fou"
        self.symbole = nom
        self.position = (7,y)
        self.couleur = "blanc"
        self.image = py.image.load("Images\\Fou_blanc.png").convert_alpha()
        self.pos_py = (630, y*90)

    def __repr__(self):
        return self.symbole

    def deplacement(self, posx, posy):
        if abs(posx - self.position[0]) == abs(posy - self.position[1]):
                self.position = (posx, posy)
                self.pos_py = (posx*90, posy*90)
        else:
            return(False)

    def modifier(self, x, y):
        self.position = (x, y)
        self.pos_py = (x*90, y*90)



