# la librairie principale pour la gestion des données
import pandas as pd
from datetime import datetime
from dateutil import parser
import re

# l'emplacement des données sur le disque
data_path = "data/"

# chargement des données
animes = pd.read_csv(data_path + "animes.csv", skipinitialspace=True)
profiles = pd.read_csv(data_path + "profiles.csv", skipinitialspace=True)
reviews = pd.read_csv(data_path + "reviews.csv", skipinitialspace=True)

# quelques fonctions utiles pour le prétraitement des données
def convert_to_list(lst):
    lst = lst.strip("[]")
    if lst == "":
        return []
    else:
        return list(map(int, lst.split(", ")))
    



# Imprimer la taille de chaque table de données
print("Taille des données:")
print("------------------")
print("animes:\t", len(animes))
print("profiles:\t\t\t", len(profiles))
print("reviews:\t\t", len(reviews))
print("------------------")


# Initialisation du Dataframe "features" qui va contenir l'ensemble de données d'entrainement
features = animes[['uid', 'genre', 'episodes', 'aired']].copy()
features = features.rename(columns={'uid': 'anime_uid'}) 

reviews_columns = reviews[['profile', 'anime_uid','score','scores']].copy()
features = features.merge(reviews_columns, on='anime_uid', how='left')

profiles_columns = profiles[['profile', 'gender', 'favorites_anime']].copy()
features = features.merge(profiles_columns, on='profile', how='left')

# Remplacement des valeurs manquantes de la colonne gender par Not Specified
features['gender'] = features['gender'].fillna(value='Not Specified')

# Remplir les valeurs manquantes dans la colonne "episodes" par la 1
features['episodes'] = features['episodes'].fillna(value=1)

# supprimer la ligne si la colonne score et la colonne scores sont vides 
features = features.dropna(subset=['score', 'scores'], how='all')

# supprimer les doublons dans le dataset
features = features.drop_duplicates()

# traiter la colonne aired
def extract_year(aired_str):
    match = re.search(r'\d{4}', aired_str)
    if match:
        return int(match.group())
    else:
        return 2021 # Valeur par défaut

# Appliquer la fonction extract_year au dataset
features['aired'] = features['aired'].apply(extract_year)

# transformer la colonne favorites_anime en liste
features["favorites_anime"] = features["favorites_anime"].str.replace("'", "")   
features["favorites_anime"] = features["favorites_anime"].apply(convert_to_list)


print(features.isnull().sum())


# réorganisation des colonnes
features.reindex(columns = ['anime_uid', 'genre', 'episodes', 'aired', 'score', 'scores', 'profile', 'gender', 'favorites_anime'])

# Sauvegarde des données dans un fichier csv
features.to_csv(data_path + "features.csv", index=False)
print("------------------")
print('preprocessing file created .......')
print("------------------")
print("Taille du dataset:\t", len(features))
print("------------------")
# print(features)