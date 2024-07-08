import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import numpy as np
import fonc_recherche_film.fonc_recherche_film as rech_film
import fonc_kpi.kpi as kpi
import warnings

warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)
st.set_page_config(layout="wide")

# importer et mettre en cache le df
@st.cache_data
def load_data():
    return pd.read_csv("df_final_Monty_streamlit.csv") 

df = load_data()

import fonc_kpi.titres as titres
import fonc_kpi.genres as genres
df_title = titres.df_titres(df)
df_genres_exp, group_by_genre  = genres.genre_explode_df(df)

st.sidebar.title("Navigation")
options = st.sidebar.radio(" ", options=['Présentation', 'Recherche de films', 'KPI', ])

# Navigation avec boutons radios
if options == 'Présentation':

    st.header("L'équipe des Monty est fière de vous présenter son projet d'étude avec la Wild Code School.")
    st.write(" ")
    st.image("Monty_team.jpg", use_column_width="auto", caption="Monty Python and the Holy Grail (1975)")
    st.write(" ")


    st.subheader("_Démarche_")
    # Pour qui fait on la sélection? (contexte pop de la Creuse, chiffres du cinéma fr...)
    st.write("À l'aide des fichiers _[IMDB](https://datasets.imdbws.com/)_ au format CSV, nous avons créé un ficher de 53 954 films différents pour créer un service fictif de streaming pour un cinéma.")
    st.write("Nous avons choisi de préparer une sélection portée par le cinéma français (mais pas exclusivement) et à la notation supérieur ou égal à 5/10.")
    st.write("La population de la Creuse comportant une part importante de seniors, nous avons donc axé notre service vers des films familiaux, et dont les plus anciens remontent aux années 1910.")
    
    st.subheader("_Spécificités de notre sélection_")
    # Film en vf ou en langue française (éviter les films non traduis pour coller à une population pas forcément familière de l'anglais)
    st.write("La sélection étant majoritairement en langue française, nous avons choisi de valoriser les films tournés en français en détectant la langue originelle du film grâce à son titre, celle-ci n'est pas renseignée de manière optimale sur IMBD.")
    st.write("Un indicateur de qualité basé sur la notation et le nombre de votants vient renforcer la pertinence et la qualité des recommandations.")
    st.write("L'influence du cinéma français est visible, notamment sur la popularité des acteurs français, qui sont nettement représentés dans la sélection.")

    st.subheader("_Quelques chiffres et informations :_")
    st.write("53 954 films différents référencés.")
    st.write("22 genres représentés")
    st.write("Une note médiane de 6.4.")
    st.write("Parmi la sélection, les aventures des mousquetaires sont les plus représentés avec 30 adaptations.")

elif options == 'Recherche de films':
    st.header("Rechercher un film :")
    st.write("_Vous pouvez chercher par mots clés, titre complets, incomplets..._")
    titre_input = st.text_input("Recherche de films :", key='input',) #label_visibility="hidden" )
    film_cible = rech_film.cible_film(df, titre_input)

elif options == 'KPI':
    kpi.kpi_image()


    

 
                