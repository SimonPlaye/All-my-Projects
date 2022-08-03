# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

import os

class Labyrinthe:

    """Classe représentant un labyrinthe."""

    def __init__(self, grille):
        self.robot_position = grille.find("X")
        self.grille = [None]*len(grille)
        for loop in range(len(grille)):
            self.grille[loop] = grille[loop]
        self.largeur = len(grille.split("\n")[0])+1

    def __str__(self):
        return "".join(self.grille)

    def deplacer(self, position_case_depart, position_case_arrive):
        """méthode permetant d'inverser deux cases,
        initialement prévue pour deplacer le robot
        elle poura servir à déplacer les murs dans
        une version prochaine"""
        if self.grille[position_case_arrive] in ("O", "U"):
                return self.grille[position_case_arrive]
        tmp = self.grille[position_case_depart]
        self.grille[position_case_depart] = self.grille[position_case_arrive]
        self.grille[position_case_arrive] = tmp
        return self.grille[position_case_arrive]

    def deplacer_robot(self, mouvement, nb):
        mouvements = {"N":-self.largeur, "E":1, "S":self.largeur, "O":-1}
        for loop in range(nb):
            robot_pos = self.robot_position
            resultat_du_deplacement = self.deplacer(robot_pos, robot_pos + mouvements[mouvement])
            if resultat_du_deplacement == "U":
                print("Vous avez gagné !")
                os.system("PAUSE")
                break
            elif resultat_du_deplacement != "O":
                self.robot_position += mouvements[mouvement]
