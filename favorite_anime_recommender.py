import pandas as pd
from collections import Counter

print("--------------------------------------------------------")
print('....Recommandation par rapport aux animes favorites....')
print("--------------------------------------------------------")
dataset = pd.read_csv("data/features.csv", skipinitialspace=True) 
animes = pd.read_csv("data/animes.csv", skipinitialspace=True) 

favorites_count = {} # Dictionnaire pour compter les favoris
favorites_anime_list = dataset["favorites_anime"].tolist()
animes_ids_list = animes["uid"].tolist() 
favorites_anime_list = [s.replace("'", "").strip('[]') for s in favorites_anime_list] # Supprimer les apostrophes et les crochets

# convertir la liste des animes_ids en liste de d'entiers
animes_ids_list = [int(anime_id) for anime_id in animes_ids_list]

# Supprimer les espaces en début et fin de chaîne de caractères
favorites_anime_list = [s.strip() for s in favorites_anime_list]

# supprimer les index vide
favorites_anime_list = [s for s in favorites_anime_list if s != '']

# Convertir la liste de chaînes de caractères en liste de listes
favorites_anime_list = [s.split(', ') for s in favorites_anime_list]

# Combiner toutes les listes en une seule
combined_list = [anime_id for sublist in favorites_anime_list for anime_id in sublist]

# convertir les éléments de la liste en entiers
combined_list = [int(anime_id) for anime_id in combined_list]

# retirer les animes_uid qui ne sont pas dans la liste des animes
combined_list = [anime_id for anime_id in combined_list if anime_id in animes_ids_list]

# Compter le nombre d'occurrences de chaque anime_id
counts = Counter(combined_list)

# Créer un nouveau dictionnaire avec des clés uniques pour chaque anime_id
for anime_id, count in counts.items():
    favorites_count[int(anime_id)] = count

fav_counts = pd.DataFrame.from_dict(favorites_count, orient="index").rename(columns={0:"count"})
df_fav = fav_counts.sort_values(by="count", ascending=False).head(10)

# renommer la colonne index en anime_uid 
df_fav.index.name = "anime_uid"

# afficher les titres des animes correspondants aux anime_uid dans le dataframe df_fav
df_fav["title"] = animes.loc[df_fav.index]["title"]

print(df_fav)
print("------------------")