

#Fonction qui permet de rattacher un clic à une case
#La fonction renvoie les coordonnées du point supérieur gauche de la case
def convert_coordonnees(x,y):
    new_x=70*(x//70)
    new_y=70*(y//70)
    return((new_x,new_y))

#Permet de sélectionner dans le plateau la pion sur laquelle l'utilisateur a cliqué
def select_objet(plateau, x, y):
    (x_bis,y_bis)=convert_coordonnees(x,y)
    x_final=int(x_bis/70)
    y_final=int(y_bis/70)
    return(plateau.select(x_final,y_final))

#Permet de choisir la case de déplacement et de déplacer le pion
def move_objet(objet, plateau, x, y):
    (x_bis,y_bis)=convert_coordonnees(x,y)
    coord_initiales = (objet.x, objet.y)
    if objet.type == "Pion" or objet.type == "Dame":
        manger=objet.move(int(x_bis/70), int(y_bis/70), plateau)
    if (objet.x, objet.y)!= coord_initiales:
        print("deplacement")
        return((True, manger)) #On a déplacé le pion
    else:
        print("no deplacement")
        return((False, manger))


#Fonction qu'on appelle après avoir manger un pion
def eat(objet, plateau, x, y):
    (x_bis, y_bis) = convert_coordonnees(x, y)
    if objet.type == "Pion" or objet.type == "Dame":
        manger=objet.manger(int(x_bis/70),int(y_bis/70), plateau)
    return(manger)