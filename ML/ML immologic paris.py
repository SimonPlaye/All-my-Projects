import pandas as pd

df = pd.read_csv("../Scraping/immologic_data_paris.csv")
df=df.drop(columns="Unnamed: 0") #on enlève la colonne index

#on enlève les lignes avec des valeurs nulles pour ces colonnes
df.dropna(subset=["Area", "Rooms", "Arrondissement"], inplace=True)
df.reset_index(drop=True, inplace=True)

#on enlève les valeurs nulles de la colonne bedroom
def replace_Nan_bedrooms(df):
    #liste des valeurs nulles de Bedroom
    nul=df.Bedrooms.isnull()
    #on récupère la moyenne et la variance de cette colonne
    means=df.groupby(["Bedrooms"]).mean()
    deviation=df.groupby(["Bedrooms"]).std()
    min= means-deviation #valeur min moyenne
    max=means+deviation
    liste_val_supp=[]
    index = min.index #toutes les valeurs différentes dans la colonne Bedrooms

    #on parcourt les valeurs de la colonne Bedroom
    for i in range(len(df.Bedrooms)):
        nouvelle_valeur=None
        if nul[i]==True: #s'il s'agit d'une valeur NaN...
            #...on récupère l'aire et le nb de pieces correspondant à cette valeur
            aire = df.iloc[i,1]
            pieces=df.iloc[i,2]

            #min.Area donne l'aire minimale pour chaque valeur de rooms:
            #par exemple, un appartement avec une seule pièce fait au minimum 29m2, 2 pièces 57m2...
            for j in range(len(min.Area)):
                aire_min=min.iloc[j,0]
                aire_max=max.iloc[j,0]
                piece_min=min.iloc[j,1]
                piece_max=max.iloc[j,1]

                #si un appartement à une aire et un nb de chambre dans un intervalle précis aors on lui affecte le nombre de bedrooms correspondants
                if aire >= aire_min and aire <= aire_max and pieces >= piece_min and pieces <= piece_max:
                    nouvelle_valeur = index[j]
                    break
                #si l'appartement n'appartient à aucun intervalle mais qu'il est tout petit, on considère qu'il n'a qu'une chambre
                elif aire <= min.iloc[0,0]:
                    nouvelle_valeur=index[0]
                    break
            #si on n'a pas pu mettre l'appartement dans un intervalle, on le garde de coté
            if nouvelle_valeur==None:
                liste_val_supp.append(i)
            #sinon on remplace NaN par le nombre de chambre trouvé
            else:
                df.iloc[i,3]=nouvelle_valeur

    #on supprime les appartements dont on n'a pas pu déterminer le nb de chambre
    df.drop(liste_val_supp, axis=0, inplace=True)
    #on supprime les index correspondants à ces appartements
    df.reset_index(drop=True, inplace=True)
    return df


df= replace_Nan_bedrooms(df)
df = df.drop(columns="Arrondissement")

#On convertit la colonne des prix de str à float
def convert(df):
    row_to_drop = []
    for i in range(df["Price"].size):
        split = df.iloc[i, 0].split(" ")
        nombre = ""
        for val in split:
            nombre += val
        try:
            nombre = float(nombre)
        except ValueError:
            row_to_drop.append(i)
        df.iloc[i, 0] = nombre

    df = df.drop(row_to_drop)
    return(df)
df = convert(df)
df.to_csv("DF.csv", index=False)
