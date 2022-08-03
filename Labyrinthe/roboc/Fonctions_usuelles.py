# -*-coding:Utf-8 -*


"""Ce module contient plusieurs fonctions indispensables
au fonctionnement du labyrinthe"""
"""Toutes sauf la prmeière servent à gérer les sauvegardes"""


import os
import pickle


#Permet de convertir la liste contenant le labyrinthe en chaine de caractères pour pouvoir l'afficher ensuite
def convertir_liste(liste):
    chaine=''
    for i, valeur1 in enumerate(liste):
        for j, valeur2 in enumerate(liste[i]):
            chaine+=valeur2
            if j==len(liste[i])-1 and i!=len(liste)-1:
                chaine+='\n'
    return(chaine)



#On récupère les données des sauvegardes
def création_fichier_joueur():

#Pour savoir si une partie existe où non et le labyrinthe correspondant
    if os.path.exists("saves_noms_joueurs.txt"): # Le fichier existe
        # On le récupère
        fichier_saves = open("saves_noms_joueurs.txt", "rb")
        mon_depickler = pickle.Unpickler(fichier_saves)
        noms_joueurs = mon_depickler.load()
        fichier_saves.close()
    else: # Le fichier n'existe pas
        noms_joueurs = {}
        fichier_saves = open("saves_noms_joueurs.txt", "wb")
        mon_pickler = pickle.Pickler(fichier_saves)
        mon_pickler.dump(noms_joueurs)
        fichier_saves.close()

#Pour la position du robot        
    if os.path.exists("saves_position.txt"): # Le fichier existe
        # On le récupère
        fichier_saves = open("saves_position.txt", "rb")
        mon_depickler = pickle.Unpickler(fichier_saves)
        position = mon_depickler.load()
        fichier_saves.close()
    else: # Le fichier n'existe pas
        position = {}
        fichier_saves = open("saves_position.txt", "wb")
        mon_pickler = pickle.Pickler(fichier_saves)
        mon_pickler.dump(position)
        fichier_saves.close()

    return(noms_joueurs, position)


#Permet de savoir si on a déjà jouer à ce labyrinthe avec ce pseudo ou pas
def test_pseudo(pseudo, noms_joueurs, nom_carte):
    for cle in noms_joueurs.keys():
        if cle[:-len(nom_carte)]==pseudo and cle[len(pseudo):]==nom_carte:
            return(True)
    return(False)



    

#Enregistre les données du jeu pour le recommencer, c'est-à-dire le labyrinthe du joueur
#ainsi que la position du robot et celle qu'il occupait juste avant
def enregistrer_saves(pseudo, nom_carte, labyrinthe, noms_joueurs, nouvelle_position_robot , ancienne_position_robot, position):

#On sauvegarde le labyrinthe du joueur
    noms_joueurs[pseudo+nom_carte]=labyrinthe
    fichier_saves = open("saves_noms_joueurs.txt", "wb") # On écrase les anciennes sauvegardes concernant la forme du labyritnhe
    mon_pickler = pickle.Pickler(fichier_saves)
    mon_pickler.dump(noms_joueurs)
    fichier_saves.close()
    
#On sauvegarde la position du robot
    position[pseudo+nom_carte]=(nouvelle_position_robot, ancienne_position_robot, position)
    fichier_saves_position=open("saves_position.txt","wb")
    mon_pickler = pickle.Pickler(fichier_saves_position)
    mon_pickler.dump(position)
    fichier_saves_position.close()



"""Fonction chargée d'effacer le labyrinthe"""
def supprimer_laby(pseudo, nom_carte, labyrinthe, noms_joueurs, nouvelle_position_robot , ancienne_position_robot, position):
    #On supprime le labyrinthe du joueur et le joueur
    del noms_joueurs[pseudo+nom_carte]
    fichier_saves = open("saves_noms_joueurs.txt", "wb") # On écrase les anciennes sauvegardes concernant la forme du labyritnhe
    mon_pickler = pickle.Pickler(fichier_saves)
    mon_pickler.dump(noms_joueurs)
    fichier_saves.close()
    
#On supprime la position du robot
    del position[pseudo+nom_carte]
    fichier_saves_position=open("saves_position.txt","wb")
    mon_pickler = pickle.Pickler(fichier_saves_position)
    mon_pickler.dump(position)
    fichier_saves_position.close()


    




"""Petite fonction chargée de vérifier si la direction entrée est valide:
    -Si c'est le cas on renvoie vérification_direction=True
    -Sinon on renvoie une erreur"""

def test_direction(direction):       
        vérification_destination=False
        vérification_entier=False
        try:
            i=direction[0]
            assert i=='s'.lower() or i=='z'.lower() or i=='q'.lower() or i=='d'.lower() or i=='e'.lower()
        except AssertionError:
            return("Vous n'avez pas entré 's', 'z', 'q', 'd' ou 'q' au début de la direction",0,0)
        except IndexError:
                return("Vous n'avez rien entré",0,0)
        else:
            vérification_direction=True
        if vérification_direction==True and i!="e".lower():
            try:
                direction[1]
            except IndexError:
                return("Vous n'avez pas indiqué de combien de cases vous souhaitez vous déplacer",0,0)
            nb_cases_déplacement=[]
            for j in range(1, len(direction)):
                try:
                    direction[j]==int(direction[j])
                except ValueError:
                    return("Vous n'avez pas indiqué de combien de cases vous souhaitez vous déplacer",0,0)
                else:
                     nb_cases_déplacement.append(int(direction[j])) #A partir d'ici on essaie d'extraire le nombre de cases sur lesquels on se déplace
            cases_déplacement=0    
            for i, valeurs in enumerate(nb_cases_déplacement):
                    cases_déplacement+=valeurs*10**(len(nb_cases_déplacement)-(i+1))
        elif i=="e".lower():
            cases_déplacement=0
        return(True,cases_déplacement, direction[0])
        


        
    
        

        
