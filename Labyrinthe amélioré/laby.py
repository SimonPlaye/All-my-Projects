import os
from tkinter import *
from commandes import *

cartes = {}
nom_cartes={}
nb_laby=1
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-4].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
        cartes[nom_carte]=contenu
        nom_cartes[nb_laby]=nom_carte
        nb_laby+=1

for cle, valeurs in nom_cartes.items():
    print("  {} - {}".format(cle, valeurs))



fen=Tk()
fen.title('Labyrinthe')

label= Label(fen, text='Avez-vous déjà jouer au labyrinthe?', justify = 'center', anchor='n')
label.pack(side=TOP, padx=50, pady=10)
can =Canvas(fen, width=500, height=150)
can.pack()
but1 = Button(fen, text='Non', width=50, command=destroy(fen))
but1.pack(side= RIGHT, padx=30, pady=50)
but2 = Button(fen, text='Oui', width=50)
but2.pack(side=LEFT, padx=30, pady=50)

fen.mainloop()
