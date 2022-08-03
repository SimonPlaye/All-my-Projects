# -*-coding:Utf-8 -*

from roboc import RobocError
from roboc.utils import INSTALL_path,\
						EvenementQuitter,\
						EvenementVictoire,\
						inputQ

from roboc.robots import Robots

class Mouvements(Robots):
	"""
	"""
	
	def __init__(self, aire_de_jeu = ""):
		"""
		Initialise les mouvements.
		"""
		Robots.__init__(self, aire_de_jeu)
		self.choix={}
		self.mouvements_autorises={}
		self.position_arrivee = [0, 0] #(y,x)
		return
	
	def Choix_directions(self):
		"""
		Remplit le dictionnaire de l'attribut choix.
		On récupère dans chaque direction, sous forme de 4 listes, les 
		éléments de labyrinthes.
		"""
		if self.position_depart[1] > 0:
			self.choix['O'] = self.tableau[self.position_depart[0]][self.position_depart[1] - 1::-1]
		else:
			self.choix['O'] = self.symboles['mur']
		
		if self.position_depart[1] < self.largeur:
			self.choix['E'] = self.tableau[self.position_depart[0]][self.position_depart[1] + 1:]
		else:
			self.choix['E'] = self.symboles['mur']
		
		if self.position_depart[0] > 0:
			self.choix['N'] = [ self.tableau[i][self.position_depart[1]] \
							for i in range(self.position_depart[0] - 1, -1, -1) ]
		else:
			self.choix['N'] = self.symboles['mur']
		
		if self.position_depart[0] < self.longueur :
			self.choix['S'] = [ self.tableau[i][self.position_depart[1]] \
							for i in range(self.position_depart[0] + 1, self.longueur + 1) ]
		else:
			self.choix['S'] = self.symboles['mur']
	
	def PropositionChoix(self):
		"""
		Évalue les choix possibles et retourne les choix qui ne bloque pas le robot.
		
		Returns: :choix_possible: liste de string de 1 caractère 'O', 'E', 'N' ou 'S' 
		"""
		
		direction_label = {}
		direction_label['N'] = "nord"
		direction_label['S'] = "sud"
		direction_label['E'] = "est"
		direction_label['O'] = "ouest"
		
		choix_possible = list()
		
		try:
			del self.choix['Q']
		except:
			pass
		
		for direction, chemin in self.choix.items():
			choix_message = ""
			element = str(chemin[0])
			if element == self.symboles['couloir']:
				choix_message = "(" + direction[0] + ") "
				choix_possible.append(direction)
				if direction in ['E', 'O']:
					choix_message += "Allez à l'" + direction_label[direction]
				else:
					choix_message += "Allez au " + direction_label[direction]
			
			elif element == self.symboles['porte']:
				choix_message = "(" + direction[0] + ") "
				choix_possible.append(direction)
				if direction in ['E', 'O']:
					choix_message += "Ouvrir la porte à l'" + direction_label[direction]
				else:
					choix_message += "Ouvrir la porte au " + direction_label[direction]
			
			elif element == self.symboles['sortie']:
				choix_message = "(" + direction[0] + ") "
				choix_possible.append(direction)
				if direction in ['E', 'O']:
					choix_message += "Sortir du labyrinthe par l'" + direction_label[direction]
				else:
					choix_message += "Sortir du labyrinthe par le " + direction_label[direction]
			
			elif element in [self.symboles['entree'], self.symboles['mur']]:
				pass
			
			elif element == self.symboles['robot']:
				raise RobocError.LabyrintheRobotUnique
			
			else:
				raise RobocError.LabyrintheElementInconnu(element)
			
			if choix_message != "":
				print(choix_message)
		
		self.mouvements_autorises = choix_possible
		return
	
	def RobotMouvements(self, decision):
		"""
		La fonction va évaluer la décision et déterminer quel mouvement 
		doit être réaliser.
		La :decision: doit commencer par 'O', 'E', 'S' ou 'N' sinon le
		robot ne bouge pas.
		Les caractères suivants de :decision: doivent être un nombre entier
		ou ':'. Un nombre fait déplacer le robot de ce nombre jusqu'au premier
		obstacle rencontré. ':' envoie à la position maximum dans la direction
		choisie.
		"""
		self.position_arrivee = list(self.position_depart)
		
		direction = decision[0].upper()
		if len(decision) > 1:
			if decision[1] == ":":
				intensite = len(self.choix[direction])
			else:
				try:
					intensite = int(decision[1:])
					if intensite == 0:
						raise ValueError
				except ValueError as err:
					raise RobocError.MouvementInvalide(str(decision[1:]))
		else:
			intensite = 1
		
		#Calcul de l'intensité effective du mouvement
		#chemin possible, c'est la plus grande distance de couloir
		#en prenant en compte l'intensite du déplassement
		#Cas paticulier de la porte, on ne peut pas aller plus loin que
		#la porte elle-même quand on la franchie
		if self.choix[direction][0] == self.symboles['porte']:
			chemin_possible = 'P'
			if intensite > 1:
				intensite = 1
				RobocError.MouvementObstacle(self.symboles['porte'])
		
		else:
			#si l'intensité est de 1 il ne peut pas y avoir (par mouvements_autorisés) de mur ou d'entree
			#ou de porte (par le cas précédent)
			chemin_possible = "".join(self.choix[direction][0:intensite]).split(self.symboles['mur'])[0]
			chemin_possible = chemin_possible.split(self.symboles['porte'])[0]
			chemin_possible = chemin_possible.split(self.symboles['entree'])[0]
			
			if chemin_possible.find(self.symboles['sortie']) != -1:
				self.labyrinthe = self.labyrinthe.replace(self.symboles['robot'], self.element_sous_robot)
				self.element_sous_robot = self.symboles['sortie']
				self.labyrinthe = self.labyrinthe.replace(self.symboles['sortie'], self.symboles['robot'])
				print(self.labyrinthe)
				raise EvenementVictoire
			
			if len(chemin_possible) < intensite:
				obstacle = self.choix[direction][len(chemin_possible)]
				intensite = len(chemin_possible)
				if decision[1] != ":":
					RobocError.MouvementObstacle(obstacle)
					RobocError.MouvementTropLong(intensite)
		
		#On calcule la position d'arrivée
		if direction == 'N':
			self.position_arrivee[0] -= intensite
		elif direction == 'S':
			self.position_arrivee[0] += intensite
		elif direction == 'O':
			self.position_arrivee[1] -= intensite
		elif direction == 'E':
			self.position_arrivee[1] += intensite
		
		#Réalisation du mouvement effectif
		self.tableau[self.position_depart[0]][self.position_depart[1]] = self.element_sous_robot
		self.element_sous_robot = chemin_possible[-1]#new
		
		self.tableau[self.position_arrivee[0]][self.position_arrivee[1]] = self.symboles['robot']
		new_labyrinthe = "\n".join(["".join(self.tableau[x]) for x in range(0, self.longueur + 1)])
		self.position_depart = list(self.position_arrivee)
		
		self.set_labyrinthe(new_labyrinthe)
