# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""

import os

class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""
    def __init__(self):
        self.cartes=[]
        self.carteChoisie = None

    def trouver_cartes(self):
        for nom_fichier in os.listdir("cartes"):
            if nom_fichier.endswith(".txt"):
                chemin = os.path.join("cartes", nom_fichier)
                nom_carte = nom_fichier[:-4].lower()
                self.cartes.append((chemin, nom_carte))

    def choisir_carte(self):
        print("Labyrinthes existants :")
        for i, carte in enumerate(self.cartes):
            print("  {} - {}".format(i + 1, self.cartes[i][1]))
        input_label="\nEntrez le numero de la carte choisie :"
        while True:
            try:
                self.carteChoisie = self.cartes[int(input(input_label))-1]
                break
            except IndexError:
                input_label="Entrez un numero entre {} et {} : ".format(1, len(self.cartes))
            except ValueError:
                input_label="Entrez le NUMERO de la carte choisie : "
        print()
        with open(self.carteChoisie[0], 'r') as fichier_carte:
            carte = fichier_carte.read()
            print(carte)
            fichier_carte.close()
        return carte

    def sauvegarder(self, labyrinte):
        chemin = self.carteChoisie[0][:-(len(self.carteChoisie[1]) + 4)] + "sauvegarde_de_" + self.carteChoisie[1] + ".txt"
        with open(chemin, "w") as fichier:
            fichier.write(str(labyrinte))
            fichier.close()

if __name__ == "__main__":
    demo = Carte()
    demo.trouver_cartes()
    demo.choisir_carte()
    os.system("pause")
