# -*-coding:Utf-8 -*
import pickle

from roboc import RobocError
from roboc.utils import INSTALL_path, \
						EvenementQuitter, \
						EvenementVictoire, \
						inputQ

from roboc.robots import Robots
from roboc.mouvements import Mouvements

PARTIES_chemin = INSTALL_path + '/RobocPartie'

class Parties(Mouvements, Robots):
	"""
	Une instance de partie ne vit que le temps de jouer la partie.
	En initialisant une nouvelle parie, on la lance automatiquement.
	"""
	def reprendre_partie(partie_a_recharger):
		try:
			with open(PARTIES_chemin, 'rb') as fichier:
				partie_a_recharger = pickle.Unpickler(fichier).load()
		except FileNotFoundError as err:
			raise FileNotFoundError(PARTIES_chemin)
		
		if partie_a_recharger.element_sous_robot in [partie_a_recharger.symboles['sortie'], ""]:
			commande = ""
			while commande not in ['O', 'N', 'Q']:
				commande = inputQ("La partie était terminé\nCommencez une nouvelle partie ? (O/N)\n").upper()
		
			if commande == 'O':
				partie_a_recharger.Choix_du_labyrinthe(partie_a_recharger.dico)
			elif commande == 'Q':
				raise EvenementQuitter
			elif commande == 'N':
				raise RobocError.PartieTermine
		else:
			pass
		
		return partie_a_recharger
	
	def sauvegarder_la_partie(self):
		with open(PARTIES_chemin, 'wb') as fichier:
			pickle.Pickler(fichier).dump(self)
	
	def Jouer(self):
		"""
		Moteur de partie : déclénche une partie et gère les cas
		"""
		self.partie_en_cours = True
		while self.partie_en_cours:
			print(self.labyrinthe)
			try:
				self.Choix_directions()
			except EvenementQuitter:
				raise EvenementQuitter
			self.PropositionChoix()
			direction = ""
			while direction not in self.mouvements_autorises:
				try:
					choix_joueur = inputQ("Que souhaitez vous faire ?\n")
				except EvenementQuitter :
					print("Vous avez arrêté la partie.")
					raise EvenementQuitter
				try:
					direction = choix_joueur[0].upper()
				except :
					pass
	
			try:
				self.RobotMouvements(choix_joueur)
			except RobocError.MouvementInvalide as err:
				print("Le mouvement n'est pas valide. Ceci n'est pas valide : " + err.args[0])
			except EvenementVictoire as err:
				print("BRAVO ! Vous êtes sorti du labyrinthe.")
				self.partie_en_cours = False
				self.sauvegarder_la_partie()
				break
	
			self.sauvegarder_la_partie()
	
		return False
	
	def __init__(self, dictionnaire_des_labyrinthes, nouvelle_partie = True):
		self.partie_en_cours = False
		self.dico = dictionnaire_des_labyrinthes
		if len(dictionnaire_des_labyrinthes._dictionnaire) > 0 and nouvelle_partie:
			try:
				Mouvements.__init__(self,"")
				self.labyrinthe = self.Choix_du_labyrinthe(dictionnaire_des_labyrinthes)
			except EvenementQuitter:
				raise EvenementQuitter
	
			if self.labyrinthe != "" and self.find_robot() == -1:
				self.PlacerRobotALEntree()
			Mouvements(self.labyrinthe)
			self.Jouer()
	
		elif not (nouvelle_partie) :
			#Labyrinthes.__init__(self)
			Mouvements.__init__(self)#, self.labyrinthe)
			try:
				self = self.reprendre_partie()
				if self.labyrinthe != "" and self.find_robot() == -1:
					self.PlacerRobotALEntree()
				self.Jouer()
			except FileNotFoundError as err:
				raise FileNotFoundError(err.args[0])
			except RobocError.PartieTermine:
				raise RobocError.PartieTermine
			except EvenementQuitter:
				raise EvenementQuitter
	
		else:
			print("Veuillez charger un labyrinthe dans le dictionnaire des " + \
						"labyrinthes avant de pouvoir commencer votre première partie.")

