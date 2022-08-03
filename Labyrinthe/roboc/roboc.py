# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

print("""La partie commence. Dirigez-vous:
    -Vers le bas avec " s "
    -Vers le haut avec " z "
    -Vers la droite avec " d "
    -Vers la gauche avec " q "
Vous pouvez aussi vous dirigez de plusieurs cases d'un côtés, par exemple 's2'
pour vous déplacez de deux cases vers le bas.
-O représente les murs du labyrinthe, ce sont des obstacles
-X vous représente vous, le robot
-. représente les portes que vous pouvez traverser
-U représente la (ou les) sortie(s)

Taper "E" pour quitter le labyrinthe

Vous pouvez aussi créer vos propres cartes. Pour en savoir plus, reportez-vous
au fichier READ-ME.
""")


import os

from Fonctions_usuelles import *
from Fonction_laby import laby





# On charge les cartes existantes
cartes = {}
nom_cartes={}
nb_laby=1
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-4].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
        cartes[nom_carte]=contenu
        nom_cartes[nb_laby]=nom_carte
        nb_laby+=1




#On demande au joueur son pseudo et on ouvre le fichier contenant la liste des joueurs
pseudo_invalide=True
while pseudo_invalide==True:
    pseudo= input("Quel est votre pseudo: ")
    try:
        assert len(pseudo)!=0
    except AssertionError:
        print("Vous n'avez pas entré de pseudo")
    else:
        pseudo_invalide=False
liste_pseudo=création_fichier_joueur()[0]
coordonnées_robot=création_fichier_joueur()[1]


        
#On commence la partie
continuer_partie=True
while continuer_partie==True:
    # On affiche les cartes existantes
    print("Labyrinthes existants :")
    for cle, valeurs in nom_cartes.items():
        print("  {} - {}".format(cle, valeurs))




    #On extrait le labyrinthe à partir d'un numéro entré par l'utilisateur
    choix=False
    while choix==False:
        choix_de_la_carte=input("Entrez un numéro de labyrinthe pour commencer à jouer: ")
        try:
            choix_de_la_carte=int(choix_de_la_carte)
            assert choix_de_la_carte>0 and choix_de_la_carte<nb_laby
            choix=True
        except ValueError:
            print("Vous n'avez pas entrer un numéro")
        except AssertionError:
            print("Le numéro entré ne correspond à aucun labyrinthe")
    nom_carte=nom_cartes[choix_de_la_carte]




    #On récupère le labyrinthe, ses dimensions et la position du robot
    labyrinthe=laby(cartes[nom_carte])[0]
    nb_colonne=laby(cartes[nom_carte])[1]
    nb_ligne=laby(cartes[nom_carte])[2]
    position_robot=list(laby(cartes[nom_carte])[3]) #D'abord le numéro de ligne puis de colonne
    print("")



#On regarde si le joueur a déjà joué au labyrinthe
    test=0
    if test_pseudo(pseudo, liste_pseudo, nom_carte)==True:
            test=1
            labyrinthe[position_robot[0]][position_robot[1]]=' '
            position_robot=[coordonnées_robot[pseudo+nom_carte][0][0],coordonnées_robot[pseudo+nom_carte][0][1]]
            nouvelle_position_robot=coordonnées_robot[pseudo+nom_carte][0]

    else:
        nouvelle_position_robot=[position_robot[0], position_robot[1], labyrinthe[position_robot[0]][position_robot[1]]]
    
    if test_pseudo(pseudo, liste_pseudo, nom_carte)==False:
        liste_pseudo[pseudo+nom_carte]=labyrinthe
    print(convertir_liste(liste_pseudo[pseudo+nom_carte]))
    print("")




    #On détermine et on affiche les déplacements de l'utilisateur...
    test_continuer_a_jouer=False
    fin_partie=False
    while fin_partie==False:

    #On vérifie d'abord que la direction entrée est valide
        testdirection=False
        while testdirection!=True:
            direction=input("Choix de la direction: ")        
            testdirection=test_direction(direction)[0]
            nb_cases=test_direction(direction)[1]
            orientation=test_direction(direction)[2]
            if testdirection!=True:
                print(testdirection)

        if test_pseudo(pseudo, liste_pseudo, nom_carte)==True and test==1:
            test=0
            ancienne_position_robot=coordonnées_robot[pseudo+nom_carte][1]
        else:
            ancienne_position_robot=nouvelle_position_robot #On sauvegarde la position que le robot a avant de le déplacer
        
    #On actualise la position du robot en vérifiant qu'il ne se déplace pas sur un 'O', sinon on le recule d'une case
        if orientation=='s'.lower():
            i=0
            while labyrinthe[position_robot[0]+i][position_robot[1]]!='O' and labyrinthe[position_robot[0]+i][position_robot[1]]!='U' and i<=nb_cases:
                i+=1
            if i==nb_cases and labyrinthe[position_robot[0]+i][position_robot[1]]!='O':
                position_robot[0]+=nb_cases
            elif labyrinthe[position_robot[0]+i][position_robot[1]]=='U':
                position_robot[0]+=i
            else:
                position_robot[0]+=i-1
        if orientation=='z'.lower():
            i=0
            while labyrinthe[position_robot[0]-i][position_robot[1]]!='O' and labyrinthe[position_robot[0]-i][position_robot[1]]!='U' and i<=nb_cases:
                i+=1
            if i==nb_cases and labyrinthe[position_robot[0]-i][position_robot[1]]!='O':
                position_robot[0]-=nb_cases
            elif labyrinthe[position_robot[0]-i][position_robot[1]]=='U':
                position_robot[0]-=i
            else:
                position_robot[0]-=i-1
        if orientation=='q'.lower():
            i=0
            while labyrinthe[position_robot[0]][position_robot[1]-i]!='O' and labyrinthe[position_robot[0]][position_robot[1]-i]!='U' and i<=nb_cases:
                i+=1
            if i==nb_cases and labyrinthe[position_robot[0]][position_robot[1]-i]!='O':
                position_robot[1]-=nb_cases
            elif labyrinthe[position_robot[0]][position_robot[1]-i]=='U':
                position_robot[1]-=i
            else:
                position_robot[1]-=i-1
        if orientation=='d'.lower():
            i=0
            while labyrinthe[position_robot[0]][position_robot[1]+i]!='O' and labyrinthe[position_robot[0]][position_robot[1]+i]!='U' and i<=nb_cases:
                i+=1
            if i==nb_cases and labyrinthe[position_robot[0]][position_robot[1]+i]!='O':
                position_robot[1]+=nb_cases
            elif labyrinthe[position_robot[0]][position_robot[1]+i]=='U':
                position_robot[1]+=i
            else:
                position_robot[1]+=i-1

        if orientation=='e'.lower():
            print("A bientôt!")
            test_continuer_a_jouer=True
            continuer_partie=False
            test_continuer_a_jouer=True
            break


    #On déplace le robot
        nouvelle_position_robot=[position_robot[0], position_robot[1], labyrinthe[position_robot[0]][position_robot[1]]] #on sauvegarde la position que le robot va prendre
        if ancienne_position_robot[2]=='X':
            labyrinthe[ancienne_position_robot[0]][ancienne_position_robot[1]]=' ' #On prend soin de remplacer la position initiale par du vide (' ')
        else:
            labyrinthe[ancienne_position_robot[0]][ancienne_position_robot[1]]=ancienne_position_robot[2]
        if labyrinthe[position_robot[0]][position_robot[1]]=='U':
            fin_partie=True
            labyrinthe[position_robot[0]][position_robot[1]]='X'
        else:
            labyrinthe[position_robot[0]][position_robot[1]]='X'

        enregistrer_saves(pseudo, nom_carte, labyrinthe, liste_pseudo,nouvelle_position_robot, ancienne_position_robot, coordonnées_robot)
        ancienne_position_robot=nouvelle_position_robot
        print(convertir_liste(liste_pseudo[pseudo+nom_carte]))
        print("")


    if orientation!="e".lower():
        print("Félicitations! Vous avez gagné!!")
        print("")
        supprimer_laby(pseudo, nom_carte, labyrinthe, liste_pseudo,nouvelle_position_robot, ancienne_position_robot, coordonnées_robot)
    
        
        


    
#On demande au joueur s'il veut continuer à jouer
    while test_continuer_a_jouer==False:
        continuer_a_jouer=input("Voulez-vous faire une autre partie (o/n): ")
        if continuer_a_jouer=='n' or continuer_a_jouer=='N':
            continuer_partie=False
            test_continuer_a_jouer=True
            print("A bientôt!")
        elif continuer_a_jouer=='o' or continuer_a_jouer=='o':
            test_continuer_a_jouer=True
        else:
            print("Vous n'avez pas indiqué correctement si vous souhaitez continuer à jouer ou non")



