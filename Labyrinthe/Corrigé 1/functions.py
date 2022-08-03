# -*-coding:UTF8-*

import os

def recup_carte():
    # fonction chargée de demander le choix de la carte et de renvoyer la carte choisie
    dico_carte = dict() #création du dictionnaire qui contiendra les cartes
    list_carte_final = list() #Liste finale contenant la carte sur deux niveaux
    
    if os.getcwd()[-6:]!= 'cartes':
        os.chdir("cartes")
    liste_carte = os.listdir(".")#lecture du contenu du dossier carte


    #enregistrement des cartes dans le dictionnaire dico_carte
    for num_carte, carte_y in enumerate(liste_carte) :
        dico_carte[str(num_carte)] = carte_y

    print('Veuillez choisir votre carte :\n')

    #affichage et récupération du choix des cartes
    for num_carte in dico_carte: 
        print("{} - {}".format(num_carte, dico_carte[num_carte]))
              
    choix=input('\nEntrez le numéro de la carte désirée : \n')

    #ouverture de la carte choisie
    if choix in dico_carte.keys(): 
        choix_carte = open(dico_carte[choix],'r')
        carte = choix_carte.read()
        choix_carte.close()
    else :
        print('la valeur entrée ne correspond à aucune carte')
        return False
    
    # transformation de la carte choisie sous forme d'une liste à deux niveaux
    n1_carte=carte.split("\n")
    for x in n1_carte :
        n2_carte=[]
        for y in x :
            n2_carte.append(y)
        list_carte_final.append(n2_carte)
    return list_carte_final

def affiche_carte(carte):
    # fonction chargée de l'affichage de la carte
    # on rassemble la liste sous un str affichable
    carte_list =list()
    for x in carte :
        ligne=''.join(x)
        carte_list.append(ligne)
    carte_affiche = "\n".join(carte_list)
    print('\n{}\n'.format(carte_affiche))

def position_X (carte):
    #fonction qui récupère la position du joueur sur la carte
    position = list()
    for x, y in enumerate(carte):
        if 'X' in y :
            position = [x,y.index('X')]
    return position

def deplacement(carte, posit, score):
    #fonction charger d'effectuer les déplacements du joueur sur la carte
    jouer = True
    porte = False
    sortie = False
    score_partie = int(score)
    largeur_carte = len(carte[0])-1
    hauteur_carte = len(carte)-1
    while jouer == True :
        mouv = input('''\nOu voulez voulez aller ? ('A' pour l'aide)
\nChoix : ''').upper()
        if mouv == 'Q' :
            jouer = False
            return carte, score_partie
        elif mouv =='A' :
            print ('''\nN, S, E, O pour haut, bas, droite, gauche
Puis un nombre pour le nombre de case\n
Ex : 'N3' pour trois case en haut\n
Q pour quitter''')
        else :
            dep = [mouv[0],int(mouv[1:])]
            while dep[1]>0 and sortie == False :

                #déplacement au nord
                if dep[0] == 'N' :
                    if posit[0] > 0 and carte[posit[0]-1][posit[1]] != 'O':
                        #si on se trouvait sur une porte on referme la porte
                        if porte == True :
                            carte[posit[0]][posit[1]] = '.'
                            porte = False
                        else :
                            carte[posit[0]][posit[1]] = ' '
                        #si on vas sur une porte on ouvre la porte    
                        if carte[posit[0]-1][posit[1]] == '.' :
                            porte = True
                        elif carte[posit[0]+1][posit[1]] == 'U' :
                            sortie = True
                        carte[posit[0]-1][posit[1]] = 'X'
                        dep[1] -= 1
                        affiche_carte(carte)
                        posit=position_X(carte)
                      
                    else :
                        # le déplacement est impossible, on place donc le nombre de déplacement restant à 0
                        dep[1]=0
                        print('déplacement impossible')
                        
                #déplacement au sud
                if dep[0] == 'S' :
                    if posit[0] < hauteur_carte and carte[posit[0]+1][posit[1]] != 'O':
                        #si on se trouvait sur une porte on referme la porte
                        if porte == True :
                            carte[posit[0]][posit[1]] = '.'
                            porte = False
                        else :
                            carte[posit[0]][posit[1]] = ' '
                        #si on vas sur une porte on ouvre la porte    
                        if carte[posit[0]+1][posit[1]] == '.' :
                            porte = True
                        elif carte[posit[0]+1][posit[1]] == 'U' :
                            sortie = True
                        carte[posit[0]+1][posit[1]] = 'X'
                        dep[1] -= 1
                        affiche_carte(carte)
                        posit=position_X(carte)
                     
                    else :
                        dep[1]=0
                        print('déplacement impossible')
                       
                #déplacement vers l'est
                if dep[0] == 'E' :
                    if posit[1] < largeur_carte and carte[posit[0]][posit[1]+1] != 'O' :
                        #si on se trouvait sur une porte on referme la porte
                        if porte == True :
                            carte[posit[0]][posit[1]] = '.'
                            porte = False
                        else :
                            carte[posit[0]][posit[1]] = ' '
                        #si on vas sur une porte on ouvre la porte    
                        if carte[posit[0]][posit[1]+1] == '.' :
                            porte = True
                        elif carte[posit[0]][posit[1]+1] == 'U' :
                            sortie = True
                        carte[posit[0]][posit[1]+1] = 'X'
                        dep[1] -= 1
                        affiche_carte(carte)
                        posit=position_X(carte)
                     
                    else :
                        dep[1]=0
                        print('déplacement impossible')

                #déplacement vers l'ouest    
                if dep[0] == 'O' :
                    if posit[1] > 0 and carte[posit[0]][posit[1]-1] != 'O' :
                        #si on se trouvait sur une porte on referme la porte
                        if porte == True :
                            carte[posit[0]][posit[1]] = '.'
                            porte = False
                        else :
                            carte[posit[0]][posit[1]] = ' '
                        #si on vas sur une porte on ouvre la porte    
                        if carte[posit[0]][posit[1]-1] == '.' :
                            porte = True
                        elif carte[posit[0]][posit[1]-1] == 'U' :
                            sortie = True
                        carte[posit[0]][posit[1]-1] = 'X'
                        dep[1] -= 1
                        affiche_carte(carte)
                        posit=position_X(carte)
                     
                    else :
                        dep[1]=0
                        print('déplacement impossible')

            if sortie == True :
                print('félicitation vous êtes sortie du labyrinthe')
                carte = ""
                score_partie += 5
                return carte, score_partie
