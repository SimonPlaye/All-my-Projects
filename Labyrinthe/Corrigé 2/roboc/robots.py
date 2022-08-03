# -*-coding:Utf-8 -*

from roboc import RobocError
from roboc.utils import symboles_default

from roboc.labyrinthes import Labyrinthes

class Robots(Labyrinthes):
	"""
	"""

	def find_robot(self):
		if type(self) == str:
			return str.find(self, symboles_default['robot'])
		else:
			return str.find(self.labyrinthe, symboles_default['robot'])
	
	def Position_du_robot(self):
		"""
		Calcul de la position du robot dans :aire_de_jeu:, s'il n'existe pas,
		et calcul de la position.
		
		:aire_de_jeu: est le labyrinthe dans lequel évolue le robot.
		"""
		
		analyse_position = self.labyrinthe[:Robots.find_robot(self.labyrinthe)]
		self.position_depart[0] = analyse_position.count('\n')
		self.position_depart[1] = len(analyse_position.split('\n')[-1])
	
	def PlacerRobotALEntree(self):
		"""
		Remplace le caractère d'entrée par le caractère robot et calcule
		la nouvelle posiiton du robot dans la grille du labyrinthe.
		"""
		self.labyrinthe = self.labyrinthe.replace(symboles_default['entree'],symboles_default['robot'])
		self.element_sous_robot = symboles_default['entree']
		self.Position_du_robot()
	
	def __init__(self, aire_de_jeu = ""):
		
		"""
		Initialise un robot.
		"""
		Labyrinthes.__init__(self)
	
		##On place le robot à l'entrée du labyrynthe de l':aire_de_jeu: 
		self.position_depart = [0, 0] #(y,x)
		self.element_sous_robot = ""
		if aire_de_jeu != "" :
			self.labyrinthe = aire_de_jeu
			self.PlacerRobotALEntree()
