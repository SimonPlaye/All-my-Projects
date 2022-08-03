# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

from carte import *
from labyrinthe import *

cartes = Carte()
cartes.trouver_cartes()
labyrinthe_jeu = Labyrinthe(cartes.choisir_carte())

while True:
    commande_utilisateur=input(">")
    if commande_utilisateur[0]=="Q":
        quit()
    elif len(commande_utilisateur) == 1:
        labyrinthe_jeu.deplacer_robot(commande_utilisateur, 1)
    else :
        labyrinthe_jeu.deplacer_robot(commande_utilisateur[0], int(commande_utilisateur[1:]))
    print(labyrinthe_jeu)
    cartes.sauvegarder(labyrinthe_jeu)
    print()
