# -*-coding:Utf-8 -*
import pickle

from roboc import RobocError
from roboc.utils import INSTALL_path,\
						EvenementQuitter,\
						inputQ,\
						symboles_default

SYMBOLES_chemin = INSTALL_path + "/RobocSymboles"

class DictionnaireDesSymboles(dict):
	"""
	Le DictionnaireDesSymboles est l'object contenant l'ensemble des sets de symboles
	utilisés pour charger les labyrinthes.
	Il peut être sauvé ou chargé depuis un fichier.
	Par défaut, le programme sauve le dictionnaire dans le fichier RobocSymboles.
	"""
	
	def Charger(self, fichier_chemin):
		try:
			with open(fichier_chemin, 'rb') as fichier :
				self._dictionnaire = pickle.Unpickler(fichier).load()
		except (FileNotFoundError, EOFError) as err:
			raise FileNotFoundError
	
	def Sauver(self, fichier_chemin):
		try:
			with open(fichier_chemin, 'wb') as fichier:
				pickle.Pickler(fichier).dump(self._dictionnaire)
		except:
			print("Le dictionnaire des symboles n'a pas pu être sauvé")
	
	def __init__(self, fichier_chemin=""):
		self._dictionnaire = {}
		
		if fichier_chemin != "":
			DictionnaireDesSymboles.Charger(self, fichier_chemin)
	
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
		if len(self)>0:
			string_msg = ""
			for symbole_set_id, symbole_set in self._dictionnaire.items():
				string_msg += "\n" + "(" + symbole_set_id + ") : " + str(symbole_set)
			return string_msg[1:]
		else:
			return "{}"
	
	def __cmp__(self, dict_):
		return self.__cmp__(self._dictionnaire, dict_)
	
	def __iter__(self):
		return iter(self._dictionnaire)

class Labyrinthes():
	"""
	"""
	
	def labyrinthe_verification(self):
		"""
		Vérifie si un labyrinthe est valide ou non :
			- le labyrinthe doit être une string,
			- seuls les caracatères '#', 'E','S', 'P', '@' et les espaces
			  sont acceptés,
			- le labyrinthe doit être rectangulaire,
			- le labyrinthe ne peut contenir qu'une entrée, qu'une sortie
			  et un seul robot (pas de version multi-joueur pour l'instant)
		"""
		
		if type(self._labyrinthe) != str:
			raise RobocError.LabyrintheString(str(type(self._labyrinthe)))
		if self._labyrinthe == "":
			raise RobocError.NoLabyrinthe
		
		#test s'il y a des éléments inconnus
		element_count = {}
		element_count['lignes'] = self._labyrinthe.count('\n')
		for element in symboles_default.values():
			element_count[element] = self._labyrinthe.count(element)
		
		if sum(element_count.values()) != len(self._labyrinthe):
			raise RobocError.LabyrintheElementInconnu(symboles_default)
		
		#test la largeur de chaque ligne
		labyrinthe_split = self._labyrinthe.splitlines()
		largeur = len(labyrinthe_split[0])
		for i, labyrinthe_ligne in enumerate(labyrinthe_split):
			if len(labyrinthe_ligne) != largeur:
				raise RobocError.LabyrintheRectangle(i, len(labyrinthe_ligne)) #(y,x)
		
		#test unicité Entrée, Sortie, Robot
		if self._labyrinthe.count(symboles_default['robot']) > 1:
			raise RobocError.LabyrintheRobotUnique
		elif self._labyrinthe.count(symboles_default['robot']) == 0: #hors d'une partie
			if self._labyrinthe.count(symboles_default['entree']) != 1:
				raise RobocError.LabyrintheEntreeUnique
			if self._labyrinthe.count(symboles_default['sortie']) != 1:
				raise RobocError.LabyrintheSortieUnique
		else:
			pass
	
	def set_labyrinthe(self, tracee):
		self._labyrinthe = tracee
		self._tableau = list([list(ligne) \
						for ligne in self._labyrinthe.splitlines()])
		self.largeur = len(self._tableau[0]) - 1
		self.longueur = len(self._tableau) - 1
	
	def get_labyrinthe(self):
		return self._labyrinthe
	
	labyrinthe = property(get_labyrinthe, set_labyrinthe)
	
	def set_tableau(self, tracee_tableau):
		"""
		Si le labyrinthe est modifiée par un tableau de caractère, le 
		labyrinthe est synchronisé.
		"""
		#On recompose le tableau en une string
		tmp_labyrinthe = ""
		try:
			for ligne in tracee_tableau:
				if ligne[-1] != "\n":
					ligne.append("\n")
				tmp_labyrinthe += "".join(ligne)
		except:
			pass
		
		#On passe par la mise à jour de la string pour mettre à jour 
		#l'attribut _tableau et faire la vérification
		self.labyrinthe = tmp_labyrinthe
	
	def get_tableau(self):
		return self._tableau
	
	tableau = property(get_tableau, set_tableau)
	
	def __init__(self):
		self.nom = ""
		self.symboles = {}
		self._labyrinthe = ""
		self._tableau  = list()
		self.longueur = 0
		self.largeur = 0
	
	def __str__(self):
		return self._labyrinthe
	
	def __radd__(self, val):
		if type(val) == str:
			return val + self._labyrinthe
	
	def Charger_symboles(self):
		#print(symboles_default)
		try:
			SYMBOLES = DictionnaireDesSymboles(SYMBOLES_chemin)
		except (FileNotFoundError, EOFError) as err:
			print("Le dictionnaire des symboles n'a pas pu ête trouvé.\n" + \
					"Seuls les symboles par défaut sont disponibles")
			SYMBOLES = DictionnaireDesSymboles()
			SYMBOLES['1'] = symboles_default
		
		print("Symboles utilisables : \n" + str(SYMBOLES) + '\n')
		charger_options = list(SYMBOLES.keys())
		charger_options.append('N')
		
		charger_option = ""
		while charger_option not in charger_options:
			try:
				charger_option = inputQ("Voulez-vous utiliser une table de conversion ci-dessus ?\n" + \
											"(entrez un numéro, N pour créer une nouvelle table ou 'Q' pour revenir au menu principal)\n").upper()
			except EvenementQuitter:
				raise EvenementQuitter
		
		if charger_option == 'N':
			symboles_OK = 'N'
			print("ATTENTION Q ou q ne peuvent pas être des symboles du labyrinthe !!! ")
			while symboles_OK !='O':
				for symboles_nom, symboles_signe in symboles_default.items() :
					self.symboles[symboles_nom] = inputQ("Quel symbole utiliser pour l'élément " + \
															symboles_nom + "(" + symboles_signe + ") : ")
				print(self.symboles)
				symboles_OK = inputQ("Le dictionnaire est-il OK ? (O/N)\n").upper()
		else:
			self.symboles = SYMBOLES[charger_option]#symboles_default
	
	def Choix_du_labyrinthe(self, dictionnaire_des_labyrinthes):
		labyrinthe_non_reconnu = True
		dico = dictionnaire_des_labyrinthes._dictionnaire
		while labyrinthe_non_reconnu:
			try:
				self.identifiant_du_labyrinthe = inputQ("Entrez un numéro de labyrinthe (ou h pour ouvrir le dictionnaire de labyrinthes) : ")
				while self.identifiant_du_labyrinthe 	== 'h':
					print(dictionnaire_des_labyrinthes)
					try:
						self.identifiant_du_labyrinthe = inputQ("Entrez un numéro de labyrinthe " + \
										"(ou h pour ouvrir le dictionnaire de labyrinthes) : ")
					except EvenementQuitter:
						raise EvenementQuitter
				
				try:
					for attribut_copy in dico[self.identifiant_du_labyrinthe].__dict__:
						self.__dict__[attribut_copy] = dico[self.identifiant_du_labyrinthe].__dict__[attribut_copy]
					labyrinthe_non_reconnu = False
				except:
					print("Le labyrinthe n'est pas reconnu. " + \
									"Veuillez saisir un identifiant du dictionnaire.")
			except EvenementQuitter:
				raise EvenementQuitter
		
		return self.labyrinthe
	
	def Sauver_symboles(self):
		try:
			SYMBOLES = DictionnaireDesSymboles(SYMBOLES_chemin)
			for symboles_connus in SYMBOLES.values() : 
				if len(self.symboles.items() & symboles_connus.items()) == len(symboles_connus):
					return
			
			nouvel_indice = str(max([int(x) for x in SYMBOLES.keys()]) + 1)
			SYMBOLES[nouvel_indice] = self.symboles
		except (FileNotFoundError, EOFError) as err:
			print("Le dictionnaire des symboles n'a pas pu ête trouvé.\n" + \
					"Un nouveau dictionnaire a été créé.")
			SYMBOLES = DictionnaireDesSymboles()
			SYMBOLES['1'] = symboles_default
			if len(self.symboles.items() & symboles_default.items()) != len(symboles_default):
				SYMBOLES['2'] = self.symboles
		
		SYMBOLES.Sauver(SYMBOLES_chemin)
	
	def Conversion_symboles(self):
		dictionnaire_conversion = {}
		for symboles_nom in symboles_default.keys():
			dictionnaire_conversion[self.symboles[symboles_nom]] = symboles_default[symboles_nom]
		
		labyrinthe_converti = self.labyrinthe
		for signe_nouveau, signe_default in dictionnaire_conversion.items():
			labyrinthe_converti = labyrinthe_converti.replace(signe_nouveau, signe_default)
		
		self.labyrinthe = labyrinthe_converti
