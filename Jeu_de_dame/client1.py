import socket
import pickle
from affichage import *

hote = "192.168.1.19"
port = 12800

#Connexion au serveur
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))


#Lancement de pygame
pygame.init()

first_message = False #le serveur défini dans un premier message la couleur associée au joueur
#boucle infine chargée de recevoir le plateau
while True:
    if first_message == False: #réception de la couleur + joueur1 ou joueur2
        msg_init = connexion_avec_serveur.recv(1024)
        msg_init=msg_init.decode()
        joueur, couleur = msg_init.split("+")
        connexion_avec_serveur.send(b"ok")
    first_message = True
    print(f"Joueur : {joueur}, couleur : {couleur}")

    try: #on essaie de recevoir du plateau
        msg_recu = connexion_avec_serveur.recv(4096)
    except ConnectionResetError:
        print("L'hôte a fermé la connexion")
        connexion_avec_serveur.close()
    else:
        if msg_recu != "": #on a recu un message du serveur
            try:
                data = pickle.loads(msg_recu) #récupération du plateau sous forme de classe
            except EOFError:
                print("EOFError") #impossible d'unpickle le message reçu
                connexion_avec_serveur.close()
            else: #on a pu correctement réceptionner le plateau
                print(data)
                #création de la fenetre pygame
                fenetre = pygame.display.set_mode((700, 700), RESIZABLE)
                print_plateau(data, fenetre, joueur) #affichae du plateau
                jeu = play(data, fenetre, joueur, couleur) #le joueur joue
                print(jeu)
                #on renvoie au serveur le plateau après que le joueur ait déplacé ses pions
                data = pickle.dumps(jeu)
                connexion_avec_serveur.send(data)
                print("Data envoyée au serveur")

print("Fermeture de la connexion")
connexion_avec_serveur.close()
