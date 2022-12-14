from Classes_pieces import *
from Collisions import *
from Fonctions import *
import pygame
from pygame import *

pygame.init()
fenetre = pygame.display.set_mode((720,720))

a = Plateau()
fond = a.image
fenetre.blit(fond, (0,0))
L=[]

for i in range(8):
    b = Pion_noir("Pn"+str(i), i)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    c = Pion_blanc("Pb"+str(i), i)
    a.modifier(c.position, c)
    L.append(c)
    objet = c.image
    fenetre.blit(objet, c.pos_py)

Rn = Roi_noir()
a.modifier(Rn.position, Rn)
L.append(Rn)
objet = Rn.image
fenetre.blit(objet, Rn.pos_py)

Rb = Roi_blanc()
a.modifier(Rb.position, Rb)
L.append(Rb)
objet = Rb.image
fenetre.blit(objet, Rb.pos_py)

b=Dame_noire()
a.modifier(b.position, b)
L.append(b)
objet = b.image
fenetre.blit(objet, b.pos_py)

b=Dame_blanche()
a.modifier(b.position, b)
L.append(b)
objet = b.image
fenetre.blit(objet, b.pos_py)


for i in range(2):
    b = Tour_noire("Tn"+str(i), i*7)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    b = Tour_blanche("Tb"+str(i), i*7)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    
    b = Cheval_noir("Cn0", 1)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    b = Cheval_noir("Cn1", 6)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    

    b = Cheval_blanc("Cb0", 1)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    b = Cheval_blanc("Cb1", 6)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    
    b = Fou_noir("Fn0", 2)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    b = Fou_noir("Fn1", 5)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    
    b = Fou_blanc("Fb0", 2)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)
    
    b = Fou_blanc("Fb1", 5)
    a.modifier(b.position, b)
    L.append(b)
    objet = b.image
    fenetre.blit(objet, b.pos_py)

jouer = True
joueur = "blanc" #Pour savoir quel joueur joue
test_echec = False #Au d??part personne n'est en ??chec



pygame.display.flip()
for event in pygame.event.get():
    if event.type == QUIT:
        jouer == False
print(a)
while jouer == True:
    test_piece = False #Pour v??rifier que les coordonn??es sont valides
    test_dep = False
    test_value = True
    manger = Manger()
    jeu_en_cours = True

    print("\n")
    print("Le joueur {} joue".format(joueur))
    print("\n")
    
    while test_piece == False:
        piece = input("Piece ?? d??placer: ")
        piece = list(piece)
        piece[0] = int(piece[0])
        piece[1] = int(piece[1])
        test_piece = True
            
            
    test_value = True
    while test_dep == False: 
        dep = input("Deplacement: ")
        dep = list(dep)
        dep[0] = int(dep[0])
        dep[1] = int(dep[1])
        test_dep = True

    #le joueur blanc joue
    while joueur == "blanc" and jeu_en_cours == True:
        objet = a.plateau[piece[0]][piece[1]]
        copie_objet_position = list(objet.position)
        if objet.couleur == "blanc": #on d??place bien un objet blanc
            deplacement(a, dep, piece, manger, objet, L)
        if copie_objet_position != list(objet.position): #On v??rifie qu'on a bien d??plac?? une pi??ce
            joueur = "noir"
        #On v??rifie s'il y a ??chec    
        test_echec = echec_1(a, Rn, Rb, objet, L)
        print(test_echec)
        jeu_en_cours = False
        print(a)

    #Le joueur noir joue
    while joueur == "noir" and jeu_en_cours == True:
        objet = a.plateau[piece[0]][piece[1]]
        copie_objet_position = list(objet.position)
        if objet.couleur == "noir":
            deplacement(a, dep, piece, manger, objet, L)
        if copie_objet_position != list(objet.position):
            joueur = "blanc"
        test_echec = echec_1(a, Rn, Rb, objet, L)
        jeu_en_cours = False
        print(a)
    print(test_echec, joueur)

    """On teste, apr??s avoir jouer, si l'adversaire est en ??chec"""
    if test_echec == True and joueur == "blanc":
        test_bis = roi_en_echec(a, Rb, L)
        print(test_bis)
        if test_bis == True:
            print("??chec et mat")
    elif test_echec == True and joueur == "noir":
        test_bis = roi_en_echec(a, Rn, L)
        print(test_bis)
        if test_bis == True:
            print("??chec et mat")
        print(a)
    
pygame.quit()        
    
