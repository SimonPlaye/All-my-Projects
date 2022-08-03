import socket
from classes import *
import pickle
import select

#le seveur commence à écouter
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind(('', 12800))
connexion_principale.listen(5)

#création des variables qui vont contenir les clients
list_clients=[]
dictionnaire_clients={}

#création du plateau qui sera envoyé aux joueurs
jeu = plateau()
jeu.create()

first_message = False

#on continue tant qu les deux clients ne se sont pas déconnectés
serveur_out=0
while serveur_out!=2:
    #on cherche si de nouveaux clients se connectent
    connexions_demandees, wlist, xlist = select.select([connexion_principale],[],[],1)
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        list_clients.append(connexion_avec_client)
    print(f"Nombre de cliens connectées : {len(list_clients)}")

    #on a deux clients de connecté: on peut jouer
    if len(list_clients)==2:
        dictionnaire_clients["client_1"]=list(list_clients[0].getpeername())+["blanc"] #on récupère l'IP et le port pour indentifier chaque client
        dictionnaire_clients["client_2"] = list(list_clients[1].getpeername())+["noir"] #on défini aussi une couleur de pion à chaque client

        #maintenant on va se connecter à chaque client l'un après l'autre à l'infini
        continuer = True
        while continuer:
            i = 0
            while i < 2: #connexion à un des deux clients
                client = list_clients[i]
                ip, port, couleur = dictionnaire_clients["client_"+str(i+1)]
                print("\n")
                print(f"Joueur : {i+1}")
                print("\n")

                if first_message == False: #si c'est la première connexion à un client, on lui envoie sa couleur
                    if couleur == "blanc":
                        msg_envoye = "joueur 1+blanc"
                    else:
                        msg_envoye = "joueur 2+noir"
                    client.send(msg_envoye.encode())

                    msg_recu =""
                    while msg_recu!=b"ok": #le client a bien recu sa couleur
                        msg_recu = client.recv(1094)

                try: #on envoie la plateau au client
                    data=pickle.dumps(jeu)
                    print("\n")
                    client.send(data)
                    print(f"Data send : {jeu}")
                    print("\n")
                    data_list = []
                    while True: #cette boucle sert à récupérer le plateau envoyé par le client qui est souvent trop lourd pour être recu en 1 seule fois
                        packet = client.recv(4096)
                        data_list.append(packet)
                        if len(packet) < 1460:
                            break #on a recu tous les paquets qui composent le plateau

                    if data_list !=[]:
                        try:
                            data = pickle.loads(b"".join(data_list)) #on rassemble tous les paquets pour créer le plateau
                        except EOFError: #on ne peut pas unpickle les paquets recus
                            print("EOFError server")
                        except pickle.UnpicklingError: #ici les données sont trop lourdes: il faut redécomposer le plateau en plus petits paquets pour tout recevoir
                            print(f"UnpicklingError : data was truncated")
                            serveur_out=2
                        else:
                            jeu = data #les données recu sont affectées à la variable qu'on enverra par la suite à l'autre client
                            print("Data reçue : \n")
                            print(data)
                            print("\n")
                except ConnectionResetError:
                    serveur_out=2 #le plateau n'a pas pu être envoyé car le serveur a coupé la connexion
                    print("L'hôte met fin à la connexion")
                i+=1 #le joueur a fini de jouer: on passe au joueur suivant
                if i == 2:
                    i=0
                    first_message = True




connexion_principale.close()