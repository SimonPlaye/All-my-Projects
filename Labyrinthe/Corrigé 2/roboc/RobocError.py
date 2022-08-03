# -*-coding:Utf-8 -*

from roboc.utils import symboles_default

#Erreur d'importation de labyrinthe
class PartieTermine(Exception):
	def __init__(self, *args):
		pass

class NoLabyrinthe(Exception):
	def __init__(self, *args):
		print("Pas de labyrinthe.")

class LabyrintheInvalide(Exception):
	def __init__(self, *args):
		print("Le labyrinthe n'est pas valide.")

class LabyrintheExists(LabyrintheInvalide):
	def __init__(self, *args):
		print("Le labyrinthe est déjà dans le dictionnaire.")

class LabyrintheRectangle(LabyrintheInvalide):
	def __init__(self, *args):
		print("Le labyrinthe n'est pas rectangle.")

class LabyrintheString(LabyrintheInvalide):
	def __init__(self, *args):
		print("Un labyrinthe doit être une chaine de caractère.")

class LabyrintheElementInconnu(LabyrintheInvalide):
	def __init__(self, *args):
		print("Il y a des caractères inconnus dans ce labyrinthe.")

class LabyrintheEntreeUnique(LabyrintheInvalide):
	def __init__(self, *args):
		print("Le labyrinthe n'a pas une unique entrée.")

class LabyrintheSortieUnique(LabyrintheInvalide):
	def __init__(self, *args):
		print("Le labyrinthe n'a pas une unique sortie.")

class LabyrintheRobotUnique(LabyrintheInvalide):
	def __init__(self, *args):
		print("Il ne peut pas y avoir plus d'un robot par labyrinthe.")

##Erreur de manipulation du robot
class MouvementInvalide(ValueError):
	def __init__(self, *args):
		print("Le mouvement demandé n'est pas reconnu.")

class MouvementObstacle(ValueError):
	def __init__(self, obstacle='', *args):
		if obstacle == symboles_default['mur']:
					print("Vous ne pouvez pas traverser un mur !\n(Enfin, voyons !)")
		elif obstacle == symboles_default['porte']:
			print('2**********')
			print("Une porte vous bloque le passage.")
			print('3**********')
		elif obstacle == symboles_default['entree']:
			print("Les grilles du labyrinthe se sont refermées.\nIl faut sortir maintenant !")
		else:
			pass

class MouvementTropLong(MouvementInvalide):
	def __init__(self, intensite = 0):
		if intensite != 0:
			print("Le mouvement sera limité à {} pas.".format(str(intensite)))
		else:
			print("Le mouvement fait sortir le robot du cadre.")


