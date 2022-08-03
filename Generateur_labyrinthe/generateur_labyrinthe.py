"Ce programme est un générateur de labyrinthe"

from classe_cellule import Cellule
from fonctions_usuelles import *



#On génère le labyrinthe
laby_gen=False
(laby, nb_secteur, largeur, longueur, liste_coordonnées)=gen_laby()
laby=list(laby)

    
position_section=0
while laby_gen==False:
    mur_enleve=False
    
    while mur_enleve==False:
#D'abord, on enlève un mur quelque part, à l'intérieur des limites:
        x, y, liste_coordonnées=casse_mur(liste_coordonnées)

#On si le mur cassé est sur une ligne, on relie les deux cases en-dessous/au-dessus
#Sinon, on relie les deux cases avant/après
#On ne veut pas casser un mur séparant deux cellules de même section
        if y%2==0 and (laby[y-1][x].liste!=laby[y+1][x].liste or laby[y-1][x].liste==laby[y+1][x].liste==""):
            mur_enleve=True
            laby[y][x]=" "
            a, position_secteur=regroupe_secteur(x, y, laby, position_section)

        elif y%2==1 and (laby[y][x-1].liste!=laby[y][x+1].liste or laby[y][x-1].liste==laby[y][x+1].liste==""):
            mur_enleve=True
            laby[y][x]=" "
            a, position_secteur=regroupe_secteur(x, y, laby, position_section)

        else:
            pass
    position_section=position_secteur

#On stop lorsque toutes les cellules ont été relié entre-elles donc sont dans la
#même sous-liste
    if len(a.secteur[0])==nb_secteur:
        laby_gen=True

#On remplace les cellule par des espaces vides
for i, val1 in enumerate(laby):
    for j, val2 in enumerate(laby[i]):
        if val2!="O" and val2!=" ":
            laby[i][j]=" "


#On créé le robot et sa sortie dans le labyrinthe
#C'est une boucle : au cas où on ne puisse pas positionner le robot à l'opposer
#de la sortie du fait de la représentation du labyrinthe alors on répète la boucle
sortie_robot=False
while sortie_robot==False:
    laby, cote_sortie, position_sortie=creer_sortie(largeur, longueur, laby)
    laby, sortie_robot=place_robot(cote_sortie, position_sortie, largeur, longueur, laby)
    
laby_fini=convertir_liste(laby)
print(laby_fini)


#Maintenant on décide si on enregistre le labyrinthe
a=save(laby_fini)
print(a)

    
