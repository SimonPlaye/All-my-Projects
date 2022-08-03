"""Classe contenant chaque cellule du labyrinthe"""



class Cellule:

    def __init__(self, nom, liste=""):
        self.liste=liste
        self.nom=nom

    def __repr__(self):
        return("{}".format(self.nom))

    
"""Classe regroupant les cellules qui ne sont plus séparées par un
"O" entre-elles """


"""L'idée est que les cellules qui sont regroupées entre-elles en section
lorsqu'un mur est cassé vont avoir le même attribut liste et vont
appartenir à la même sous liste (definies dans self.secteur)"""

"""A chaque fois qu'on créé une nouvelle section (groupe de cellules
reliées entre-elles) on donne aux cellules de cette section le même attribut
self.liste qui est différents de celui des autres cellules qui
appartiennent à d'autres section
Ces cellules formeront une nouvelle sous liste dans self.secteur"""


class Section:

    def __init__(self, secteur=[]):
        self.secteur=secteur

    def creer_liste(self, cellule1, cellule2, position_secteur):
        cellule1=Cellule(cellule1, "L"+str(position_secteur))
        cellule2=Cellule(cellule2, "L"+str(position_secteur))
        self.secteur.append([cellule1, cellule2])
        return(cellule1, cellule2)

    def __str__(self):
        return("{}".format(self.secteur))

    def fusion_de_secteur(self, laby1, laby2):
        liste_secteur_modifié=[]
        cellule_secteur2=[]
        for i in range(len(self.secteur)):
            for j in range(len(self.secteur[i])):
                if self.secteur[i][j]==laby1:
                    position_laby1=i
                elif self.secteur[i][j]==laby2:
                    position_laby2=i
                else:
                    pass
        for i in self.secteur[position_laby2]:
            i=Cellule(i, self.secteur[position_laby1][0].liste)
            liste_secteur_modifié.append(i)
        self.secteur[position_laby1]+=self.secteur[position_laby2]
        cellule_secteur2=self.secteur[position_laby2]
        del self.secteur[position_laby2]
        return(liste_secteur_modifié, cellule_secteur2)
#On garde la section qu'on supprime pour pouvoir modifier leur attribut liste
#et faire qu'il soit le même de l'autre section        
        

    def ajouter_cellule_secteur(self, laby1, laby2):
        for i in range(len(self.secteur)):
            for j in range(len(self.secteur[i])):
                if self.secteur[i][j]==laby1:
                    position_laby1=i

        laby2=Cellule(laby2, self.secteur[position_laby1][0].liste)
        self.secteur[position_laby1].append(laby2)
        return(laby2)
