import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors



def prep_model(df_complet):
    # Restreindre le df aux colonnes pour le ML (différents de celles des KPI)
    df_pour_ML = df_complet[['tconst', 'primaryTitle', 'Titre original', 'Année', 'Durée', 'Genres',
                            'Titres', 'Note', 'Nbr votants', 'Acteurs', 'native_lang_fr',
                            'titres_recherches', 'Action', 'Adventure', 'Animation', 'Biography',
                            'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
                            'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
                            'Romance', 'Sci-Fi', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western',
                            'Top film']]
    # Création du  sur le df uniquement sur vos valeurs quantitatives
    X = df_pour_ML.select_dtypes("number")
    # Création du modèle scalaire
    scaler_df = StandardScaler()
    # Entrainement du modèle sur X
    scaler_df.fit(X)
    # Transformer notre X en données scalaires
    X_scaled_test = scaler_df.transform(X)
    # Passer ces données en dataframme pour pouvoir travailler dessus
    X_scaled_test = pd.DataFrame(X_scaled_test, index=X.index, columns=X.columns)
    # Création du modèle et entrainement
    model = NearestNeighbors(n_neighbors=11)
    model.fit(X_scaled_test)
    return scaler_df , model



def afficher_film(film_choisi, filmsproches, df_complet):
    # Générer des colonnes ou ranger les info des films
    st.write("_Fiml choisi_ :")

    col_espace1, col_info_film, col_espace2, col_lien_fiche_film, col_espace3 = st.columns([0.3, 8, 0.5, 3, 0.5])

    with col_info_film : 
        film_choisi_titre = film_choisi["Titres"]
        premier_titre_film_choisi = film_choisi_titre.split(",")[0].rstrip('"').rstrip("'").lstrip('"').lstrip("'")
        st.write(premier_titre_film_choisi)

    with col_lien_fiche_film:
        tconst_film_choisi = film_choisi['tconst']
        url_film_choisi = "https://www.imdb.com/title/{}/?ref_=nv_sr_srsg_0_tt_5_nm_3_q_taram%2520et".format(tconst_film_choisi)
        st.write("[Voir la fiche IMDB](%s)" % url_film_choisi)

    st.divider()
    # Générer des colonnes ou ranger les info des films
    st.write("_Films proposés_ :")
    col_espace2_1, col_info_film_2, col_espace2_2, col_lien_fiche_film_2, col_espace_2_3 = st.columns([0.3, 8, 0.5, 3, 0.5])

    with col_info_film_2 : 
        for film in filmsproches.index:
            # Afficher les info des films
            # N'afficher que le premier titre pour gagner en lisbilité
            nom_film = df_complet["Titres"].iloc[film]
            premier_titre_film = nom_film.split(",")[0]  
            # Enlever les " et ' 
            premier_titre_film = premier_titre_film[:-1]
            premier_titre_film = premier_titre_film[1:]
            note_film = df_complet['Note'].iloc[film]
            st.write(premier_titre_film, note_film)
            st.divider()

    with col_lien_fiche_film_2 : 
        for film in filmsproches.index:
            # Faire apparaitre le lien de la fiche IMDB
            tconst_film = df_complet['tconst'].iloc[film]
            url = "https://www.imdb.com/title/{}/?ref_=nv_sr_srsg_0_tt_5_nm_3_q_taram%2520et".format(tconst_film)
            st.write("[Voir la fiche IMDB](%s)" % url)
            st.divider()
                
## Passage à 3 films pour plus de lisibilité

# Fonction qui retourne les 3 films similaires
def filmslesplusproches(film_cible, df_complet,):  #scaler_df, model
    # Adapter le modèle pour une appli j'appelle directement ma fonction de prépa de modèle dans celle ci.
    scaler_df, model = prep_model(df_complet)

    # scaler la ligne du film
    scaler_ligne_choisie = scaler_df.transform(film_cible[scaler_df.feature_names_in_])
    film_cible_scaled = pd.DataFrame(scaler_ligne_choisie, index=film_cible.index, columns=scaler_df.feature_names_in_)
    ### les voisins
    df_complet = df_complet.filter(items=['tconst', 'Titre original', 'Année', 'Durée', 'Genres',
                                        'Titres', 'Note', 'Nbr votants', 'Acteurs', 'native_lang_fr', 'Top film'])
    
    neigh_dist, neigh_films =  model.kneighbors(scaler_ligne_choisie)
    film_choisi = df_complet.iloc[neigh_films[0][0]]
    filmsproches = df_complet.iloc[neigh_films[0][1:4]]
    afficher_film(film_choisi, filmsproches, df_complet)          
