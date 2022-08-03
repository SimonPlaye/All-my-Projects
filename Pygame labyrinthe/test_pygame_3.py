import pygame
from pygame.locals import *
from fonctions import *

L, x, y = convertir_laby_list(afficher_laby("facile"))


pygame.init()
fenetre = pygame.display.set_mode((x*15,y*15), RESIZABLE)
for i in range ((x//30)+1):
    for j in range ((y//30)+1):
        fond = pygame.image.load("Images\\fond.jpg").convert()
        fenetre.blit(fond, (i*450,j*450))

i=0

while i <15:
    j=0
    while j<15 :
        if j % 2 !=0:
            mur = pygame.image.load("Images\\mur.png").convert()
            fenetre.blit(mur, (j*30, i*30))
        j+=1
    i+=1

pygame.display.flip()


continuer = 1

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            continuer =0 
