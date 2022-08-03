# -*-coding:Utf-8 -*
from roboc import RobocError
from roboc.utils import INSTALL_path, \
						EvenementQuitter, \
						EvenementVictoire, \
						inputQ

from roboc.labyrinthes import Labyrinthes
from roboc.robots import Robots
from roboc.mouvements import Mouvements
from roboc.dictionnairedeslabyrinthes import DictionnaireDesLabyrinthes
from roboc.parties import Parties

##Paramètres FIGÉES
#Chemins des fichiers de sauvegarde
LABYRINTHES_chemin = INSTALL_path + '/RobocLabyrinthes'

print("Bienvenue dans Roboc\n")

try:
	LABYRINTHES = DictionnaireDesLabyrinthes(LABYRINTHES_chemin)
except (FileNotFoundError, EOFError) as err:
	print("Le dictionnaire des labyrinthes n'est pas chargé.")
	print("Vérifiez la présence du fichier :")
	print(LABYRINTHES_chemin)
	LABYRINTHES = DictionnaireDesLabyrinthes()

commande = ""

while commande != 'Q':
	print("""Options :
	  - (1) commencer une nouvelle partie
	  - (2) reprendre la partie en cours
	  - (3) voir le catalogue des labyrinthes
	  - (4) charger un nouveau labyrinthe
	  - (5) sauvegarder le dictionnaire des labyrinthes 
	  - (Q) Quitter le jeu""")

	commande = input("Que voulez-vous faire ?\n").upper()
	if commande == '1':
		try:
			Parties(LABYRINTHES,True)
		except EvenementQuitter as event :
			pass
		except EvenementVictoire as event :
			print(event)
	elif commande == '2':
		try:
			Parties(LABYRINTHES, False)
		except FileNotFoundError as err:
			print("Il n'y a pas de partie sauvegardée")
		except (RobocError.PartieTermine, EvenementQuitter) as event :
			pass
		except EvenementVictoire as event :
			print(event)
	elif commande == '3':
		print(LABYRINTHES)
	elif commande == '4':
		try:
			chemin = inputQ("Veuillez indiquer le chemin du nouveau labyrinthe : ")
			LABYRINTHES.NouveauLabyrinthe(chemin)
		except RobocError.LabyrintheExists as err:
			print("Le labyrinthe est déjà dans le dictionnaire avec l'indice : " + err.args[0])
		except FileNotFoundError as err:
			print("Le chemin fourni ne pointe pas vers un fichier valide.\n")
			print("Veuillez vérifier le fichier :")
			print(chemin)
		except (RobocError.LabyrintheInvalide, EvenementQuitter) as err:
			pass
	elif commande == '5':
		LABYRINTHES.Sauver(LABYRINTHES_chemin)
	elif commande == 'Q':
		print("Au revoir !")
	else:
		print("L'option n'existe pas !".center(50,'*'))

#le path existe a priori, on ne vérifie pas s'il a pu disparaitre entre temps
LABYRINTHES.Sauver(LABYRINTHES_chemin)
