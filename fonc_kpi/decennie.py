import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib
import plotly.graph_objects as go
import streamlit as st

# Préparer le df pour les décénies
def decenies_populaires(df_complet):
    # Préparer les axes du barplot
    film_dec = df_complet["tconst"].groupby(by=df_complet["decade"]).count()
    data_frame_film_dec = pd.DataFrame(film_dec).reset_index()

    # le numbre de votes moyen par décennies

    # renommer les colonnes pour notre lineplot
    data_frame_film_dec.rename(columns={'index': "decade", "tconst": "Nombre_films"}, inplace=True)
    nbr_moy_vote_dec = round(df_complet["numVotes"].groupby(by=df_complet["decade"]).mean())
    merge_graphique = pd.merge(data_frame_film_dec, nbr_moy_vote_dec, how = "left", left_on="decade", right_index=True)

    matplotlib.rc_file_defaults()
    ax1 = sns.set_style(style=None, rc=None )

    fig, ax1 = plt.subplots(figsize=(12,7))

    graph_1 = sns.lineplot(data = merge_graphique['Nombre_films'], color = "purple", marker='o', sort = False, ax=ax1, label = "Nombre de films")
    plt.ylabel("Nombre de films")
    plt.xlabel("Décennies")

    #graph_1.set_title("Evolution par décennies du nombre de films et du nombre de votes")

    ax2 = ax1.twinx()

    graph_2 = sns.barplot(data = merge_graphique, x='decade', y='numVotes', color = "royalblue", alpha=0.5, ax=ax2)
    plt.ylabel("Nombre de votes")


    plt.show()
    st.pyplot(fig)

def pyramide_h_f_decenie():
    df_genres = pd.DataFrame({"decennie":["1910", "1920", "1930", "1940", "1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"], 
                                "actor":[63.76, 62.73, 62.35, 62.83, 63.28, 63.82, 65.62, 64.32, 62.78, 61.61, 60.51, 58.13], 
                                "actress": [36.24, 37.27, 37.65, 37.17, 36.72, 36.18, 34.38, 35.68, 37.22, 38.39, 39.49, 41.87]})
    y_age = df_genres['decennie']
    x_M = df_genres['actor']
    x_F = df_genres['actress'] * -1
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
                                        yaxis_title="Décennies",

                                        #legend_title="Legend Title",
                                        font=dict(
                                            family="Courier New, monospace",
                                            size=18,
                                            color="RebeccaPurple"))

    st.plotly_chart(fig, use_container_width=True)