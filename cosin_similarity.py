import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import users_test

dataset = pd.read_csv("data/animes_for_cs.csv", skipinitialspace=True) 

# Vectoriser les données textuelles pour la similarité cosinus
count = CountVectorizer()
count_matrix = count.fit_transform(dataset["genre"])

# Calculer la similarité cosinus entre les animes
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Fonction pour recommander des animes similaires en fonction de l'indice de l'anime
def recommend_animes(anime_index, cosine_sim=cosine_sim):

    # Récupérer les scores de similarité des animes
    sim_scores = list(enumerate(cosine_sim[anime_index]))

    # Trier les animes en fonction des scores de similarité
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Sélectionner les 10 animes les plus similaires (en excluant l'anime lui-même)
    sim_scores = sim_scores[1:11]

    # Récupérer les indices des 10 animes les plus similaires
    anime_indices = [i[0] for i in sim_scores]

    # Renvoyer les titres des 10 animes les plus similaires
    return dataset["title"].iloc[anime_indices]

anime_index = 100 

# récuperer le titre de l'anime
anime_title = dataset["title"][anime_index]

# récupérer les genre de l'anime
anime_genre = dataset["genre"][anime_index] 

print("Recommandation par la similarité du cosinus en considérant seulement le genre de : ", anime_title)
print("Les genres sont : ", anime_genre)
print("........................................................................................................ ")
# Exemple d'utilisation : recommander des animes similaires à l'anime d'indice 0
print(recommend_animes(anime_index))



print("---------------------------------------------------------------------------------------------")
print(".............................................................................................")
print("---------------------------------------------------------------------------------------------")