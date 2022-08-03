# -*- coding:utf8 -*

from functions import *
from mes_class import *
import os

''' initialisation de variable'''
jouer = True
player = class_joueur()
list_sav = list()

print ('*'*10,'JEUX DU LABYRINTHE','*'*10,'\n')

# recherche du fichier de sauvegarde, si il n'existe pas il est créé
data_folder = os.listdir()
if 'sav.txt' not in data_folder :
    with open (r'sav.txt','w',encoding='utf8') as data_sav :
        data_sav.close()

#ouverture du fichier de sauvegarde et récupération des données du joueur
with open(r'sav.txt','r',encoding='utf8') as f :
    data_sav = f.read()
    f.close()
    '''
    si aucun joueur n'existe on en creer un nouveau
    sinon on récupère la liste des joueurs existants
    '''
    if data_sav == '' :
        pseudo = input("Aucun joueur n'a été trouvé. Veuillez indiquer votre pseudo : ")
        player = class_joueur(pseudo)
    else :
        list_niv1 = data_sav.split('\n')
        list_sav = [i.split(';') for i in list_niv1]
        list_joueur = [class_joueur(*i) for i in list_sav]

#Choix du joueur : creer un nouveau joueur ou reprendre une partie        
while True :
    if player.pseudo != "":
        break
    choix1 = input('Voulez vous :\n1 - Créer un nouveau joueur\n2 - Reprendre une partie en cours\nChoix : ')
    if choix1 == '1' :
        pseudo = input("Veuillez indiquer votre pseudo : ")
        player = class_joueur(pseudo)
        break
    elif choix1 == '2':
        print('Choisisez votre joueur :\n')
        for i in list_joueur :
              print (f'{i.pseudo} : {i.score} points')
        choix2 = input('\nQuel est votre joueur ? : ')
        try :
            player = [i for i in list_joueur if i.pseudo == choix2]
            player = player [0]
            break
        except IndexError :
            print("le choix rentré n'est pas valide\n")
    else :
        print("le choix rentré n'est pas valide\n")

#début de la partie
while jouer == True :
    '''
        on regarde si le joueur à une partie sur une carte en cours
        Si non on lance la fonction de récupération des cartes existantes pour en proposer une nouvelle
        Si oui on récupère la carte sauvegardée dans le fichier de sauvegarde
    '''
    if player.carte_en_cour == "" :
        player.carte_en_cour = recup_carte()
    else :
        player.carte_en_cour = player.carte_en_cour.split('/')

        for x, y in enumerate(player.carte_en_cour):
            player.carte_en_cour[x] = y.split('-')
    '''
        on affiche maintenant la carte en cours
        on récupère la position du joueur sur la carte
        on lance la fonction de déplacement    
    '''
    affiche_carte(player.carte_en_cour)
    posit = position_X(player.carte_en_cour)
    data_game = deplacement(player.carte_en_cour, posit, player.score)

    '''
    on récupère les données de la partie pour les placer dans notre variable player de classe class_joueur
    '''
    player.score = data_game[1]
    player.carte_en_cour = data_game[0]

    '''
    on propose au joueur d'effectuer une nouvelle partie
    '''
    while True :
        jeux = input('Voulez vous refaire une patie ? O/N : ').upper()
        if jeux == 'O' :
            jouer = True
            break
        elif jeux == 'N':
            jouer = False
            break
        else :
            print (f"la valeur {jeux} n'est pas valide")

#sauvegarde de la partie
'''
on vérifie d'être dans le bon dossier pour effectuer la sauvegarde
'''
if os.getcwd()[-6:]== 'cartes':
        os.chdir("..")
with open(r'sav.txt', 'w', encoding='utf8') as fs :
    
    '''
    Convertion de la carte en format str pour enregistrement
    enregistrement de une des données player dans une liste pour préparer la sauvegarde 
    '''
    carte_format_sav = "/".join(["-".join(x) for x in player.carte_en_cour])
    joueur = [player.pseudo,str(player.score), carte_format_sav]
    joueur_existe = False
    '''
    si aucun joueur n'existe on écrit directement dans le fichier
    si une sauvegarde existe déja avec le nom du joueur on la remplace
    sinon on rajoute le joueur à la suite du fichier
    '''
    if list_sav == [] :
        newdata = ';'.join(joueur)
        fs.write(newdata)
    else :
        for x,y in enumerate(list_sav):
            if joueur[0] in y :
                    list_sav[x] = joueur
                    joueur_existe = True
        if joueur_existe == False :
            list_sav.append(joueur)
        list_sav2=[";".join(x) for x in list_sav]
        newdata = '\n'.join(list_sav2)
        fs.write(newdata)
print('Fin de la partie')
