"""Fonction qui converti une chaine de caractères représentant
un labyrinthe rectangulaire encadré par des 'O' en une liste de liste"""

"""On la met à part car elle est plus longue que les autres et plus complexe"""


import os


#On ouvre le dossier contenant les cartes et on récupère les cartes
cartes = {}
nom_cartes={}
i=1
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-4].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
        cartes[nom_carte]=contenu #Dictionnaire des cartes avec en clé le nom du fichier texte
        nom_cartes[i]=nom_carte #Dictionnaire des cartes avec en clé leur numéro
        i+=1


#On a récupérer les cartes, maintenant on converti celle qui nous intéresse
def laby(chaîne):
    largeur_labyrinthe=0
    hauteur_labyrinthe=1
    grille=[]


#Première étape: On détermine la largeur du labyrinthe    
    i=chaîne[largeur_labyrinthe]
    while i!='\n':
        largeur_labyrinthe+=1
        i=chaîne[largeur_labyrinthe]
    largeur_labyrinthe+=1 #On compte le saut de ligne dans la largeur du labyrinthe

#On vérifie ensuite si le labyrinthe est bien proportionné et délimité sur les côtés
    compteur_largeur=1
    compteur_hauteur=0
    
    for i in chaîne:
        if i!='\n':
            compteur_largeur+=1
        else:
            if compteur_largeur!=largeur_labyrinthe:
                return("Les lignes du labyrinthe ne font pas toutes la même taille")
            elif (chaîne[compteur_hauteur*largeur_labyrinthe]!='O' and chaîne[compteur_hauteur*largeur_labyrinthe]!='U') or (chaîne[(compteur_hauteur+1)*largeur_labyrinthe-2]!='O' and chaîne[(compteur_hauteur+1)*largeur_labyrinthe-2]!='U'):
                return("Il manque un 'O' ou un 'U' sur les bords")
            else:
                compteur_largeur=1
                compteur_hauteur+=1


#On s'intéresse aux bords horinzontaux maintenant
#On calcule d'abord la hauteur du labyrinthe
    for i in chaîne:
        if i=='\n':
            hauteur_labyrinthe+=1

#On regarde ensuite si le labyrinthe est bien proportionné et délimité à l'horizontal
    ligne_1=0
    ligne_n=0
    while ligne_1<largeur_labyrinthe-1:
        if chaîne[ligne_1]!='O' and chaîne[ligne_1]!='U':
            return("Il manque un (ou plusieurs) 'O' ou 'U' sur le haut du laybrinthe ou alors les colonnes ne font pas toutes la même taille")
        ligne_1+=1
    for i in range((hauteur_labyrinthe-1)*largeur_labyrinthe, len(chaîne)):
        if len(chaîne)-(hauteur_labyrinthe-1)*largeur_labyrinthe!=largeur_labyrinthe-1:
            return("Il n'y a pas le bon nombre de caractères sur la dernière ligne")
        if chaîne[i]!='O' and chaîne[i]!='U':
            return("Il manque un (ou plusieurs) 'O' ou 'U' sur le bas du laybrinthe")
        ligne_n+=1



#On va ensuite chercher à représenter le labyrinthe sous une forme de liste de liste (ligne/colonne) débarassé des '\n'                            
    for i in range(hauteur_labyrinthe):
        grille.append([])

        for j in range(largeur_labyrinthe):
#La chaîne fait largeur_caractère de large le dernier étant '\n'
            
            if i!=hauteur_labyrinthe-1:
                if chaîne[j+i*largeur_labyrinthe]!='\n':
#On ajoute pas le saut de ligne à notre grille
                    
                    grille[i].append(chaîne[j+i*largeur_labyrinthe])

#On doit procéder différemment sur la dernière ligne qui ne fait que largeur_caractère-1 caractères
#En effet, on a pas de saut de ligne, pas de '\n'
            else:
                if j!=largeur_labyrinthe-1:
                    grille[i].append(chaîne[j+i*largeur_labyrinthe])


#On cherche la position du robot
    nb_robot=0                
    for i,valeur1 in enumerate(grille):
        for j, valeur2 in enumerate(grille[i]):
            if valeur2=='X':
                nb_robot+=1
                position_robot=(i,j)
    if nb_robot==0:
        return("Il n'y a pas de robot dans ce labyrinthe")
    elif nb_robot>1:
        return("Il y a trop de robot dans ce labyrinthe")
    else:
        return(grille,largeur_labyrinthe-1,hauteur_labyrinthe,position_robot)
        
