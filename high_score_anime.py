import re
import pandas as pd
from collections import Counter

print("------------------")
print('Recommandation par rapport aux animes avec le plus grand score par les votant .......')
print("------------------")

animes = pd.read_csv("data/animes.csv", skipinitialspace=True) 
dataset = pd.read_csv("data/features.csv", skipinitialspace=True) 

# convertir la liste des animes_ids en liste d'entiers
animes_ids_list = animes["uid"].tolist() 
animes_ids_list = [int(anime_id) for anime_id in animes_ids_list]

dictionnaire = {} # Dictionnaire pour compter les favoris

count_scores = dataset.groupby(['anime_uid'])['score'].sum()

# Créer un nouveau dictionnaire avec des clés uniques pour chaque anime_id
for anime_id, count in count_scores.items():
    dictionnaire[int(anime_id)] = count

scores_counts = pd.DataFrame.from_dict(dictionnaire, orient="index").rename(columns={0:"score"})
animes_scored = scores_counts.sort_values(by="score", ascending=False)

# convertir les animes_uid de la liste animes_scored en entiers
animes_scored.index = animes_scored.index.astype(int)

# renommer la colonne index en anime_uid 
animes_scored.index.name = "uid"

# ajouter la colonne de titres, genre et aired à animes_scored
animes_scored = pd.merge(animes_scored, animes[["uid", "title", "genre", "episodes", "aired"]], on='uid')

animes_scored.rename(columns={"uid":"anime_uid"}, inplace=True) # renommer la colonne uid en anime_uid
animes_scored.rename(columns={"aired":"release_year"}, inplace=True) # renommer la colonne aired en release_year

# supprimer les doublons dans le dataset
animes_scored = animes_scored.drop_duplicates()

# traiter la colonne aired
def extract_year(aired_str):
    match = re.search(r'\d{4}', aired_str)
    if match:
        return int(match.group())
    else:
        return 2021 # Valeur par défaut

# Appliquer la fonction extract_year au dataset
animes_scored['release_year'] = animes_scored['release_year'].apply(extract_year)

# Remplir les valeurs manquantes dans la colonne "episodes" par 1 
animes_scored['episodes'] = dataset['episodes'].fillna(value=1)

print(animes_scored.head(10))

print("------------------")
# Sauvegarde des données dans un fichier csv
animes_scored.to_csv("data/animes_for_cs.csv", index=False)
print("------------------")
print('animes_scored file created .......')
print("------------------")
print("Taille du fichier :\t", len(animes_scored))
print("------------------")