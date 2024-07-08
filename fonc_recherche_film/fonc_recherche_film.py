import pandas as pd
import streamlit as st

# Appeler les fonctions pour générer les voisins
import fonc_films_plus_proches.fonc_films_plus_proches as affichage

# Gére les lignes unique et relance le choix si != titre unique
def cible_film(df_complet, titre):

    if titre != "" :

        titre = pd.Series([titre]).str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip().values[0]
        while len(titre) != 1:

            if len(df_complet[df_complet["titres_recherches"].str.contains(titre)]) == 1 :
                # Ce que je dois obtenir
                film_cible = df_complet[df_complet["titres_recherches"].str.contains(titre)]

                return affichage.filmslesplusproches(film_cible, df_complet)


            elif len(titre) > 1 :

                ligne_a_choisir = df_complet[df_complet["titres_recherches"].str.contains(titre)]
                        
                return choix_multiple(df_complet, ligne_a_choisir)
            

# Gérer choix multiple et 0 matchs
def choix_multiple(df_complet, ligne_a_choisir):

    if len(ligne_a_choisir) == 0 :

        return st.write("Désolé ! Aucun film ne correspond, mais vous pouvez relancer une recherche!")

    else :
        # Garder le premier titre francophone, retirer les quotes
        ligne_a_choisir["ligne_pour_input"] = ligne_a_choisir["Titres"].str.split(",").str[0].str.rstrip('"').str.rstrip("'").str.lstrip('"').str.lstrip("'")
        # Agglomérer les colonnes pour le visuel + ajotuer un espace entre les genres 
        ligne_a_choisir["ligne_pour_input"] = ligne_a_choisir["ligne_pour_input"].astype(str) + ", " + ligne_a_choisir["Année"].astype(str) + ", " + ligne_a_choisir["Genres"].str.replace(",", ", ").astype(str)

        # Les valeurs nécéssaire pour afficher les titres mais récupérer le tconst pour faire la recherche
        values = ligne_a_choisir['ligne_pour_input'].tolist()
        options = ligne_a_choisir["tconst"].tolist()
        # Le dico me permet de récupérer le tconst pour isoler la ligne choisie
        dic = dict(zip(options, values))

        bouton_choix = st.selectbox("Veuillez choisir un film : ",  options, format_func=lambda x: dic[x])
        # faire apparaitre les info du film 

        load = st.button('Choisir ce film', bouton_choix) 
        if load:
            
            film_cible = df_complet[df_complet["tconst"] == bouton_choix]
            return affichage.filmslesplusproches(film_cible, df_complet)