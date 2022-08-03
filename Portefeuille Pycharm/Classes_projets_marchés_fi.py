from random import *
import matplotlib.pyplot as plt
import numpy as np
from math import *
import pandas as pd

"""Classe définissant les caractéristiques d'un agent - market maker ou trader"""


class Agent:

    # Atttribut de tous les agents
    def __init__(self, iter):
        self.pnl = 100
        self.iter = iter
        self.dict_agents = {}
        self.nb_actions = 0
        self.capital = self.pnl
        self.valeur_action = 0

        # on conserve l'évolution du PnL
        self.list_pnl = np.array([])
        self.list_actions = np.array([])
        self.list_capital = np.array([])

    # méthode chargée de stocker tous les agents de l'économie par catégorie, autres que le market maker
    def store_agents(self, name, agent):
        if name in self.dict_agents:
            self.dict_agents[name].append(agent)
        else:
            self.dict_agents[name] = [agent]

    # méthode chargée de faire acheter des actions au trader
    def buy(self, prix, nb_actions, bid):
        self.pnl -= nb_actions * prix
        self.nb_actions += nb_actions
        self.valeur_action = prix
        self.refresh(bid)

    # méthode chargée de faire vendre des actions au trader
    def sold(self, prix, nb_actions, bid):
        self.pnl += prix * nb_actions
        self.nb_actions -= nb_actions
        self.valeur_action = bid
        self.refresh(bid)

    # Méthode chargée d'actualiser les listes de PnL et d'actions détenues
    def refresh(self, bid):
        self.list_pnl = np.append(self.list_pnl, [self.pnl])
        self.list_actions = np.append(self.list_actions, [self.nb_actions])
        self.capital = self.pnl + self.nb_actions * bid
        self.list_capital = np.append(self.list_capital, [self.capital])


"""Classe définissant le comportement du market maker"""


class MarketMaker(Agent):

    # méthode qui défini un bid, un ask, le PnL du market maker et l'évolution des cours
    def __init__(self, iter):
        Agent.__init__(self, iter)
        self.ask = 10
        self.bid = self.ask * uniform(0.995, 0.999)
        self.iter = iter  # nombre de jour de simulation
        self.pnl_initial = 100

        # les listes suivantes stockent les différentes valeurs du Bid et du Ask
        self.list_ask = np.array([])
        self.list_bid = np.array([])
        self.list_action = np.array([])

    # méthode chargée d'actualiser les prix du market maker
    def refresh_price(self, temps_ecoule, baissier=True):
        if baissier:
            self.ask = 10 - self.__share_price(temps_ecoule)
        else:
            self.ask = 10 + self.__share_price(temps_ecoule)
        self.bid = self.ask * uniform(0.98, 0.99)
        self.list_ask = np.append(self.list_ask, [self.ask])  # on stock le ask dans la liste des ask
        self.list_bid = np.append(self.list_bid, [self.bid])
        self.list_action = np.append(self.list_action, [self.nb_actions])

    # Ici on cherche à représenter le prix du ask avec une fonction
    # La ponderation sert à adapter la courbe au nombre d'iterations
    def __share_price(self, x):
        iterations = self.iter
        ponderation = 1 / iterations
        y = sqrt(75 * x * ponderation * uniform(1, 1.03)) - sqrt(10 * x * ponderation) + cos(
            20 * ponderation * x * uniform(1, 1.05)) + cos(ponderation * x * uniform(1, 1.07) + 5) * sin(
            -50 * ponderation * x * uniform(1, 1.03) - 15) * cos(3 * ponderation * x - 7) - sin(
            7 * ponderation * x * uniform(1, 1.01) + 3) * cos(10 * ponderation * x * uniform(1, 1.02) + 4) * cos(
            -9 * ponderation * x * uniform(1, 1.09))
        ask_final = self.__intelligent(y, x)
        return (ask_final)

    # Actualise le PnL du market maker et son nombre d'action après chaque itération sur le marché
    # Remarque : les actions achetees par les Traders sont les actions vendues par le market maker (pareil pour la vente)
    def decision(self, ventes, achats):
        self.pnl += ventes * self.ask - achats * self.bid
        self.nb_actions += achats - ventes
        self.list_pnl = np.append(self.list_pnl, [self.pnl])
        self.capital = self.pnl + self.bid * self.nb_actions
        self.list_capital = np.append(self.list_capital, [self.capital])

    # méthode chargée de rendre le Market Maker intelligent en ajustant le Bid/Ask en fonction du nombre d'actions qu'il possède
    # Pour cela, on étudie l'évolution du nb d'actions dans le portefeuille du market maker
    # Dans cette optique, le PnL initial du Trader fou est très faible sinon il fait trop varier le portefeuille du MM
    def __intelligent(self, ask, iterations):
        if iterations > 2:  # il faut qu'on ait au moins 2 actions dans notre liste de nb d'actions pour étudier leur évolution
            val_1 = self.list_action[iterations - 1]  # nb d'action hier
            val_2 = self.list_action[iterations - 2]  # nb d'action avant hier
            variation = (val_1 - val_2) / abs(val_2)
            retour = ask - variation * (np.random.randn() + 1)
            return (
                retour)  # note : le choix du + 1 est voulu: sinon le cours peut varier énormément par période (essayer avec +3 ou +2 c'est rigolo)
        else:
            return (ask)

    def __repr__(self):
        return ("MarketMaker")


"""Classe définissant le comportement du premier trader
Ce trader achète les jours pairs et vend les jours impairs"""


class TraderFou(Agent):

    # méthode qui créé le trader fou
    def __init__(self, iter, numero):
        Agent.__init__(self, iter)
        self.numero = numero
        self.pnl_initial = 5  # Très faible pour éviter qu'ils influencent trop le court de l'action

    # Défini ce que va faire le Trader en fonction du jour
    def decision(self, jour, ask, bid):
        if jour % 2 == 0:
            # il achète le maximum d'action qu'il peut avec son PnL
            Agent.buy(self, ask, self.pnl / ask, bid)
            return ("achat")
        else:
            Agent.sold(self, bid, self.nb_actions, bid)
            return ("vente")

    def __repr__(self):
        return ("TraderFou" + str(self.numero))


"""Classe définissant le comportement d'un Trader prudent.
Ce Trader une achète une action au début et ne la revend
que si le cours de l'action a monté de y% """
"""Capital initial aléatoire compris entre 50 et 150"""
"""Ce trader achète une action x jour après avoir revendue son action"""


class CarefulTrader(Agent):

    # Création de l'agent
    def __init__(self, iter, numero, baissier=True):
        Agent.__init__(self, iter)
        self.valeur_action = 0
        self.duree_attente = randint(0, 4)  # durée pendant lequel le trader attend avant de racheter des actions
        self.temps_attente = 0
        self.numero = numero  # défini duquel trader il s'agit
        self.pnl_initial = randrange(50, 150, 10)
        self.pnl = self.pnl_initial  # permettra de calculer la rentabilité du trader
        self.y = 1 + abs(np.random.randn() * 0.025 + 0.075)

    # méthode qui défini le comportement de ce Trader
    def decision(self, jour, ask, bid):

        # Le trader attend une opportunité d'achat
        if self.valeur_action == 0:
            # le trader ne souhaite pas acheter tout de suite une action
            if self.temps_attente < self.duree_attente:
                self.temps_attente += 1
                Agent.refresh(self, bid)


            # il achète le nombre maximal d'action qu'il peut avec son pnl
            else:
                Agent.buy(self, ask, self.pnl / ask, bid)
                return ("achat")

        # le trader attend de vendre ses actions
        else:
            # il peut effectivement les vendre
            if self.y * self.valeur_action <= bid:
                Agent.sold(self, bid, self.nb_actions, bid)
                self.valeur_action = 0
                return ("vente")
            else:
                Agent.refresh(self, bid)

    def __repr__(self):
        return ("CarefulTrader" + str(self.numero))


"""Classe représentant un Trader qui n'achète que si le cours a diminué de x%
et ne revend que s'il a augmenté de y%
x, y et le capital initial son initiés de façon aléatoire"""


class CleverTrader(Agent):

    def __init__(self, iter, numero, baissier=True):
        Agent.__init__(self, iter)

        if baissier:
            self.valeur_action = 10 - abs(np.random.randn() * 2)
        else:
            self.valeur_action = 10 + abs(
                np.random.randn() * 2)  # on valorise à 12 pour être sûr que les traders vont acheter une action au départ
        self.numero = numero
        self.pnl_initial = randrange(50, 150, 10)
        self.pnl = self.pnl_initial
        self.x = 1 - abs(np.random.randn() * 0.025)
        self.y = 1 + abs(np.random.randn() * 0.025 + 0.075)

    # méthode représentant le comportement de ce Trader sur le marché
    def decision(self, jour, ask, bid):

        # il achète des actions
        if self.x * self.valeur_action >= ask and self.nb_actions == 0:
            Agent.buy(self, ask, self.pnl / ask, bid)
            return ("achat")

        # il les vend
        elif self.valeur_action * self.y <= bid and self.nb_actions != 0:
            Agent.sold(self, bid, self.nb_actions, bid)
            return ("vente")

        else:
            Agent.refresh(self, bid)

    def __repr__(self):
        return (f'CleverTrader{self.numero}')

"""Classe définissant un Trader adoptant une gestion passive:
il achète tout ce qu'il peut le premier jour et revend tout le dernier jour"""

class PassiveTrader(Agent):

    def __init__(self, iter, numero):
        Agent.__init__(self, iter)
        self.numero = numero
        self.pnl_initial = randrange(50, 150, 10)
        self.pnl = self.pnl_initial

    # methode représentant le comportement du trader sur le marché
    def decision(self, jour, ask, bid):

        if jour == 0:
            Agent.buy(self, ask, self.pnl / ask, bid)
            return ("achat")
        elif jour == 999:
            Agent.sold(self, bid, self.nb_actions, bid)
            return ("vente")
        else:
            Agent.refresh(self, bid)

    def __repr__(self):
        return (f'PassiveTrader{self.numero}')


"""Classe définissant un Trader dont le comportement est le suivant:
        - S'il a des actions, il les vend si le cours de l'action diminue beaucoup ou s'il augmente un peu
        - Sinon, il achète des actions si le cours augmente ou s'il diminue beaucoup"""


class NormalTrader(Agent):

    def __init__(self, iter, numero, baissier=True):
        Agent.__init__(self, iter)
        self.numero = numero
        if baissier:
            self.valeur_action = -abs(np.random.randn() * 2) + 10  # seuil de référence de départ
        else:
            self.valeur_action = abs(np.random.randn() * 2) + 10
        self.x = abs(np.random.randn() * 0.025)  # seuil si le cours de l'action diminue ou augmente un peu
        self.y = abs(np.random.randn() * 0.1)  # seuil si le cours de l'action diminue ou augmente beaucoup
        self.pnl_initial = randrange(50, 150, 10)
        self.pnl = self.pnl_initial

    def decision(self, jour, ask, bid):

        # S'il a des actions:
        if self.nb_actions > 0:
            # Si le cours diminue beaucoup
            if bid < self.valeur_action * (1 - self.y):
                Agent.sold(self, bid, self.nb_actions, bid)
                return ("vente")
            # si le cours de l'action augmente un peu
            elif bid > self.valeur_action * (1 + self.x):
                Agent.sold(self, bid, self.nb_actions, bid)
                return ("vente")
            else:
                Agent.refresh(self, bid)
        # S'il n'en n'a pas
        else:
            # Si le cours diminue beaucoup
            if ask < self.valeur_action * (1 - self.y):
                Agent.buy(self, ask, self.pnl / ask, bid)
                return ("achat")
            # Si le cours augmente beaucoup
            elif ask > self.valeur_action * (1 + self.y):
                Agent.buy(self, ask, self.pnl / ask, bid)
                return ("achat")
            else:
                Agent.refresh(self, bid)

    def __repr__(self):
        return (f"NormalTrader{self.numero}")


"""Classe définissant un Trader qui peut prendre la décision de vendre à découvert des actions
    son comportement est définit ainsi:
        - Si le marché commence à grimper de x euros il achète des actions, il les revend en totalité
          soit si le cours à augmenter de y euros
          soit si le cours à diminuer de z euros
        - Si le marché commence à diminuer de x euros il vend des actions, il les rachète en totalité
          soit si le cours à augmenter de y euros
          soit si le cours à diminuer de z euros
    lorsqu'il achète des actions, il le fait avec la totalité de son PnL
    lorsqu'il les vend à découvert, il le fait pour un montant correspondant à 100% de son PnL
    Ne pas utiliser une valeur en % pour savoir si on achète/vend permet à ce Trader d'effectuer autant d'échange
    sur un marché en hausse qu'en baisse"""


class ShortTrader(Agent):

    def __init__(self, iter, numero, baissier=True):
        Agent.__init__(self, iter)
        self.numero = numero
        if baissier:
            self.valeur_action = -abs(np.random.randn()) + 10
        else:
            self.valeur_action = abs(np.random.randn()) + 10
        self.pnl_initial = randrange(50, 150, 10)
        self.pnl = self.pnl_initial
        self.x = abs(np.random.randn() * sqrt(0.5))
        self.y = self.x + abs(np.random.randn()) + 2
        self.z = abs(np.random.randn()) * 3

    def decision(self, jour, ask, bid):

        # il a des actions dans son portefeuille
        if self.nb_actions > 0:
            # le cours a suffisamment augmenté pour que le trader les revende
            if bid > self.valeur_action + self.y:
                Agent.sold(self, bid, self.nb_actions, bid)
                return ("vente")
            # le cours a chuté
            elif bid < self.valeur_action - self.z:
                Agent.sold(self, bid, self.nb_actions, bid)
                return ("vente")
            else:
                Agent.refresh(self, bid)

        # Le trader a shorté des actions
        elif self.nb_actions < 0:
            # le cours a augmenté
            if bid > self.valeur_action + self.z:
                Agent.buy(self, ask, -self.nb_actions, bid)
                return ("achat")
            # le cours a suffisament diminué
            elif bid < self.valeur_action - self.y:
                Agent.buy(self, ask, -self.nb_actions, bid)
                return ("achat")
            else:
                Agent.refresh(self, bid)

        # le trader n'a aucune action dans son portefeuille
        else:
            # le cours augmente assez pour qu'il en achète
            if bid > self.valeur_action + self.x:
                Agent.buy(self, ask, self.pnl / ask, bid)
                return ("achat")
            # le cours diminue pour qu'il en short
            elif bid < self.valeur_action - self.x:
                Agent.sold(self, bid, self.pnl / ask, bid)
                return ("vente")
            else:
                Agent.refresh(self, bid)

    def __repr__(self):
        return (f"ShortTrader{self.numero}")


"""Classe définissant un Trader au comportement qui mélange celui d'un NormalTrader et d'un CleverTrader
    mais qui ne s'intéresse pas à l'évolution relative des prix (hausse ou 
    baisse en %) mais à leur évolution absolue (en euros) ainsi:
        - Il achète si le cours commence à diminuer de x euros
        - Il revend lorsque le cours aura augmenté de y euros
        - Si le cours diminue de z euros (lorsqu'il chute brutalement), il se débarasse de ses titres"""


class PriceTrader(Agent):

    def __init__(self, iter, numero, baissier=True):
        Agent.__init__(self, iter)
        self.numero = numero
        if baissier:
            self.valeur_action = -abs(np.random.randn() * 2) + 10  # seuil de référence de départ
        else:
            self.valeur_action = abs(np.random.randn() * 2) + 10
        self.x = abs(np.random.randn()) + 0.5
        self.y = self.x + abs(np.random.randn()) + 1
        self.z = abs(np.random.randn())
        self.pnl_initial = randrange(50, 150, 10)
        self.pnl = self.pnl_initial

    def decision(self, jour, ask, bid):

        # S'il a des actions:
        if self.nb_actions > 0:
            # Si le cours diminue beaucoup
            if bid < self.valeur_action - self.z:
                Agent.sold(self, bid, self.nb_actions, bid)
                return ("vente")
            # si le cours de l'action augmente suffisamment
            elif bid > self.valeur_action + self.y:
                Agent.sold(self, bid, self.nb_actions, bid)
                return ("vente")
            else:
                Agent.refresh(self, bid)
        # S'il n'en n'a pas
        else:
            # Si le cours diminue suffisamment
            if ask < self.valeur_action - self.x:
                Agent.buy(self, ask, self.pnl / ask, bid)
                return ("achat")
            else:
                Agent.refresh(self, bid)

    def __repr__(self):
        return (f"PriceTrader{self.numero}")


"""Classe définissant le marché"""


class StockMarket():

    # création de la classe
    def __init__(self, iterations):
        self.iter = iterations
        self.data = {}  # permet de stocker la liste des bid, des ask et des pnl par stratégie
        self.agents = {}  # en clé les stratégies, en valeur les objets pour chacune de ces stratégies
        self.actions_vendues = 0  # toutes les actions vendues par les traders sur une itération
        self.actions_achetees = 0
        self.df = ""  # df qu'on va afficher à la fin de la simulation
        self.list_agents = ""  # futur objet ayant pour but de lister les agents avec la méthode défini dans Agent

    # lance le marché
    def run_market(self, nb_agents, baissier=True):

        if nb_agents < 2:
            return ("Erreur : il faut au minimum 2 agents")

        # Création des agents
        else:
            self.list_agents = Agent(self.iter)
            market_maker = MarketMaker(self.iter)
            self.list_agents.store_agents("MarketMaker", market_maker)  # permet de stocker les agents dans une liste

            compteur = 1
            # on répartit les différents agents
            for j in range(nb_agents - 1):
                if j < 1:
                    self.agents["TraderFou" + str(compteur)] = TraderFou(self.iter, compteur)
                    self.list_agents.store_agents("TraderFou", self.agents["TraderFou" + str(compteur)])
                    compteur += 1
                    if j == 0:
                        compteur = 1

                elif j > 0 and j <= int(0.2 * nb_agents):
                    self.agents["CarefulTrader" + str(compteur)] = CarefulTrader(self.iter,
                                                                                 compteur)  # on stock cet agent particulier
                    self.list_agents.store_agents("CarefulTrader", self.agents["CarefulTrader" + str(
                        compteur)])  # on stock cet agent particulier avec tous les autres agents ayant la même stratégie
                    compteur += 1

                    if j == int(0.2 * nb_agents):  # on a fini de créer des CarefulTrader
                        compteur = 1

                elif j > int(0.2 * nb_agents) and j <= int(0.3 * nb_agents):
                    self.agents["CleverTrader" + str(compteur)] = CleverTrader(self.iter, compteur, baissier)
                    self.list_agents.store_agents("CleverTrader", self.agents["CleverTrader" + str(compteur)])
                    compteur += 1
                    if j == int(0.3 * nb_agents):
                        compteur = 1

                elif j > int(0.3 * nb_agents) and j <= int(0.5 * nb_agents):
                    self.agents["NormalTrader" + str(compteur)] = NormalTrader(self.iter, compteur, baissier)
                    self.list_agents.store_agents("NormalTrader", self.agents["NormalTrader" + str(compteur)])
                    compteur += 1
                    if j == int(0.5 * nb_agents):
                        compteur = 1
                elif j > int(0.5 * nb_agents) and j <= int(0.7 * nb_agents):
                    self.agents["ShortTrader" + str(compteur)] = ShortTrader(self.iter, compteur, baissier)
                    self.list_agents.store_agents("ShortTrader", self.agents["ShortTrader" + str(compteur)])
                    compteur += 1
                    if j == int(0.7 * nb_agents):
                        compteur = 1
                elif j > int(0.7 * nb_agents) and j <= int(0.9 * nb_agents):
                    self.agents["PriceTrader" + str(compteur)] = PriceTrader(self.iter, compteur, baissier)
                    self.list_agents.store_agents("PriceTrader", self.agents["PriceTrader" + str(compteur)])
                    compteur += 1
                    if j == int(0.9 * nb_agents):
                        compteur = 1
                else:
                    self.agents["PassiveTrader" + str(compteur)] = PassiveTrader(self.iter, compteur)
                    self.list_agents.store_agents("PassiveTrader", self.agents["PassiveTrader" + str(compteur)])
                    compteur += 1

            # On lance le marché
            for i in range(self.iter):

                # Création du PnL du market maker, du bid et du ask
                market_maker.refresh_price(i, baissier)

                # on récupère le bid et le ask auprès du market maker
                ask = market_maker.ask
                bid = market_maker.bid

                # Pour chaque agent:
                for trader in self.agents.values():
                    operation = trader.decision(i, ask, bid)
                    if operation == "achat":
                        self.actions_achetees += 1  # achetées par les traders
                    elif operation == "vente":
                        self.actions_vendues += 1

                market_maker.decision(self.actions_achetees, self.actions_vendues)

                self.actions_vendues = 0
                self.actions_achetees = 0

            self.agents["MarketMaker"] = market_maker
            self.__store_data(market_maker)

    # Sauvegarde les données sous forme d'un dictionnaire
    def __store_data(self, market_maker):

        self.data["Bid"] = list(market_maker.list_bid)
        self.data["Ask"] = list(market_maker.list_ask)

        for key, value in self.agents.items():
            self.data[key + str(" PnL")] = list(value.list_pnl)

    # Convertit en data frame les données sauvées
    def df_data(self):
        self.df = pd.DataFrame(self.data)
        return (self.df)

    # Enregistre les données au format csv
    def data_to_csv(self, name):
        self.df.to_csv(name + str(".csv"))

    # Retourne toutes les données interessantes
    def return_data(self):
        return (self.list_agents.dict_agents)


"""Classe chargée de mettre en place un tirage de plusieurs simulations du système"""


class Simulation:

    # Création des attributs qui permettrons de stocker les résultats des simulations
    def __init__(self):
        self.data = {}  # dictionnaire des simulations avec en clé la simulation i et en valeur un dictionnaire des stratégies de cette simulation (détails plus bas)
        self.output = {}  # dictionnaire qui servira de df, en clé la stratégie, en valeur une liste contenant la rentabilité, le nombre d'agents... toutes les données agrégées intéressantes de cette simulation
        self.list_outputs = []  # liste de tous les self.output, sert à faire une agrégation globale de toutes les simulations
        self.global_output = ""  # futur df ressemblant à self.output sauf qu'il rassemble toutes les simulations
        self.iter = 1000
        self.all_pnl = []  # liste composée de dictionnaires pour chaque simulation eux-memes ayant pour clé une stratégie et pour valeur la liste des pnl moyens par itération de cette stratégie
        self.list_pnl = []  # variable qu'on va renvoyer pour afficher le graphique sur flask
        self.all_ask = ""  # cours moyen du ask pour toutes les simulations
        self.all_bid = ""  # pareil mais pour le bid
        self.performance = ""  # DataFrame avec en colonne les stratégies en ligne les outputs intéressants (rentabilité, nombre de traders...)
        self.best_performance = ""  # DataFrame des meilleures stratégies

    # run le nombre de fois voulu notre système avec un certain nombre d'agent
    # Par défaut le marché a une tendancce baissière, on peut choisir une tendance haussière avec baissier = False
    def run(self, nb_agents, nb_simulations, baissier=True):

        for i in range(nb_simulations):
            # simule un marché boursier avec un certain nombre d'agents choisi
            stock_market = StockMarket(self.iter)
            stock_market.run_market(nb_agents, baissier)

            # enregistre toutes les données pour chaque simulation
            # Il s'agit d'un dictionnaire de dictionnaire :
            # Le premier dictionnaire a pour clé la simulation i et pour valeur le dictionnaire contenant les données de cette simulation
            # Ce deuxième dictionnaire a pour clé chaque type de stratégie de la simulation i et en valeur les agents de cette stratégie (contenu dans une liste)
            data = stock_market.return_data()
            self.data["Simulation " + str(i)] = data
            df = self.__stock_output(data)
            self.list_outputs.append(df)

    # Méthode chargée de stocker les outputs pour une simulation
    # Elle retourne le DF qui a, en colonne, les stratégies, en ligne les outputs (rentabilité, nombre d'agent, max drawdown...)
    def __stock_output(self, data_simulation):

        list_index = ["Capital initial", "Capital final", "Rentabilite sur la periode en %", "Nombre d'agents",
                      "PnL min", "PnL max", "Max drawdown en %", "Evolution du cours du Bid en %",
                      "Performance par rapport au Bid en %", "Evolution du cours du Ask en %",
                      "Performance par rapport au Ask en %"]  # liste des index pour le dataframe

        dic_pnl = {}  # en clé les stratégies, en valeur la liste des PnL moyen au cours du temps pour cette stratégie

        for key, value in data_simulation.items():

            if key == "MarketMaker":
                bid = value[0].list_bid
                ask = value[0].list_ask

            self.output[key] = [0 for i in range(11)]
            dic_pnl[key] = []  # on va stocker la liste des PnL moyens par stratégie
            nb_agents = 0
            for i in value:
                if type(dic_pnl[key]) == list:  # première itération sur cette stratégie
                    dic_pnl[key] = i.list_capital
                else:
                    # on ajoute la liste des pnl d'un trader particulier à la liste de la stratégie
                    dic_pnl[key] = np.add(dic_pnl[key], i.list_capital)

                self.output[key][0] += i.pnl_initial  # somme des capitaux initiaux par stratégie
                self.output[key][1] += i.capital  # somme des capitaux finaux
                self.output[key][2] += (i.capital - i.pnl_initial) / i.pnl_initial  # somme des rentabilités
                self.output[key][3] = int(len(value))  # nb d'agents pour chaque stratégie
                self.output[key][4] += np.amin(i.list_pnl)  # somme des PnL mimimum par stratégie
                self.output[key][5] += np.max(i.list_pnl)  # somme des PnL maximaux par stratégie
                nb_agents += 1

            self.output[key][0] = self.output[key][0] / nb_agents  # capitaux initiaux moyen par stratégie
            self.output[key][1] = self.output[key][1] / nb_agents  # capitaux finaux moyen par stratégie
            self.output[key][2] = self.output[key][2] * 100 / nb_agents  # rentabilité moyenne
            self.output[key][4] = self.output[key][4] / nb_agents  # pnl minimum moyen
            self.output[key][5] = self.output[key][5] / nb_agents  # pnl max moyen
            self.output[key][6] = ((self.output[key][5] - self.output[key][4]) / self.output[key][
                5]) * 100  # max drawdown
            self.output[key][7] = ((bid[-1] - bid[0]) / bid[0]) * 100  # évolution du bid en %
            self.output[key][8] = self.output[key][2] - self.output[key][7]  # performance par rapport au bid
            self.output[key][9] = ((ask[-1] - ask[0]) / ask[0] * 100)  # évolution du ask
            self.output[key][10] = self.output[key][2] - self.output[key][9]  # Performance par rapport au ask
            dic_pnl[key] = dic_pnl[key] / nb_agents  # on détermine la liste moyenne des pnl de cette stratégie

        self.all_pnl.append(dic_pnl)  # on stock les résultats de cette simulation dans une liste
        df = pd.DataFrame(self.output, index=list_index)
        pd.options.display.float_format = "{:,.2f}".format  # affiche les données avec 2 décimales
        self.performance = df
        return (df)

    # Méthode chargée d'agréger les outputs de toutes les simulations, de les sauvegarder dans un csv et de les afficher
    # sous forme de data frame
    # Le data frame affiché fait office de dashboard
    def dashboard(self):
        self.global_output = sum(self.list_outputs) / len(self.list_outputs)
        self.__market_evolution()
        self.__pnl_evolution()
        return (self.global_output)



    # Méthode chargée d'afficher la courbe moyenne des prix du market maker pour chaque simulation
    def __market_evolution(self):

        list_bid = []
        list_ask = []

        # On parcourt chacune des simulations
        for key, value in self.data.items():
            # on récupère chaque objet market maker
            market_maker = value["MarketMaker"][0]
            list_bid.append(market_maker.list_bid)
            list_ask.append(market_maker.list_ask)

        global_bid = sum(list_bid) / len(list_bid)
        global_ask = sum(list_ask) / len(list_ask)

        self.all_ask = global_ask
        self.all_bid = global_bid

        plt.ylabel("Prix de l'action en €")
        plt.xlabel("Dates")
        plt.title('Evolution du Bid et du Ask moyen')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), global_bid, 'r', label='Bid')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), global_ask, label='Ask')
        plt.legend()
        plt.show()

    # méthode chargée d'afficher les PnL moyens des différentes stratégies au cours du temps
    def __pnl_evolution(self):
        nb_simulation = len(self.all_pnl)
        pnl_CT = []  # Careful trader
        pnl_ClT = []  # clever trader
        pnl_PT = []  # PassiTrader
        pnl_NT = []
        pnl_ST = []
        pnl_PrT = []
        compteur = 0
        for i in self.all_pnl:
            for cle, valeur in i.items():
                if cle == "CarefulTrader":
                    if compteur == 0:
                        pnl_CT = valeur
                    else:
                        pnl_CT = np.add(pnl_CT, valeur)
                elif cle == "CleverTrader":
                    if compteur == 0:
                        pnl_ClT = valeur
                    else:
                        pnl_ClT = np.add(pnl_ClT, valeur)
                elif cle == "PassiveTrader":
                    if compteur == 0:
                        pnl_PT = valeur
                    else:
                        pnl_PT = np.add(pnl_PT, valeur)
                elif cle == "NormalTrader":
                    if compteur == 0:
                        pnl_NT = valeur
                    else:
                        pnl_NT = np.add(pnl_NT, valeur)
                elif cle == "ShortTrader":
                    if compteur == 0:
                        pnl_ST = valeur
                    else:
                        pnl_ST = np.add(pnl_ST, valeur)
                elif cle == "PriceTrader":
                    if compteur == 0:
                        pnl_PrT = valeur
                    else:
                        pnl_PrT = np.add(pnl_PrT, valeur)

            compteur = -1
        pnl_CT = pnl_CT / nb_simulation
        pnl_ClT = pnl_ClT / nb_simulation
        pnl_PT = pnl_PT / nb_simulation
        pnl_NT = pnl_NT / nb_simulation
        pnl_ST = pnl_ST / nb_simulation
        pnl_PrT = pnl_PrT / nb_simulation

        # on stock les listes de tous les Pnl par stratégie dans une liste
        self.list_pnl.append(pnl_CT)
        self.list_pnl.append(pnl_ClT)
        self.list_pnl.append(pnl_PT)
        self.list_pnl.append(pnl_NT)
        self.list_pnl.append(pnl_ST)
        self.list_pnl.append(pnl_PrT)

        plt.ylabel("PnL en euros")
        plt.xlabel("Dates")
        plt.title('Evolution du PnL par stratégie')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), pnl_CT, 'g', label='Careful Trader')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), pnl_ClT, 'r', label='Clever Trader')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), pnl_PT, 'm', label='Passive Trader')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), pnl_NT, 'y', label='Normal Trader')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), pnl_ST, 'k', label='Short Trader')
        plt.plot(np.linspace(0, self.iter - 1, num=self.iter), pnl_PrT, 'b', label='Price Trader')

        plt.legend()
        plt.show()

    # Méthode chargée d'afficher la meilleure stratégie selon différents critères
    # On ne compte pas le fait d'être Market Maker comme étant une stratégie
    def __best_strategie(self):

        df = self.global_output.transpose()  # On inverse ligne et colonne du df agréger
        df.drop("MarketMaker", axis=0, inplace=True)  # on enlève la ligne correspondant au Market Maker

        min_drawdown = df.iloc[:, 6].idxmin(0)  # On récupère l'index du minimum de la colonne "Max drawdown"

        df_bis = df[["Rentabilite sur la periode en %", "Performance par rapport au Bid en %",
                     "Performance par rapport au Ask en %"]]  # On récupère les colonnes en %
        df_bis = df_bis.idxmax(
            axis=0).values  # On récupère les index (qui sont nos stratégies) correspondants au maximum de chacune de ces colonnes
        df_bis = df_bis.tolist()  # on convertit le df précédent en liste
        df_dict = {'Best Strategy': [
                                        min_drawdown] + df_bis}  # dictionnaire regroupant le nom de chaque stratégie qui est la meilleure possible
        index = ["Max Drawdown", "Rentabilite", "Performance par rapport au Bid", "Performance par rapport au Ask"]
        df_final = pd.DataFrame(df_dict, index=index)  # on en fait un df avec pour index les colonnes en %
        self.best_performance = df_final
        return (df_final)

    # Méthode chargée de lancer les méthodes best_strategie et market_evolution
    # Repond à la question : "Proposer une étude des données générés par son système"
    def study_of_data(self):

        df = self.__best_strategie()
        return (df)

    # renvoie les données pour flask
    def data_for_flask(self):
        return (self.performance, self.best_performance, self.all_ask, self.all_bid, self.list_pnl)


from flask import Flask, render_template, request
import io
import base64
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('Agg') #sinon error Run time loop in the main thread

plt.rcParams['figure.figsize'] = (15, 5)  # défini la taille de la figure matplotlib


def application_web():
    app = Flask(__name__)

    def collect_data(agents, simulation, tendance):
        modele = Simulation()
        modele.run(agents, simulation, tendance)
        modele.dashboard()
        modele.study_of_data()
        return modele.data_for_flask()

    @app.route('/', methods=('POST', 'GET'))
    def index():
        trend = ["Baisse", "Hausse"]
        return render_template("index_marche_fi.html", tendance=trend)

    @app.route('/print_data', methods=('POST', 'GET'))
    def print_data():

        trend = ["Baisse", "Hausse"]

        # on récupère les données entrées par l'utilisateur
        if request.method == "POST":  # des données ont bien été rentrées
            values = request.form.to_dict()
        else:
            return render_template("index_marche_fi.html", tendance=trend)

        # cas où on n'a pas choisi un nombre d'agents et un nombre de simulations : on reste sur la page d'accueil
        try:
            agents = int(values["agent"])
            simulation = int(values["sim"])
        except ValueError:
            return render_template("index_marche_fi.html", tendance=trend)

        if values["trend"] == "Baisse":
            trend = 1
        else:
            trend = 0
        # on récupère les données
        df_strategies, df_best_strategies, list_ask, list_bid, list_pnl = collect_data(agents, simulation, trend)

        # on refait les graphiques pour ensuite les afficher
        fig = Figure()
        market = fig.add_subplot(1, 1, 1)
        market.set_title("Evolution du cours de l'action")
        market.set_xlabel("Iterations")
        market.set_ylabel("Prix en €")
        market.plot(np.linspace(0, 999, num=1000), list_bid, 'r', label='Bid')
        market.plot(np.linspace(0, 999, num=1000), list_ask, 'b', label='Ask')
        market.legend(title="Legend", loc="upper right", bbox_to_anchor=(1.08, 1))
        market.grid()

        fig2 = Figure()
        pnl = fig2.add_subplot(1, 1, 1)
        pnl.set_title("Evolution du cours des PnL")
        pnl.set_xlabel("Iterations")
        pnl.set_ylabel("€")
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[0], 'g', label='Careful Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[1], 'r', label='Clever Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[2], 'm', label='Passive Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[3], 'y', label='Normal Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[4], 'k', label='Short Trader')
        pnl.plot(np.linspace(0, 999, num=1000), list_pnl[5], 'b', label='Price Trader')
        pnl.legend(title="Legend", loc="upper right", bbox_to_anchor=(1.14, 1))
        pnl.grid()

        # On converti les graphiques en image sous format PNG
        pngImage = io.BytesIO()
        pngImage2 = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        FigureCanvas(fig2).print_png(pngImage2)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        pngImageB64String2 = "data:image/png;base64,"
        pngImageB64String2 += base64.b64encode(pngImage2.getvalue()).decode('utf8')

        # on affecte les variables au template
        template = render_template('print_data.html', image=pngImageB64String, image2=pngImageB64String2,
                                   data=df_strategies.to_html(), data_bis=df_best_strategies.to_html())
        return (template)

    if __name__ == "__main__":
        app.run()

application_web()