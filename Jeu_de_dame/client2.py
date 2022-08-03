import socket
import pickle
from affichage import *

hote = "192.168.1.19"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))



pygame.init()
first_message = False
while True:
    if first_message == False:
        msg_init = connexion_avec_serveur.recv(1024)
        msg_init=msg_init.decode()
        joueur, couleur = msg_init.split("+")
        connexion_avec_serveur.send(b"ok")
    first_message = True
    print(f"Joueur : {joueur}, couleur : {couleur}")
    try:
        msg_recu = connexion_avec_serveur.recv(4096)
    except ConnectionResetError:
        print("L'hôte a fermé la connexion")
        connexion_avec_serveur.close()
    else:
        if msg_recu != "":
            try:
                data = pickle.loads(msg_recu)
            except EOFError:
                print("EOFError")
                connexion_avec_serveur.close()
            else:
                print(data)
                fenetre = pygame.display.set_mode((700, 700), RESIZABLE)
                print_plateau(data, fenetre, joueur)
                jeu = play(data, fenetre, joueur, couleur)
                print(jeu)
                data = pickle.dumps(jeu)
                connexion_avec_serveur.send(data)
                print("Data envoyée au serveur")

print("Fermeture de la connexion")
connexion_avec_serveur.close()
