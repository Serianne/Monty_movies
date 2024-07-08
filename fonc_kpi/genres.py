import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly_express as px


# Générer le df des genres
def genre_explode_df(df_complet):
    # Explode sur les genres pour les utilisers dans les graphs
    # Scinder tous les multi-genres sur une seule colonne
    df_genres_exp = pd.merge(df_complet["genres"] .str.split(",").explode(), df_complet, left_index=True, right_index=True)
    df_genres_exp = pd.merge(df_complet["genres"] .str.split(",").explode(), df_complet, left_index=True, right_index=True)
    df_genres_exp.rename(columns={'genres_x':'genre_unique','genres_y':'genre_mulitple' }, inplace=True)
    
    # créer une condition pour les genres trop peu représenté pour des résultats plus pertinents
    nb_genres = df_genres_exp.groupby('genre_unique').size().sort_values(ascending=False)
    nb_genres = nb_genres[nb_genres>=100]

    # création d'un DF avec cette condition
    nb_genres = nb_genres.to_frame()

    # fusion du DF avec condition et le DF principal pour insérer la colonne de condition
    df_genres_exp = pd.merge(df_genres_exp,nb_genres,how='left',on='genre_unique')
    # renommer la colonne
    df_genres_exp.rename(columns={0:'sup à 100 genres'},inplace=True)

    # suppression des lignes et vérif le nombre de lignes
    df_genres_exp = df_genres_exp[df_genres_exp['sup à 100 genres'].notna()]

    # numéroter les genres avec factorize
    df_genres_exp['No_genre'] = df_genres_exp['genre_unique'].factorize()[0]

    group_by_genre = df_genres_exp.groupby('genre_unique').mean()
    group_by_genre = pd.DataFrame(dict(group_by_genre))
    group_by_genre = group_by_genre.reset_index()

    return df_genres_exp, group_by_genre 

# Le top 10 des genres
def top_10_genres(df_genres_exp):

    # TOP 10 genres
    top10genres = df_genres_exp['genre_unique'].value_counts().nlargest(10)
    # Créer un DF pour mise en forme
    top10genres_df = top10genres.to_frame().reset_index()
    # Ajouter un index
    top10genres_df.index = top10genres_df.index+1
    top10genres_df.rename(
        columns={'index' : "Genre",
                    'genre_unique': "Cumul"},
                        inplace=True)
    
    s = top10genres_df.style.background_gradient(cmap='viridis')
    #st.write("Top10 des genres")
    st.write(s)

# visualiser la moyenne des notes par genre de films, taille du point selon la moyenne du nombre de votes
def scatterplot_fleche(group_by_genre):
    fig, ax = plt.subplots(figsize = (30,15))

    plt.scatter(x = group_by_genre['averageRating'], y = group_by_genre['numVotes'], sizes=(100,500))

    ax.set_xlabel("Note moyenne des genres")
    ax.set_ylabel("Nombre de votes moyen des genres")

    ax.scatter(x = 6.51, y = 14982.26, marker = "v", c = "white") #drama
    ax.scatter(x = 6.14, y = 77277.29, marker = "v", c = "white") #Sci-fi
    ax.scatter(x = 7.14, y = 1899.61, marker = "v", c = "white") #docu
    ax.scatter(x = 6.16, y = 27879.72, marker = "v", c = "white") #Thriller
    ax.scatter(x = 6.31, y = 48019.55, marker = "v", c = "white") #Adventure

    ax.annotate('Drama', xy =(6.51, 14982.26),
                xytext =(6.50, 20000),
                arrowprops = dict(facecolor ='black',
                                shrink = 0.05),size=30   )

    ax.annotate('Sci-fi', xy =(6.14, 77277.29),
                xytext =(6.10, 70000),
                arrowprops = dict(facecolor ='black',
                                shrink = 0.05),size=30   )

    ax.annotate('Documentary', xy =(7.14, 1899.61),
                xytext =(7.0, 6000),
                arrowprops = dict(facecolor ='black',
                                shrink = 0.05),size=30   )

    ax.annotate('Thriller', xy =(6.16, 27879.72),
                xytext =(6.2, 29000),
                arrowprops = dict(facecolor ='black',
                                shrink = 0.05),size=30   )

    ax.annotate('Adventure', xy =(6.31, 48019.55),
                xytext =(6.35, 50000),
                arrowprops = dict(facecolor ='black',
                                shrink = 0.05),size=30   )
    #plt.suptitle("Notes moyennes et Nombre de votes moyens par genre de films", size=22)

    fig.update_layout(
                        xaxis_title="",
                        yaxis_title=""
                        )

    st.pyplot(fig)


def barplot_genre_plus_present(df_genres_exp):
    fig, ax = plt.subplots(figsize=(12,8))
    genres = df_genres_exp["genre_unique"].value_counts().sort_index()
    plt.barh(genres.index, genres.values, color='royalblue')
    plt.ylabel("Genres de films")
    plt.xlabel("Nombre de films")
    #plt.title('Genre le plus présent dans les films')
    st.pyplot(fig)

def barplot_genre_plus_votes(df_genres_exp):
    fig = px.histogram(df_genres_exp, y='genre_unique', x='averageRating',color='genre_unique', height=400, title='Genres avec le plus de votes')
    st.plotly_chart(fig, use_container_width=True)