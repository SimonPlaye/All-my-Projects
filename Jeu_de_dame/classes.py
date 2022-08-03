class plateau():

    def __init__(self):
        self.liste_pion = []
        self.plat = []
        self.nb_dames=1

    #Création du plateau avec les pions
    def create(self):
        plat_final = []
        cmpt_noir = 1
        cmpt_blanc = 1
        for i in range(10):
            plat = []
            for j in range(10):
                if j % 2 == 0:
                    if i == 1 or i == 3:
                        x = pion("noir", j, i, "B" + str(cmpt_noir))
                        cmpt_noir += 1
                        plat.append(x)
                        self.liste_pion.append(x)
                    elif i == 9 or i == 7:
                        x = pion("blanc", j, i, "W" + str(cmpt_blanc))
                        cmpt_blanc += 1
                        plat.append(x)
                        self.liste_pion.append(x)
                    else:
                        plat.append("O")
                else:
                    if i == 0 or i == 2:
                        x = pion("noir", j, i, "B" + str(cmpt_noir))
                        cmpt_noir += 1
                        plat.append(x)
                        self.liste_pion.append(x)
                    elif i == 8 or i == 6:
                        x = pion("blanc", j, i, "W" + str(cmpt_blanc))
                        cmpt_blanc += 1
                        plat.append(x)
                        self.liste_pion.append(x)
                    else:
                        plat.append("O")
            plat_final.append(plat)
        self.plat = plat_final

    "Affichage du plateau"
    def __repr__(self):
        plat = "  0 1 2 3 4 5 6 7 8 9 \n"
        cmpt = 0
        for i in self.plat:
            plat = plat + str(cmpt) + "~"
            for j in i:
                if type(i) == str:
                    plat = plat + j + " "
                else:
                    plat = plat + str(j)[0] + " "
            plat += "\n"
            cmpt += 1
        return (plat)

    #Permet d'affecter une pièce à une case du plateau
    def change(self, x, y, objet):
        self.plat[y][x] = objet

    #Permet de sélectionner une case du plateau
    def select(self, x, y):
        return(self.plat[y][x])

    def add_dames(self):
        self.nb_dames+=1

    def return_nb_dames(self):
        return(self.nb_dames)

class pion(plateau):

    def __init__(self, couleur, x, y, name):
        plateau.__init__(self)
        self.couleur = couleur
        self.x = x
        self.y = y
        self.name = name
        self.type = "Pion"
        self.picture = "pion_"+couleur+".png"

    def __repr__(self):
        return (self.name)

    #Permet de déplacer un pion
    def move(self, pos_x, pos_y, plateau):
        if self.couleur == "noir":
            #Premier cas: l'utilisateur veut ne déplacer que d'une case le pion
            if abs(pos_x - self.x) == 1 and pos_y - self.y == 1 and plateau.select(pos_x, pos_y)=="O":
                plateau.change(pos_x, pos_y, plateau.select(self.x,self.y))
                plateau.change(self.x, self.y, "O")
                self.x = pos_x
                self.y = pos_y
                if self.y == 9: #Si l'utilisateur est arrivé au bout du plateau le pion devient une dame
                    dame= Dame("noir",self.x, self.y, "b")
                    plateau.change(dame.x, dame.y, dame)
            else: #Cas où il déplace de plus d'une case pour manger un pion
                continuer=self.manger(pos_x, pos_y, plateau)
                return continuer
        else:
            if abs(pos_x - self.x) == 1 and pos_y - self.y == -1 and plateau.select(pos_x, pos_y)=="O":
                plateau.change(pos_x, pos_y, plateau.select(self.x, self.y)) #On déplace notre pion
                plateau.change(self.x, self.y, "O") #La case initiale est vide
                self.x = pos_x
                self.y = pos_y
                if self.y == 0: #Si l'utilisateur est arrivé au bout du plateau le pion devient une dame
                    dame= Dame("blanc",self.x, self.y, "w")
                    plateau.change(dame.x, dame.y, dame)
            else:
                continuer=self.manger(pos_x, pos_y, plateau)
                return continuer



    #L'utilisateur souhaite manger un pion
    def manger(self, pos_x, pos_y, plateau):
        #Permet de savoir la position du pion que l'on va manger
        if abs(pos_x - self.x) == 2 and abs(pos_y - self.y) == 2:
            if pos_x > self.x:
                n = 2
            else:
                n = 1
            if pos_y>self.y:
                k=2
            else:
                k=1

            #On vérifie si effectivement il y a un pion sur la case intermédiaire
            if plateau.plat[self.y + (-1)**k][self.x + (-1) ** n] != "O":
                #Peut-on manger ce pion intermédiaire
                if self.couleur == "noir" and \
                        plateau.plat[self.y + (-1)**k][self.x + (-1) ** n].couleur == "blanc" and \
                        plateau.plat[pos_y][pos_x] == "O":
                    if pos_y == 9 :
                        dame = Dame("noir", pos_x, pos_y, "b")
                        plateau.change(pos_x, pos_y, dame)
                        plateau.plat[self.y + (-1)**k][self.x + (-1) ** n] = "O" #On mange le pion
                        plateau.plat[self.y][self.x] = "O" #On rend vide la case initiale
                        self.x = pos_x
                        self.y = pos_y
                    else:
                        plateau.change(pos_x, pos_y, plateau.select(self.x, self.y)) #On déplace notre pion
                        plateau.plat[self.y + (-1)**k][self.x + (-1) ** n] = "O" #On mange le pion
                        plateau.plat[self.y][self.x] = "O" #On rend vide la case initiale
                        self.y = pos_y
                        self.x = pos_x
                    return True

                elif self.couleur == "blanc" and \
                        plateau.plat[self.y + (-1)**k][self.x + (-1) ** n].couleur == "noir" and \
                        plateau.plat[pos_y][pos_x] == "O":
                    if pos_y == 0:
                        dame = Dame("blanc", pos_x, pos_y, "w")
                        plateau.change(pos_x, pos_y, dame)
                        plateau.plat[self.y + (-1) ** k][self.x + (-1) ** n] = "O"
                        plateau.plat[self.y][self.x] = "O"
                        self.x = pos_x
                        self.y = pos_y
                    else:
                        plateau.change(pos_x, pos_y, plateau.select(self.x, self.y))
                        plateau.plat[self.y + (-1)**k][self.x + (-1) ** n] = "O"
                        plateau.plat[self.y][self.x] = "O"
                        self.y = pos_y
                        self.x = pos_x
                    return True
                else:
                    return False

            else:
                return False
        else:
            return False

class Dame(plateau):

    def __init__(self, couleur, x, y, name):
        plateau.__init__(self)
        self.couleur = couleur
        self.x = x
        self.y = y
        self.name = name+str(plateau.return_nb_dames(self))
        self.type = "Dame"
        self.picture = "dame_" + couleur + ".png"
        plateau.add_dames(self)

    def __repr__(self):
        return (self.name)

    def move(self, pos_x, pos_y, plateau):
        if pos_x > self.x:
            k=2
        else:
            k=1
        if pos_y > self.y:
            n=2
        else:
            n=1

        if abs(self.x - pos_x)==abs(self.y - pos_y) and self.x!=pos_x: #on vérifie que le déplacement se fasse en diagonale et qu'on déplace bien la dame
            distance_parcourue = abs(self.x - pos_x)
            deplacement=True
            manger=False
            for i in range(1, distance_parcourue + 1):
                case_x = self.x + i * ((-1) ** k)
                case_y = self.y + i * ((-1) ** n)
                objet_case = plateau.select(case_x, case_y)
                if objet_case == "O":
                    continue
                else:
                    if objet_case.couleur == self.couleur:
                        deplacement = False
                        break
                    else:
                        case_finale_x = self.x + (i + 1) * ((-1) ** k)
                        case_finale_y = self.y + (i + 1) * ((-1) ** n)
                        case_finale = plateau.select(case_finale_x, case_finale_y)
                        if i == distance_parcourue - 1 and case_finale == "O":
                            manger = True
                        else:
                            print("impossible de déplacer la dame")
                            deplacement = False
                            break
            if deplacement == True and manger == False:
                print("Dame déplacement sans manger")
                plateau.change(pos_x, pos_y, plateau.select(self.x, self.y)) #on déplace la dame
                plateau.change(self.x, self.y, "O") #on rend vide la case initiale
                self.x = pos_x
                self.y = pos_y
            elif deplacement == True and manger == True:
                print("Dame déplacmeent en mangeant")
                plateau.change(pos_x, pos_y, plateau.select(self.x, self.y))  # on déplace la dame
                plateau.change(self.x, self.y, "O")  # on rend vide la case initiale
                plateau.change(pos_x + (-1) ** (k - 1), pos_y + (-1) ** (n - 1), "O") #On rend vide la case où on mange un pion
                self.x = pos_x
                self.y = pos_y
                return True


    def manger(self, pos_x, pos_y, plateau):
        if abs(pos_x - self.x) == 2 and abs(pos_y - self.y) == 2:
            if pos_x > self.x:
                n = 2
            else:
                n = 1
            if pos_y > self.y:
                k = 2
            else:
                k = 1

            # On vérifie si effectivement il y a un pion sur la case intermédiaire
            if plateau.plat[self.y + (-1) ** k][self.x + (-1) ** n] != "O":
                # Peut-on manger ce pion intermédiaire
                if self.couleur == "noir" and \
                        plateau.plat[self.y + (-1) ** k][self.x + (-1) ** n].couleur == "blanc" and \
                        plateau.plat[pos_y][pos_x] == "O":
                    plateau.change(pos_x, pos_y, plateau.select(self.x, self.y))  # On déplace notre dame
                    plateau.plat[self.y + (-1) ** k][self.x + (-1) ** n] = "O"  # On mange le pion
                    plateau.plat[self.y][self.x] = "O"  # On rend vide la case initiale
                    self.y = pos_y
                    self.x = pos_x
                    return True

                elif self.couleur == "blanc" and \
                        plateau.plat[self.y + (-1) ** k][self.x + (-1) ** n].couleur == "noir" and \
                        plateau.plat[pos_y][pos_x] == "O":
                    plateau.change(pos_x, pos_y, plateau.select(self.x, self.y))
                    plateau.plat[self.y + (-1) ** k][self.x + (-1) ** n] = "O"
                    plateau.plat[self.y][self.x] = "O"
                    self.y = pos_y
                    self.x = pos_x
                    return True
                else:
                    return False

            else:
                return False
        else:
            return False
