import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.graph_objects as go



# Créer le df intervenants pour lancer les graphiques sur les colonnes qu'il contient
def df_intervenants(df_complet):
    # explode + merge sur le df initial
    df_nconst = pd.merge(df_complet['nconst'].str.split(',').explode(), df_complet, left_index=True, right_index=True)
    # on ne garde que la colonne qui résulte de l'explode, soit nconst_X
    df_nconst = df_nconst.drop(columns=['tconst', 'primaryTitle', 'originalTitle', 'startYear',
            'runtimeMinutes', 'genres', 'decade', 'title', 'averageRating',
            'numVotes', 'nconst_y', 'category', 'Acteurs'])
    # on ne garde que la colonne qui résulte de l'explode, soit category_X
    df_category = pd.merge(df_complet['category'].str.split(',').explode(), df_complet, left_index=True, right_index=True)
        # explode + merge sur le df initial
    df_category = df_category.drop(columns=['tconst', 'primaryTitle', 'Titre original', 'Année',
            'runtimeMinutes', 'genres', 'decade', 'title', 'averageRating',
            'numVotes', 'nconst', 'category_y', 'primaryName'])
    # explode + merge sur le df initial
    df_primaryName = pd.merge(df_complet['primaryName'].str.split(',').explode(), df_complet, left_index=True, right_index=True)
    # on ne garde que la colonne qui résulte de l'explode, soit primaryName_X
    df_primaryName = df_primaryName.drop(columns=['tconst', 'primaryTitle', 'originalTitle', 'startYear',
                                                        'Durée', 'Genres', 'decade', 'Titres', 'Note',
                                                        'Nbr votants', 'nconst', 'category', 'primaryName_y'])
    # concaténation des 3 df créés avec le df initial
    df_intervenants = pd.concat([df_complet, df_nconst, df_category, df_primaryName], axis = 1)
    # suppression des [] et '' pour les 3 colonnes qui résultent de l'explode
    df_intervenants['nconst_x'] = df_intervenants['nconst_x'].str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace("'", '', regex=False)
    df_intervenants['category_x'] = df_intervenants['category_x'].str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace("'", '', regex=False)
    df_intervenants['primaryName_x'] = df_intervenants['primaryName_x'].str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace("'", '', regex=False)

    # renommer les colonnes
    df_intervenants.rename(
                columns={"nconst": "liste_nconst",
                        "category": "liste_category",
                        "primaryName": "liste_primaryName",
                        "nconst_x" :"nconst",
                        "category_x" : "category",
                        "primaryName_x" : "primaryName"},
                        inplace=True,)
    # suppression des espaces indésirables (qui se trouveraient au début ou à la fin)
    df_intervenants['category'] = df_intervenants['category'].str.strip()
    df_intervenants['nconst'] = df_intervenants['nconst'].str.strip()
    df_intervenants['primaryName'] = df_intervenants['primaryName'].str.strip()

    return df_intervenants


# Top10 des acteurs
def top_10_acteurs(df_intervenant):
    # création du df_actors
    df_actors = df_intervenant[df_intervenant['category'] == 'actor'].copy()
    # TOP 10 des acteurs
    top10_actors = df_actors.groupby('primaryName').size().nlargest(10)
    top10_actors = top10_actors.to_frame().reset_index()
    top10_actors.index = top10_actors.index + 1
    top10_actors.rename(
        columns={'primaryName' : "Nom de l'acteur",
                    0: "Nombre de films"},
                        inplace=True)
        
    s = top10_actors[["Nom de l'acteur", "Nombre de films"]].style.background_gradient(cmap='viridis')
    #st.write("Top10 des acteurs")
    st.write(s)

# Top 10 des actrices
def top_10_actrices(df_intervenant):
    df_actress = df_intervenant[df_intervenant['category'] == 'actress']
    top10_actress = df_actress.groupby('primaryName').size().nlargest(10)
    top10_actress_df = top10_actress.to_frame().reset_index()
    top10_actress_df.index = top10_actress_df.index + 1
    top10_actress_df.rename(
            columns={'primaryName' : "Nom de l'actrice",
                    0: "Nombre de films"},
                        inplace=True,)

    cm = sns.light_palette("green", as_cmap=True)
    s = top10_actress_df[["Nom de l'actrice", "Nombre de films"]].style.background_gradient(cmap='viridis')
    #st.write("Top10 des actrices")
    st.write(s)



def acteur_actrice_pyramide():
    df_genres = pd.DataFrame({"decennie":["2000", "2010", "2020"], "h":[30, 40, 70], "f": [70, 60, 30]})
    y_age = df_genres['decennie']
    x_M = df_genres['h']
    x_F = df_genres['f'] * -1
    # Creating instance of the figure
    fig = go.Figure()
            
    # Adding Male data to the figure
    fig.add_trace(go.Bar(y= y_age, x = x_M, 
                                name = 'Acteurs', 
                                orientation = 'h'))
            
    # Adding Female data to the figure
    fig.add_trace(go.Bar(y = y_age, x = x_F,
                                name = 'Actrices', orientation = 'h'))
            
    # Updating the layout for our graph
    fig.update_layout(barmode = 'relative',
                            xaxis = dict(tickvals = [-70, -50, -40,
                                                    0, 40, 50, 70],
                                            
                                        ticktext = ['70%', '50%', '40%', '0', 
                                                    '40', '50', '70']),

                                        #title="Répartition des acteurs et actrices :",

                                        #xaxis_title="Pourcentage d'acteurs et d'actrices",
                                        yaxis_title="Année",

                                        #legend_title="Legend Title",
                                        font=dict(
                                            family="Courier New, monospace",
                                            size=18,
                                            color="RebeccaPurple"))
            
    #fig.show()
    st.plotly_chart(fig, use_container_width=True)