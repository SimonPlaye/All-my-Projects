# -*-coding:Utf-8 -*
import pickle
from os import listdir

from roboc import RobocError
from roboc.utils import INSTALL_path, \
						EvenementQuitter, \
						EvenementVictoire, \
						inputQ, \
						symboles_default

from roboc.labyrinthes import Labyrinthes
from roboc.robots import Robots
find_robot = Robots.find_robot

SYMBOLES_chemin = INSTALL_path + '/RobocSymboles'
CARTES_chemin = INSTALL_path + '/cartes'
cartes_existante = listdir(CARTES_chemin)

class DictionnaireDesLabyrinthes(dict):
	"""
	Le DictionnaireDesLabyrinthes est l'object contenant l'ensemble des cartes chargées dans le jeu.
	Il peut être sauvé ou chargé depuis un fichier.
	Par défaut, le programme sauve le dicitionnaire dans le fichier RobocLabyrinthes.
	"""
	def Charger(self, fichier_chemin):
		try:
			with open(fichier_chemin, 'rb') as fichier :
				self._dictionnaire = pickle.Unpickler(fichier).load()
		except (FileNotFoundError, EOFError) as err:
			raise FileNotFoundError
		finally:
			print(str(len(self._dictionnaire)) + " labyrinthe(s) ont été chargés.")
	
	def Sauver(self, fichier_chemin):
		try:
			with open(fichier_chemin, 'wb') as fichier:
				pickle.Pickler(fichier).dump(self._dictionnaire)
				print("Le dictionnaire a bien été sauvé")
		except:
			print("Le dictionnaire des labyrinthes n'a pas pu être sauvé")
	
	def __init__(self, fichier_chemin=""):
		self._dictionnaire = {}
		
		if fichier_chemin != "":
			self.Charger(fichier_chemin)
	
	def __len__(self):
		return len(self._dictionnaire)
	
	def __contains__(self, item):
		return item in self._dictionnaire
	
	def has_key(self, k):
		return k in self._dictionnaire
	
	def keys(self):
		return self._dictionnaire.keys()
	
	def values(self):
		return self._dictionnaire.values()
	
	def __getitem__(self, key):
		return self._dictionnaire[key]
	
	def __delitem__(self, key):
		value_to_return = self._dictionnaire[key]
		del self._dictionnaire[key]
		return value_to_return
	
	def __setitem__(self, key, item):
		self._dictionnaire[key] = item
	
	def __repr__(self):
		return repr(self._dictionnaire)
	
	def __str__(self):
		if len(self) > 0:
			string_msg = ""
			for labyrinthe_id, labyrinthe in self._dictionnaire.items():
					string_msg += "(" + labyrinthe_id + ") : " + labyrinthe.nom +\
									"\n" + labyrinthe._labyrinthe +\
									"\n" + "*".center(50,'*') + "\n"
			return string_msg
		else:
			return "Pas de labyrinthe au dictionnaire."
	
	def NouveauLabyrinthe(self, chemin_du_fichier):
		nouveau_labyrinthe = Labyrinthes()
		
		try:
			with open(chemin_du_fichier, 'r', newline=None) as fichier :
				print("""
					Rappel : 
						- le labyrinthe doit être une string,
						- les caracatères '#', 'E','S', 'P', '@' et les espaces
						    sont utilisés mais vous pouvez convertir les symboles
						    au chargement dans le dictionnaire,
						- le labyrinthe doit être rectangulaire (attention à la 
						    dernière ligne de votre fichier et aux espaces),
						- un robot est converti en entrée (E),
						- le labyrinthe doit contenir qu'une entrée (ou un robot) et qu'une sortie.
				""")
				
				nouveau_labyrinthe.labyrinthe = fichier.read() 
				
				print("Le labyrinthe que vous souhaitez charger :\n")
				print(nouveau_labyrinthe.labyrinthe)
				
				nouveau_labyrinthe.Charger_symboles()
				nouveau_labyrinthe.Conversion_symboles()
				try:
					nouveau_labyrinthe.labyrinthe_verification()
				except (RobocError.LabyrintheRobotUnique, \
								RobocError.LabyrintheEntreeUnique, \
								RobocError.LabyrintheSortieUnique) as err:
					raise RobocError.LabyrintheInvalide
				except RobocError.NoLabyrinthe as err:
					raise RobocError.NoLabyrinthe
				except RobocError.LabyrintheString as err:
					print("type de tracee : " + err.args[0])
					raise RobocError.LabyrintheInvalide
				except RobocError.LabyrintheElementInconnu as err:
					print("Les éléments autorisés sont " + \
									", ".join([(_value + " (" +_key + ")") \
									for _key, _value in err.args[0].items()]))
					print(nouveau_labyrinthe)#debug
					raise RobocError.LabyrintheInvalide
				except RobocError.LabyrintheRectangle as err:
					print(("La ligne {0} comporte {1} caractères").format( \
									str(int(err.args[0]) + 1), err.args[1]))
					raise EvenementQuitter
				except Exception as err:
					raise err
				
				nouveau_labyrinthe.nom = chemin_du_fichier.rsplit("/")[-1].split(".")[0]
				
				if Robots.find_robot(nouveau_labyrinthe) != -1:
					nouveau_labyrinthe = nouveau_labyrinthe.replace(symboles_default['robot'], symboles_default['entree'])

		except RobocError.LabyrintheRobotUnique:
			raise EvenementQuitter("Vous ne pouvez pas charger un labyrinthe avec un robot.")
		except RobocError.LabyrintheInvalide as err:
			raise EvenementQuitter("Le labyrinthe n'est pas chargé. Merci de vérifier votre dessin.")

		nouveau_labyrinthe.Sauver_symboles()
		nouveau_labyrinthe.symboles = symboles_default

		if self._dictionnaire == {}:
			nouvel_indice = '1'
		else:
			if nouveau_labyrinthe.labyrinthe in \
							[x.labyrinthe for x in self._dictionnaire.values()]:
				for labyrinthe_id, labyrinthe_du_dictionnaire in \
							self._dictionnaire.items():
					if nouveau_labyrinthe.labyrinthe == labyrinthe_du_dictionnaire.labyrinthe:
						raise RobocError.LabyrintheExists(labyrinthe_id)
			else:
				nouvel_indice = str(max([int(x) for x in self._dictionnaire.keys()]) + 1)
		
		print("Le nouveau labyrinthe \'" + nouveau_labyrinthe.nom + "\' à ajouter au dictionnaire :\n" + \
						nouveau_labyrinthe.labyrinthe)
		print("a été ajouté avec l'indice : " + nouvel_indice + "\n\n")
		self._dictionnaire[nouvel_indice] = nouveau_labyrinthe
