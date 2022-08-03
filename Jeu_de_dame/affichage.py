import pygame
from pygame.locals import *
from fonctions import *




#Fonction charger d'afficher le plateau à partir de plateau.plat qui est une liste de liste
def print_plateau(jeu, fenetre, joueur):
    plateau=pygame.image.load("plateau.jpg").convert()
    fenetre.blit(plateau,(0,0))
    pygame.display.set_caption(joueur)


    for i in jeu.plat:
        for j in i:
            if j!="O":
                pion = pygame.image.load(j.picture).convert_alpha()
                pion_x = j.x * 70
                pion_y = j.y*70
                fenetre.blit(pion, (pion_x,pion_y))


    pygame.display.flip()

#Fonction chargé de mettre en route le jeu
def play(jeu, fenetre, joueur, color):

    manger=False #défini si on a mangé ou non une pièce
    continuer = 1
    first_click=True #défini si on a bien choisi une pièce valide
    while continuer:
        for event in pygame.event.get():

            if event.type == QUIT:
                continuer = 0

            if event.type == KEYDOWN and event.key==K_a: #On appuie sur q pour déselectionner la pièce sélectionnée
                first_click=True

            if event.type == MOUSEBUTTONDOWN:
                if event.button==1:

                    #On sélectionne une pièce
                    if first_click==True:
                        print(jeu)
                        x=event.pos[0] #Position de la pièce
                        y=event.pos[1]
                        objet = select_objet(jeu, x,y) #Sélection de la pièce
                        if objet!="O" and objet.couleur==color: #On vérifie qu'on n'a pas sélectionné de case vide ni une pièce de la mauvaise couleur
                            first_click=False

                    #On sélectionne la case sur laquelle on se déplace
                    elif first_click==False:
                        x=event.pos[0]
                        y=event.pos[1]
                        resultat, manger = move_objet(objet,jeu, x, y) #Résultat = s'est-on déplacé (True/False) et a-t-on mangé une pièce (True/False)
                        print(jeu)
                        if resultat==True:
                            print_plateau(jeu, fenetre, joueur) #Si on s'est déplacé, on réaffiche le plateau
                            first_click = True
                            if not manger: #Si on n'a pas mangé de pièce c'est à l'autre joueur de jouer
                                return jeu

                            else: #Si on a mangé une pièce
                                objet = select_objet(jeu, x, y)
                                continuer_bis=1
                                while continuer_bis==1: #on continue tant que le joueur souhaite essayer de manger des pièces
                                    for event_bis in pygame.event.get():
                                        if event_bis.type == KEYDOWN and event_bis.key==K_a: #on décide qu'on ne peut rien faire de plus: on arrête de jouer
                                            continuer_bis=0
                                            first_click = True
                                            return jeu

                                        elif event_bis.type==MOUSEBUTTONDOWN and event_bis.button==1: #on essaie de manger une autre pièce
                                            x_bis=event_bis.pos[0]
                                            y_bis=event_bis.pos[1]
                                            manger=eat(objet,jeu, x_bis, y_bis) #objet = la pièce déjà selectionnée dans la première boucle
                                            print_plateau(jeu, fenetre, joueur) #Si on a réussi à re-manger une pièce on réactualise le plateau
                                        elif event.type == QUIT:
                                            continuer_bis=0
                                            continuer=0


