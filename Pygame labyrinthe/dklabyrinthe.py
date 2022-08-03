import pygame
from pygame.locals import *
from fonctions import *
from classes import *



pygame.init()


jeu = 1
pygame.time.Clock().tick(30)
while jeu:
    continuer = 1
    menu = 1

    pygame.time.Clock().tick(30)
    while menu:

        
        fenetre = pygame.display.set_mode((450,450))
        fond = pygame.image.load("Images\\fond.jpg").convert()
        fenetre.blit(fond, (0,0))

        texte = pygame.image.load("Images\\Texte.png").convert_alpha()
        fenetre.blit(texte, (75,75))

        texte_menu = pygame.image.load("Images\\menu.png").convert_alpha()
        fenetre.blit(texte_menu, (75, 375))

        dk_haut_gauche = pygame.image.load("Images\\dk_droite_bis.png").convert_alpha()
        dk_bas_gauche = pygame.image.load("Images\\dk_droite_bis.png").convert_alpha()
        dk_haut_droit = pygame.image.load("Images\\dk_gauche_bis.png").convert_alpha()
        dk_bas_droit = pygame.image.load("Images\\dk_gauche_bis.png").convert_alpha()
        
        fenetre.blit(dk_haut_gauche, (30,30))
        fenetre.blit(dk_bas_gauche,(30, 390))
        fenetre.blit(dk_haut_droit, (390,30))
        fenetre.blit(dk_bas_droit, (390,390))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                jeu = 0
                menu = 0
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    menu = 0
                    L, x, y = convertir_laby_list(afficher_laby("Niveau 1"))
                    fenetre = pygame.display.set_mode((x*20,y*20), RESIZABLE)
                    for i in range (int(x//22.5)+1):
                        for j in range (int(y//22.5)+1):
                            fond = pygame.image.load("Images\\fond.jpg").convert()
                            fenetre.blit(fond, (i*450,j*450))

                    carte = Niveau("carte", L)
                    carte.afficher_niveau(fenetre)
                
                    dk = Perso(carte.départ, carte.arrivée)
                    dk.affichage(fenetre)

                if event.key == K_F2:
                    menu = 0
                    L, x, y = convertir_laby_list(afficher_laby("Niveau 2"))
                    fenetre = pygame.display.set_mode((x*20,y*20), RESIZABLE)
                    for i in range (int(x//22.5)+1):
                        for j in range (int(y//22.5)+1):
                            fond = pygame.image.load("Images\\fond.jpg").convert()
                            fenetre.blit(fond, (i*450,j*450))

                    carte = Niveau("carte", L)
                    carte.afficher_niveau(fenetre)

                    dk = Perso(carte.départ, carte.arrivée)
                    dk.affichage(fenetre)

                if event.key == K_F3:
                    menu = 0
                    L, x, y = convertir_laby_list(afficher_laby("Niveau 3"))
                    fenetre = pygame.display.set_mode((x*20,y*20), RESIZABLE)
                    for i in range (int(x//22.5)+1):
                        for j in range (int(y//22.5)+1):
                            fond = pygame.image.load("Images\\fond.jpg").convert()
                            fenetre.blit(fond, (i*450,j*450))

                    carte = Niveau("carte", L)
                    carte.afficher_niveau(fenetre)

                    dk = Perso(carte.départ, carte.arrivée)
                    dk.affichage(fenetre)
                    
                if event.key == K_F4:
                    menu = 0
                    L, x, y = convertir_laby_list(afficher_laby("Niveau 4"))
                    fenetre = pygame.display.set_mode((x*20,y*20), RESIZABLE)
                    for i in range (int(x//22.5)+1):
                        for j in range (int(y//22.5)+1):
                            fond = pygame.image.load("Images\\fond.jpg").convert()
                            fenetre.blit(fond, (i*450,j*450))

                    carte = Niveau("carte", L)
                    carte.afficher_niveau(fenetre)

                    dk = Perso(carte.départ, carte.arrivée)
                    dk.affichage(fenetre)

                if event.key == K_F5:
                    menu = 0
                    L, x, y = convertir_laby_list(afficher_laby("Niveau 5"))
                    fenetre = pygame.display.set_mode((x*20,y*20), RESIZABLE)
                    for i in range (int(x//22.5)+1):
                        for j in range (int(y//22.5)+1):
                            fond = pygame.image.load("Images\\fond.jpg").convert()
                            fenetre.blit(fond, (i*450,j*450))

                    carte = Niveau("carte", L)
                    carte.afficher_niveau(fenetre)

                    dk = Perso(carte.départ, carte.arrivée)
                    dk.affichage(fenetre)

        
    pygame.display.flip()

    pygame.key.set_repeat(400, 30)
    i=0
    while continuer:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
                menu = 0
                jeu = 0

            if event.type == KEYDOWN and event.key == K_p:
                continuer=0
                
                
            if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN):
                """for i in range ((x//20)+1):
                    for j in range ((y//20)+1):
                        fond = pygame.image.load("Images\\fond.jpg").convert()
                        fenetre.blit(fond, (i*450,j*450))            
                carte.afficher_niveau(fenetre)"""

                carte.départ = list(carte.départ)
                
                if dk.position_liste == carte.départ:
                    fenetre.blit(carte.départ_image, dk.position_dk)

                elif dk.position_dk.x%450 == 440 and dk.position_dk.y%450 == 440:
                    fenetre.blit(fond, dk.position_dk, (dk.position_dk.x%450,dk.position_dk.y%450, 10,10))
                    fenetre.blit(fond, (dk.position_dk.x+10, dk.position_dk.y), (0,dk.position_dk.y%450, 10,10))
                    fenetre.blit(fond, (dk.position_dk.x, dk.position_dk.y+10), (dk.position_dk.x%450,dk.position_dk.y%450, 10,10))
                    fenetre.blit(fond, (dk.position_dk.x+10, dk.position_dk.y+10), (dk.position_dk.x%450,0, 10,10))

                elif dk.position_dk.x%450 == 440:
                    fenetre.blit(fond, dk.position_dk, (dk.position_dk.x%450,dk.position_dk.y%450, 10,20))
                    fenetre.blit(fond, (dk.position_dk.x+10, dk.position_dk.y), (0,dk.position_dk.y%450, 10,20))

                elif dk.position_dk.y%450 == 440:
                    fenetre.blit(fond, dk.position_dk, (dk.position_dk.x%450,dk.position_dk.y%450, 20,10))
                    fenetre.blit(fond, (dk.position_dk.x, dk.position_dk.y+10), (dk.position_dk.x%450,0, 20,10))

                else:   
                    fenetre.blit(fond, dk.position_dk, (dk.position_dk.x%450,dk.position_dk.y%450, 20,20))

                dk.mouvement(L, event)
                dk.arrivee()
                continuer = dk.continuer
                
                fenetre.blit(dk.dk, dk.position_dk)
                pygame.display.flip()
    
    
pygame.quit()
