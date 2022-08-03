from classe_cellule import *
import re
import random
import os


"""Fonction chargée, une fois le mur cassé, de relier entre-eux
les secteurs qui se touchent"""
"""On distingue 3 cas:
    -Soit les deux cellules ne sont reliés à aucune cellule, dans ce cas
on les relie entre-elles
    -Soit une cellule est relié à d'autre cellule et l'autre pas, dans ce cas
on relie la cellule toute seule au groupoe de cellules qu'on appelle section
    -Soit les deux cellules qui vont être reliées entre-elles appartiennent déjà
à des sections, dans ce cas on fusionne les sections"""

def regroupe_secteur(x, y, laby, position_section):
    a=Section()
    position_secteur=position_section
    if y%2==0:
        if laby[y-1][x].liste=="" and laby[y+1][x].liste=="":
            laby[y-1][x], laby[y+1][x]=a.creer_liste(laby[y-1][x], laby[y+1][x], position_secteur)
            position_secteur+=1

        elif laby[y-1][x].liste!="" and laby[y+1][x].liste!="":
            liste1, liste2=a.fusion_de_secteur(laby[y-1][x], laby[y+1][x])
            for valeur in liste2:
                valeur.liste=liste1[0].liste

        elif laby[y-1][x].liste!="":
            laby[y+1][x]=a.ajouter_cellule_secteur(laby[y-1][x], laby[y+1][x])
            
        elif laby[y+1][x].liste!="":
            laby[y-1][x]=a.ajouter_cellule_secteur(laby[y+1][x], laby[y-1][x])

        else:
            pass

    else:
        if laby[y][x-1].liste=="" and laby[y][x+1].liste=="":
            laby[y][x-1], laby[y][x+1]=a.creer_liste(laby[y][x-1], laby[y][x+1], position_secteur)
            position_secteur+=1


        elif laby[y][x-1].liste!="" and laby[y][x+1].liste!="":
            liste1, liste2=a.fusion_de_secteur(laby[y][x-1], laby[y][x+1])
            for valeur in liste2:
                valeur.liste=liste1[0].liste


        elif laby[y][x-1].liste!="":
            laby[y][x+1]=a.ajouter_cellule_secteur(laby[y][x-1], laby[y][x+1])
            
        elif laby[y][x+1].liste!="":
            laby[y][x-1]=a.ajouter_cellule_secteur(laby[y][x+1], laby[y][x-1])

        else:
            pass

    return(a, position_secteur)

        
                
""" Fonction chargé de générer une grille avec des "O" """
def gen_laby():
    test_dim=False
    while test_dim==False:


#D'abord on récupère les dimensions du labyrinthes

        dim=input("Entrez les dimensions du labyrinthe horinzontalxvertical (ex: 20x5): ")
        expression_dimension=r"^([0-9]+)x([0-9]+)$"
        if re.search(expression_dimension, dim) is None:
            print("Coordonnées invalides")
            
        else:
            longueur, largeur=dim.split("x")
#Car le labyrinthe a un mur entre chaque ligne/colonne, il faut donc l'agrandir
            if int(longueur)<3 or int(largeur)<3:
                print("La taille minimale du labyrinthe est 3x3")
            else:
                test_dim=True
            longueur=int(longueur)*2+1 
            largeur=int(largeur)*2+1
        

#On génère un labyrinthe de ces dimensions composés de cellules numérotées        
    laby=[]
    secteur=0
    liste_coordonnées=[]
    for i in range(largeur):
        laby.append([])
        for j in range(longueur):
            if i%2==0: #A chaque ligne paire on ajoute une ligne de "O"
                laby[i].append("O")

            elif j%2==0:
                laby[i].append("O")

            else:
                cellule=Cellule("C"+str(secteur))
                laby[i].append(cellule) #On créer une cellule aux endroits vides
                secteur+=1

#On regrouope les coordonnées des murs qu'on peut casser pour créer le labyrinthe
    for i in range(largeur):
        for j in range(longueur):
            if i>0 and i<largeur-1 and j>0 and j<longueur-1:
                if j%2==0 and i%2==1:
                    liste_coordonnées.append((j, i))
                elif i%2==0 and j%2==1:
                    liste_coordonnées.append((j, i))
    return(laby, secteur, largeur, longueur, liste_coordonnées)          


"""Convertit une liste de liste en chaine"""
def convertir_liste(liste):
    chaine=''
    for i, valeur1 in enumerate(liste):
        for j, valeur2 in enumerate(liste[i]):
            if type(valeur2) is not str():
                valeur2=str(valeur2)
            chaine+=valeur2
            if j==len(liste[i])-1 and i!=len(liste)-1:
                chaine+='\n'
    return(chaine)


""" Fonction chargé de créer une sortie dans le labyrinthe"""
def creer_sortie(largeur, longueur, laby):
    position_sortie=False
    while position_sortie==False:        
        cote_sortie=random.randrange(4) #En fonction du nombre on choisi le côté de la sortie

        if cote_sortie==0: #La sortie est en haut
            x=random.randrange(1, longueur)
            if laby[1][x]==" ":
                laby[0][x]="U"
                position_sortie=True

        elif cote_sortie==1: #La sortie est en bas
            x=random.randrange(1, longueur)
            if laby[largeur-2][x]==" ":
                laby[largeur-1][x]="U"
                position_sortie=True
            
        elif cote_sortie==2: #La sortie est à gauche
            x=random.randrange(1, largeur)
            if laby[x][1]==" ":
                laby[x][0]="U"
                position_sortie=True
            
        else: #La sortie est à droite
            x=random.randrange(1, largeur)
            if laby[x][longueur-2]==" ":
                laby[x][longueur-1]="U"
                position_sortie=True
            

    return(laby, cote_sortie, x)


"""Fonction chargée de placer le robot dans le coin opposer de là où est la sortie
du labyrinthe"""
def place_robot(cote_sortie, position_sortie, largeur, longueur, laby):
#Pour se simplifier la vie, on opère par symétrie
    if cote_sortie==1:
        cote_sortie=0
        largeur=3

    elif cote_sortie==3:
        cote_sortie=2
        longueur=3

    sortie_robot=True
    position_robot=False
    while position_robot==False:

        if cote_sortie==0 and position_sortie<=longueur/2:
            y=random.randrange(int(longueur/2)+1, longueur-1)
            if laby[largeur-2][y]==" ":
                laby[largeur-2][y]="X"
                position_robot=True
                

        elif cote_sortie==0 and position_sortie>longueur/2:
            y=random.randrange(1, int(longueur/2))
            if laby[largeur-2][y]==" ":
                laby[largeur-2][y]="X"
                position_robot=True

        elif cote_sortie==2 and position_sortie<=largeur/2:
            y=random.randrange(int(largeur/2)+1, largeur-1)
            if laby[y][longueur-2]==" ":
                laby[y][longueur-2]="X"
                position_robot=True

        elif cote_sortie==2 and position_sortie>largeur/2:
            y=random.randrange(1, int(largeur/2))
            if laby[y][longueur-2]==" ":
                laby[y][longueur-2]="X"
                position_robot=True
            
        else:
            sortie_robot=False
            position_robot=True

        return(laby, sortie_robot)


"""Fonction charger d'enregistrer le labyrinthe et son nom"""
def save(laby):
    liste_nom_carte=[]

    print("")
    save_lab=input("Voulez-vous sauvegarder le labyrinthe généré (o/n): ")
    if save_lab!="o".lower() and save_lab!="n".lower():
        return(save(laby))

    
    elif save_lab=="o".lower():
        os.chdir("..\\Tuto pygame labyrinthe")
        print("")
        print("""Choisissez un nom qui ne soit pas dans la liste suivante, s'il est dedans\nle labyrinthe existant sera supprimé:""")
        
        for nom_fichier in os.listdir("cartes"):
            if nom_fichier.endswith(".txt"):
                chemin = os.path.join("cartes", nom_fichier)
                nom_carte = nom_fichier[:-4].lower()
                liste_nom_carte.append(nom_carte)
                print(nom_carte)
                

        nom_choisi = False
        while nom_choisi == False:
            print("")
            nom_carte=input("Nom de votre carte: ")
            
            if nom_carte in liste_nom_carte:
                supprimer=False
                while supprimer==False:
                    print("")
                    supp=input("""Etes-vous sur de vouloir supprimer la carte "{}" (o/n): """.format(nom_carte))
                    if supp=="n".lower():
                        supprimer=True
                    elif supp=="o".lower():
                        supprimer=True
                        nom_choisi=True
                        os.chdir("C:\\Users\\simon\\Desktop\\Tout\\Python\\Tuto pygame labyrinthe\\cartes")
                        fichier_saves=open("{}.txt".format(nom_carte), "w")
                        fichier_saves.write(laby)
                        fichier_saves.close()
                    else:
                        print("")
                        print("Vous n'avez pas indiqué correctement ce que vous voulez faire")
            else:                    
                nom_choisi=True
                os.chdir("C:\\Users\\simon\\Desktop\\Tout\\Python\\Tuto pygame labyrinthe\\cartes")
                fichier_saves=open("{}.txt".format(nom_carte), "w")
                fichier_saves.write(laby)
                fichier_saves.close()
    else:
        return("Labyrinthe supprimé")
    return("Labyrinthe sauvegardé!")


"""Fonction chargée de casser un mur, renvoie la position du mur casse"""
def casse_mur(liste_coordonnées):
#Coordonnées du mur qu'on enlève
        i=random.randrange(len(liste_coordonnées))
        (x, y)=liste_coordonnées[i]
        del liste_coordonnées[i]
        return(x, y, liste_coordonnées)
