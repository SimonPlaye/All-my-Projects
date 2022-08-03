"""Fichier contenant les classes propres aux éléments constituants le laby"""


class Mur:

    def __init__(self, x, y):
        self.nom = 'mur'
        self.symbole = 'O'
        self.x = x
        self.y = y
        self.traverser=False


    def __repr__(self):
        return("{}".format(self.symbole))


class Sortie:

    def __init__(self, x, y):
        self.nom = 'sortie'
        self.symbole='U'
        self.x = x
        self.y=y
        self.traverser=True

    def __repr__(self):
        return("{}".format(self.symbole))


class Porte:

    def __init__(self, x, y):
        self.nom = 'porte'
        self.symbole='.'
        self.x = x
        self.y=y
        self.traverser=True

    def __repr__(self):
        return("{}".format(self.symbole))


class Robot:

    def __init__(self, x, y):
        self.nom = 'robot'
        self.symbole='X'
        self.x = x
        self.y=y

    def __repr__(self):
        return("{}".format(self.symbole))

        
