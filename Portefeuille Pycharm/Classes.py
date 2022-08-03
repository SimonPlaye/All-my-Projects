import pandas as pd
import datetime
import yfinance as yf
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import exp, sqrt
import pickle
from datetime import date
import openpyxl
yf.pdr_override()

"""A FAIRE : Remplacer tous les pdr par yahoo finance pcq pdr incomplet"""

"""Classe servant à calculer le prix d'un call par la méthode de Monte-Carlo"""
class PriceMC:

    def __init__(self, S, K, T, r, sigma):
        self.C = 0  # prix du call
        self.S = S  # prix du sous-jacent
        self.K = K  # strike
        self.T = T  # Temps jusqu'à maturité
        self.r = r  # Taux d'intérêt
        self.sigma = sigma  # volatilité

    "Calcule le prix du call par cette méthode et affiche l'évolution du cours de 10 sous-jacents"
    def price(self, simulations, temps):
        dt = self.T / temps
        S = np.zeros((temps+1,simulations))
        S[0] = self.S
        for i in range(1, temps+1):
            z = np.random.standard_normal(simulations)
            S[i] = S[i-1] * np.exp((self.r - 0.5*self.sigma**2)*dt + self.sigma*sqrt(dt)*z)
        self.C = exp(-self.r*self.T)*np.sum(np.maximum(S[-1]-self.K,0))/simulations
        print(f"Valeur du call : {self.C}")
        plt.plot(S[:, :10])
        plt.grid(True)
        plt.xlabel("Time step")
        plt.ylabel("Asset level")



"""Classe servant à déterminer la surface de volatilé implicite d'un call sur une action donnée"""
"""Ne fonctionne pas car panda reader ne peut pas récupérer les données de titres européens or la formule pour
la volatilité implicite ne fonctionne que pour des options européennes"""
class ImpliedVolatility:

    def __init__(self, security, tolerance, type):
        self.security_name = security #nom de l"action
        self.ticker = yf.Ticker(security)
        self.expiry = self.ticker.options
        self.tolerance = tolerance #tolerance in/out of the money pour enlever les options trop loins du spot
        self.type = type #soit call soit put
        self.list_options = [] #liste des df: chaque df contient les données d'un call/put pour une maturité donnée


    "Méthode chargée de récupérer les données sur le call de l'action"
    def getData(self):

        data = pd.DataFrame()
        if self.type == "C":
            today = datetime.datetime.today()
            spot = yf.download(self.security_name, start = today - datetime.timedelta(days=10), end=today)["Close"][-1] #récupère le dernier cours de l'action
            for date in self.expiry:
                data = self.ticker.option_chain(date=date).calls
                data = data[["strike", "lastPrice","impliedVolatility"]]
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                delta = date - today
                TTM = delta.days / 360
                data["TTM"] = TTM
                data["spot"] = spot
                data.reset_index(inplace=True, drop=True)
                data["r"] = 0.01
                data["IV_est"] = 2
                data["Expiry"] = date

                #on enlève les options qui ne respectent pas le seuil toléré
                data=data[data["strike"]>(1-self.tolerance)*data["spot"]]
                data =data[data["strike"]<(1+self.tolerance)*data["spot"]]
                data.reset_index(inplace=True, drop=True)
                self.list_options.append(data)
        print(self.expiry)
        for i in range(len(self.list_options)):
            print(f"Maturité : {self.expiry[i]}")
            print(self.list_options[i])



    "Calcule le prix du call selon les paramètres donnés"
    def BS_formula(self, S, K, T, r, sigma):
        d1 = (np.log(S/K)+(r+0.5*(sigma)**2)*T) / (sigma*np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        value = S * stats.norm.cdf(d1,0,1) - K * np.exp(-r*T)*stats.norm.cdf(d2,0,1)
        return value

    "Calcul le vega du call pour une vol donné"
    def BSM_vega(self,S, K, T, r, sigma):
        # S: spot price
        # K: strike price
        # T: time to maturity
        # r: interest rate
        # sigma: volatility of underlying asset
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        vega = S * stats.norm.cdf(d1, 0.0, 1.0) * np.sqrt(T)
        return vega

    "Déduit la volatilité implicite"
    def BSM_impl_vol(self, S, K, T, r,sigma_est, C, it=200):
        for i in range(it):
            price = self.BS_formula(S,K,T,r,sigma_est)
            vega = self.BSM_vega(S,K,T,r,sigma_est)
            diff = price - C
            sigma_est -= diff/vega
        return sigma_est

    "Calcule la volatilité implicite"
    def run(self):
        for data in self.list_options:
            sigma_est = self.BSM_impl_vol(data["spot"], data["strike"], data["TTM"], data["r"],data["IV_est"], data["lastPrice"])
            data["IV_est"]=sigma_est
            data["IV_est"].fillna(inplace=True, method="ffill")
            print(data)

    #Tous les calculs sont bons : reste à représenter la surface de volatilité


"""Classe servant à récupérer des données de plusieurs actions pour créer des portefeuilles et 
        comparer les performances de ces portefeuilles"""

class ManagePtf:

    # Récupère les portefeuilles existants s'ils existent
    def __init__(self):
        try:
            self.fichier_ptf = pickle.load(open("ptf.txt", "rb"))
        except EOFError:
            self.fichier_ptf = ""
        self.ptf = pd.DataFrame()
        self.quantite = []
        self.benchmark = pd.DataFrame()
        self.data_chatron = pd.DataFrame()

    #Affiche les ptfs existants
    def displayPtf(self):
        try:
            for ptf, data in self.fichier_ptf.items():
                print(f"Nom du portefeuille : '{ptf}', il est composé des actifs : '{data[0]}', dont la quantité par actif est  : '{data[3]}', début : {data[1]}, fin : {data[2]}")
        except AttributeError:
            print("Aucun portefeuille existant")

    #Supprime un ptf:
    def deletePtf(self, name):
        del self.fichier_ptf[name]
        self.savePtf("",self.fichier_ptf)
        print(f"Le portefeuille '{name}' a été supprimé")

    #Récupère un ptf
    def getPtf(self, name):
        ptf = self.fichier_ptf[name]
        self.getAssetsDataframe(ptf[0], ptf[1], ptf[2], ptf[3])
        print(self.ptf)

    # Sauvegarde un ptf
    def savePtf(self, name, *ptf):
        if ptf: #cas où delete
            pickle.dump(ptf[0], open(
                "ptf.txt", "wb"))
        else:
            if type(self.fichier_ptf) == dict:
                debut = str(self.ptf.index.values[0])[:10]
                fin = str(self.ptf.index.values[-1])[:10]
                equity_to_list = self.ptf.columns.tolist()
                self.fichier_ptf[name] = [" ".join(equity_to_list),debut,fin, self.quantite]
                pickle.dump(self.fichier_ptf, open("ptf.txt", "wb"))
            else:
                debut = str(self.ptf.index.values[0])[:10]
                fin = str(self.ptf.index.values[-1])[:10]
                equity_to_list = self.ptf.columns.tolist()
                self.fichier_ptf={name: [" ".join(equity_to_list), debut, fin, self.quantite]}
                pickle.dump(self.fichier_ptf, open(
                    "ptf.txt",
                    "wb"))


    # Renvoie un data frame des actifs sur la période indiquée, en colonne on ne garde que le close
    def getAssetsDataframe(self, assets, debut, fin, quantite=[]):

        #on vérifie que si l'on met des quantités alors il n'y a pas plus de quantités différentes qu'il n'y a d'accent
        if quantite:
            if len(quantite) != len(assets.split(" ")):
                print("Quantité incohérene")
            else:
                self.ptf = pd.DataFrame()
                self.quantite = quantite
                df = yf.download(assets, start=debut, end=fin)
                close = df[["Close"]]
                close.columns = assets.split(" ")
                self.ptf = pd.concat([self.ptf, close], axis=1)
        #si pas de quantité indiquée
        else:
            self.ptf = pd.DataFrame()
            self.quantite = quantite
            df = yf.download(assets, start=debut, end=fin)
            close = df[["Close"]]
            close.columns = assets.split(" ")
            self.ptf = pd.concat([self.ptf, close], axis=1)
        

    # Affiche les graphiques du ptf
    def basicPlotAssets(self):

        plt.figure(figsize=(12,7))
        plt.subplot(311)
        plt.tight_layout()
        for column in self.ptf:
            plt.plot(self.ptf[column], label=column)
        plt.legend()
        plt.grid(True)
        plt.title("Absolute evolution of the assets")

        plt.subplot(312)
        plt.tight_layout()
        first_row = self.ptf.iloc[0] / 100
        base100 = self.ptf / first_row

        for column in base100:
            plt.plot(base100[column],label=column)
        plt.legend()
        plt.grid(True)
        plt.title("Evolution en base 100")

        plt.subplot(313)
        plt.tight_layout()
        log_return = np.log(self.ptf/self.ptf.shift(1))
        volatility = log_return.rolling(252).var() * np.sqrt(252)
        for column in volatility:
            plt.plot(volatility[column], label=column)
        plt.legend()
        plt.grid(True)
        plt.title("Volatilité annuelle 200 jours glissants")

    "Affiche le portefeuille"
    def plotPortefeuille(self):
        #multiplie le cours des actifs par leur quantité
        data = self.ptf
        for i in range(len(self.quantite)):
            data.iloc[:,i] = self.quantite[i]*data.iloc[:,i]
        ptf = data.sum(1)
        premiere_ligne = ptf.iloc[0]/100
        ptf = ptf/premiere_ligne
        plt.figure(figsize=(9,5))
        plt.plot(ptf, label=" + ".join(data.columns.tolist()))
        plt.title("Evolution du portefeuille en base 100")
        plt.legend()
        plt.grid(True)

    "Clean les datas pour le projet"
    def projetChatronEvolution(self, rafraichir):
        #Récupère le ptf en base 100
        ptf100, ptf = self.getProjetChatronPtf("29-01-2021", rafraichir)

        #Récupère le STOXX 600 et le met en base 100
        benchmark = yf.download("^STOXX", start="2021-01-28")
        benchmark = benchmark[["Close"]]
        benchmark = benchmark.rename(columns={"Close": "STOXX 600"})
        benchmark["STOXX 600"] = (benchmark["STOXX 600"]*100)/benchmark["STOXX 600"][0]

        fig = plt.figure(figsize=(9, 5))
        plt_ptf = fig.add_subplot(1,1,1)
        plt_ptf.plot(ptf100, label="Portefeuille")
        plt_ptf.plot(benchmark, label="EURO STOXX 600")
        plt_ptf.legend()

        plt_ptf.set_title("Evolution du portefeuille en base 100")
        plt_ptf.grid()

        return(fig, ptf)

    def cleanDataChatron(self,date,name):
        data = pd.read_excel("Data/" + date + "/" +name + ".xlsx")
        data.set_index("Ticker", drop=True, inplace=True)
        for col in data.columns:
            if col != "Name":
                data[col] = data[col].replace(" ",0)
        self.data_chatron = data
        return(data)

    def projetChatronPlotHisto(self):
        data = self.data_chatron

        fig = plt.figure(figsize=(14,9), tight_layout=True)
        pe = fig.add_subplot(2,2,1)
        pe.hist(data['BEst P/E BF12M'], bins=50)
        pe.set_xlabel("P/E")
        pe.set_ylabel("Nombre d'entreprises")
        pe.set_xlim([0,150])
        pe.set_title("Répartition du P/E des entreprises")

        peg = fig.add_subplot(2,2,2)
        peg.hist(data['BEst PEG Ratio BF12M'], bins=50)
        peg.set_xlabel("PEG")
        peg.set_ylabel("Nombre d'entreprises")
        peg.set_xlim([-50,50])
        peg.set_title("Répartition du PEG des entreprises")

        ebit = fig.add_subplot(2,2,3)
        ebit.hist(data['EBIT/Net Sales:H'], bins=50)
        ebit.set_xlabel("EBIT/Sales")
        ebit.set_ylabel("Nombre d'entreprises")
        ebit.set_xlim([-150,150])
        ebit.set_title("Répartition de la marge d'EBIT des entreprises")

        sharpe = fig.add_subplot(2,2,4)
        sharpe.hist(data['Sharpe:M-6'], bins=50)
        sharpe.set_xlabel("Ratio de Sharpe")
        sharpe.set_ylabel("Nombre d'entreprises")
        sharpe.set_title("Répartition du ratio de Sharpe des entreprises")

        return(fig)

    #Recupère le ptf en Chatron
    def getProjetChatronPtf(self, date, rafraichir):
        #Retélécharge des données à jour
        if rafraichir:
            #Récupère les données du excel et garde les tickers, le taux de change et les quantités (qu'on a calculé sur le excel directement)
            data = pd.read_excel("Data/ptf "+date+".xlsx")
            data = data[["Ticker", "Name","Quantité", "FX Rate"]]
            data.set_index("Ticker", drop= True, inplace=True)

            ptf = pd.DataFrame()
            #Parcourt les tickers et récupère le cours des derniers jours depuis la création du ptf
            #Si le ptf n'existe pas on le créé, s'il existe on le fusionne avec les nouvelles données
            for ticker in data.index:
                if ptf.empty:
                    data_temp = yf.download(ticker, start="2021-01-28")["Close"] * data.loc[ticker]["FX Rate"] * data.loc[ticker]["Quantité"] #attention, le FX rate est statique: c'est celui en t=0
                    ptf = pd.DataFrame({'Date': data_temp.index, ticker: data_temp.values})

                else:
                    data_temp = yf.download(ticker, start="2021-01-28")["Close"] * data.loc[ticker]["FX Rate"]* data.loc[ticker]["Quantité"]
                    data_temp = pd.DataFrame({'Date': data_temp.index, ticker: data_temp.values})
                    data_temp=data_temp.dropna()
                    ptf = pd.merge(ptf, data_temp, on="Date", how="outer")
            ptf.fillna(inplace=True, method="bfill")
            ptf.set_index("Date", drop=True, inplace=True)
            ptf.rename(columns=data["Name"], inplace=True)

            #Enfin, on somme tous les cours puis on met le ptf en base 100
            ptf100 = ptf.sum(axis=1)
            ptf100 = (ptf100 / ptf100.iloc[0])*100

            data_to_save = pd.merge(ptf100.to_frame("Portefeuille base 100"), ptf, on="Date")
            data_to_save.to_csv("Data/ptf_save.csv")

        #Récupère des données sauvegardées
        else:
            data_to_get = pd.read_csv("Data/ptf_save.csv")
            data_to_get.set_index("Date", drop=True, inplace=True)
            ptf100 = data_to_get.iloc[:,0]
            ptf100.index = pd.to_datetime(ptf100.index) #retransforme en date l'index de la série
            ptf = data_to_get.drop(columns="Portefeuille base 100")

        return(ptf100, ptf)


    "Get best firms according to parameters define by the user"
    def selectDataChatron(self, PE, PEG_inf, PEG_sup, EBIT, Sharpe):
        data = pd.DataFrame()
        data["P/E"] = self.data_chatron['BEst P/E BF12M']<PE
        data["PEG"] = (self.data_chatron['BEst PEG Ratio BF12M']>PEG_inf) & (self.data_chatron['BEst PEG Ratio BF12M']<PEG_sup)
        data['EBIT margin'] = self.data_chatron['EBIT/Net Sales:H'] > EBIT
        data["Sharpe"] = self.data_chatron['Sharpe:M-6'] > Sharpe
        match = data.index[(data["P/E"]==True)&(data["PEG"]==True)&(data["EBIT margin"]==True)&(data["Sharpe"]==True)]
        match = self.data_chatron.loc[match.to_list()]
        match = match[['BEst P/E BF12M','BEst PEG Ratio BF12M', 'EBIT/Net Sales:H', 'Sharpe:M-6']]
        match.columns = ["P/E","PEG", 'EBIT margin', "Sharpe"]
        match.loc["Parameters"] = ["<"+str(PE), "btw:["+str(PEG_inf)+" - "+str(PEG_sup)+"]", ">"+str(EBIT), ">"+str(Sharpe)]

        return(match)


    def printDataSectorChatron(self):
        data = self.data_chatron

        #On récupère notre ptf
        data_to_get = pd.read_csv("Data/ptf_save.csv")
        data_to_get.set_index("Date", drop=True, inplace=True)
        ptf = data_to_get.drop(columns="Portefeuille base 100")
        #on parcourt notre portefeuille et on ne garde que les titres qui appartiennent au secteur en question
        liste_titres = []
        for ticker in ptf.columns:
            try:
                data["Name"][ticker]
            except KeyError: #le titre du portefeuille n'est pas dans le secteur
                pass
            else:
                liste_titres.append(ticker)
        ptf = ptf[liste_titres]
        rendement = ((ptf.iloc[-1] / ptf.iloc[0]) - 1) * 100
        rendement.rename("Rendement en %", inplace=True)
        ptf = pd.concat([pd.DataFrame(rendement).T, ptf])
        return(ptf)








