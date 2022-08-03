
import os
from tkinter import *
from Fonctions_usuelles import *



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

choix=False
while choix==False:
    choix_de_la_carte=input("Entrez un numéro de labyrinthe pour commencer à jouer: ")
    try:
        choix_de_la_carte=int(choix_de_la_carte)
        assert choix_de_la_carte>0 and choix_de_la_carte<nb_laby
        choix=True
    except ValueError:
        print("Vous n'avez pas entrer un numéro")
    except AssertionError:
        print("Le numéro entré ne correspond à aucun labyrinthe")
    nom_carte=nom_cartes[choix_de_la_carte]



L, lab_x, lab_y, robot = convertir_chaine(cartes[nom_carte])
print(robot.x, robot.y)


h=20
k=20
while lab_x*h>1600:
    h-=1
lab_x = lab_x*h

while lab_y*k>780:
    k-=1

lab_y=lab_y*k

longueur_case=min(h, k)

obstacle_avant = " "
fen=Tk()
can=Canvas(fen, width=lab_x, height=lab_y, bg='#FFFFFF')
for i in range(len(L)):
    for j in range(len(L[i])):
        if L[i][j] == 'O'.lower():
            can.create_rectangle(j*longueur_case,i*longueur_case,(j+1)*longueur_case,(i+1)*longueur_case, fill='#000000')
        elif L[i][j] == 'X':
            rob_x1 = j*longueur_case
            rob_y1= i*longueur_case
            rob_x2 = (j+1)*longueur_case
            rob_y2 = (i+1)*longueur_case

        elif L[i][j] == '.':
            if L[i+1][j] == 'O' or L[i-1][j] == 'O':
                can.create_rectangle(j*longueur_case+5,i*longueur_case,(j+1)*longueur_case-5,(i+1)*longueur_case, fill='brown', width=0)
            if L[i][j+1] == 'O' or L[i][j-1] == 'O':
                can.create_rectangle(j*longueur_case,i*longueur_case+5,(j+1)*longueur_case,(i+1)*longueur_case-5, fill='brown', width=0)           
        else:
            can.create_rectangle(j*longueur_case,i*longueur_case,(j+1)*longueur_case,(i+1)*longueur_case, fill='#FFFFFF', outline='#FFFFFF')

Robot = can.create_oval(rob_x1, rob_y1, rob_x2, rob_y2, fill='red', outline='red')
if longueur_case>14:
    Robot_oeil1 = can.create_oval(rob_x1+5, rob_y1+7, rob_x2+8-longueur_case, rob_y2+10-longueur_case, fill='yellow', outline='yellow')
    Robot_oeil2 = can.create_oval(rob_x1+13, rob_y1+7, rob_x2+16-longueur_case, rob_y2+10-longueur_case, fill='yellow', outline='yellow')



def deplacement(event):

    global rob_x1, rob_x2, rob_y1, rob_y2, L, obstacle_avant, test
    touche = event.char
    if touche == 'z':
        test, obstacle_avant, L = deplacement_rob(L, robot, robot.x+1, robot.y, obstacle_avant)
        print(test, robot.x+1, robot.y, robot)
        if test == True:    
            rob_y1 -= longueur_case
            rob_y2 -= longueur_case

    if touche == 's':
        test, obstacle_avant, L = deplacement_rob(L, robot, robot.x-1, robot.y, obstacle_avant)
        if test == True:
            rob_y1 += longueur_case
            rob_y2 += longueur_case

    if touche == 'q':
        test, obstacle_avant, L = deplacement_rob(L, robot, robot.x, robot.y-1, obstacle_avant)
        if test == True:
            rob_x1 -= longueur_case
            rob_x2 -= longueur_case

    if touche == 'd':
        test, obstacle_avant, L = deplacement_rob(L, robot, robot.x, robot.y+1, obstacle_avant)
        if test == True:
            rob_x1 += longueur_case
            rob_x2 += longueur_case

    can.coords(Robot, rob_x1, rob_y1, rob_x2, rob_y2)
    if longueur_case>14 and test == True:
        can.coords(Robot_oeil1, rob_x1+5, rob_y1+7, rob_x2+8-longueur_case, rob_y2+10-longueur_case)
        can.coords(Robot_oeil2, rob_x1+13, rob_y1+7, rob_x2+16-longueur_case, rob_y2+10-longueur_case)


can.focus_set()
can.bind('<Key>', deplacement)
can.pack()
fen.mainloop()

