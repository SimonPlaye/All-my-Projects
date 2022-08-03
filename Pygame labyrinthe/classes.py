from fonctions import *
import pygame
from pygame.locals import *

"""côté d'un mur: 20 pixels"""

class Niveau():
    
    def __init__(self, nom, niveau):
        self.nom = nom
        self.niveau = niveau
        self.départ=(0,0)
        self.arrivée = (0,0)
        self.départ_image = pygame.image.load("Images\\depart.png").convert()

    def afficher_niveau(self, fenetre):
        a=20
        for i in range (len(self.niveau)):
            for j in range(len(self.niveau[0])):
                if self.niveau[i][j] == "O":
                    mur = pygame.image.load("Images\\mur.png").convert()
                    fenetre.blit(mur, (j*a, i*a))
                if self.niveau[i][j] == "U":
                    arrivee = pygame.image.load("Images\\arrivee.png").convert_alpha()
                    fenetre.blit(arrivee, (j*a, i*a))
                    self.arrivée=[j, i]
                if self.niveau[i][j] == "X":
                    depart = pygame.image.load("Images\\depart.png").convert()
                    fenetre.blit(depart, (j*a, i*a))
                    self.départ=[j, i]
    
            
class Perso():

    def __init__(self, position_case, case_arrivee):

        self.position_liste = position_case
        self.position_pixel= [position_case[0]*20, position_case[1]*20]
        self.dk = pygame.image.load("Images\\dk_droite.png").convert_alpha()
        self.direction_droite = pygame.image.load("Images\\dk_droite.png").convert_alpha()
        self.direction_bas = pygame.image.load("Images\\dk_bas.png").convert_alpha()
        self.direction_gauche = pygame.image.load("Images\\dk_gauche.png").convert_alpha()
        self.direction_haut = pygame.image.load("Images\\dk_haut.png").convert_alpha()
        self.position_dk=self.dk.get_rect(x=self.position_pixel[0], y=self.position_pixel[1])
        self.case_arrivee = case_arrivee
        self.continuer = 1
        
    def mouvement(self, L, event):

        if event.type == KEYDOWN:
            if event.key == K_LEFT and L[self.position_liste[1]][self.position_liste[0]-1] !="O":
                self.position_dk = self.position_dk.move(-20,0)
                self.dk = self.direction_gauche
                self.position_liste[0]=self.position_liste[0]-1
                
                
            if event.key == K_RIGHT and L[self.position_liste[1]][self.position_liste[0]+1] !="O":
                self.position_dk = self.position_dk.move(20,0)
                self.dk = self.direction_droite
                self.position_liste[0]=self.position_liste[0]+1
                
            if event.key == K_UP and L[self.position_liste[1]-1][self.position_liste[0]] !="O":
        
                self.position_dk = self.position_dk.move(0,-20)
                self.dk = self.direction_haut
                self.position_liste[1]=self.position_liste[1]-1

            if event.key == K_DOWN and L[self.position_liste[1]+1][self.position_liste[0]] !="O":
                self.position_dk = self.position_dk.move(0,20)
                self.dk=self.direction_bas
                self.position_liste[1]=self.position_liste[1]+1

           


    def affichage(self, fenetre):
        position_dk = self.dk.get_rect(x=self.position_pixel[0], y=self.position_pixel[1])        
        fenetre.blit(self.dk, position_dk)
        pygame.display.flip()

    def arrivee(self):
        if self.position_liste == self.case_arrivee:
            self.continuer = 0
            
        else:
            pass
        

      
                    
                        
                     
                    
        
        
        
