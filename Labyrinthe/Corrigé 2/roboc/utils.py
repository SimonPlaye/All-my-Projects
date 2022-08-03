# -*-coding:Utf-8 -*

from os.path import dirname

INSTALL_path = dirname(__file__)

#symboles du labyrinthe
symboles_default = {}
symboles_default['mur']="#"
symboles_default['porte']="P"
symboles_default['couloir']=" "
symboles_default['entree']="E"
symboles_default['sortie']="S"
symboles_default['robot']="@"

##Événements
class EvenementQuitter(Exception):
	def __init__(self, *args):
		print("".join(args))
		pass

class EvenementVictoire(Exception):
	def __init__(self, *args):
		print("Vous avez gagné la partie.")

#redéfintion de la fonction input pour lever une erreur si 'Q'
def inputQ(*args):
	reponse = input(args[0])
	reponseUp = reponse.upper()
	if reponseUp == 'Q':
		raise EvenementQuitter
	return reponse
