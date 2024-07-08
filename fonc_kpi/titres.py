import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def df_titres(df_complet):
    df_title = df_complet.filter(['tconst', 'primaryTitle', 'originalTitle', 'title'])
    df_title = pd.merge(df_title['title'].str.split(',').explode(), df_title, left_index=True, right_index=True)
    df_title.drop(['title_y'], axis=1, inplace=True)
    df_title['title_x'] = df_title['title_x'].str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.strip().str.replace('"', '', regex=False).str.lstrip("'").str.rstrip("'").str.strip()
    df_title['title_x'].str.lstrip(" ").str.rstrip(" ")
    return df_title

def barplot_titre(df_title):
    plot_nb_top_titre = df_title['title_x'].value_counts().nlargest(20).reset_index()
    fig, ax1 = plt.subplots(figsize=(12,7))
    sns.color_palette("rocket", as_cmap=True)
    sns.barplot(data=plot_nb_top_titre, y='index', x='title_x',  palette="crest")
    plt.title('Le top 20 des titres de films')
    plt.xlabel('Nombre de fois ou le titre revient')
    plt.ylabel('Titre qui revient')
    st.pyplot(fig)

def titres_reviennent_plus(df_title):
    nbr_titre = df_title['tconst'].value_counts().sort_values(ascending=True)
    nbr_titre = nbr_titre.value_counts().reset_index()
    nbr_titre.rename(columns={'index': "nbr_titres", "tconst": "Nombre_films"}, inplace=True)
    fig, ax1 = plt.subplots(figsize=(12,7))
    sns.barplot(data=nbr_titre, x='Nombre_films', y='nbr_titres', errorbar=None, color='royalblue')
    plt.title('Répartition du nombre de films en fonction du nombre de titre')
    plt.xlabel('Nombre de films')
    plt.ylabel('Nombre de titres')
    st.pyplot(fig)  

def pie_chart_titre(df_complet):
    # Viz pour la proportion : 
    # Pie chart car 2 catégories
    orginal_egal_primary = (df_complet['originalTitle'] == df_complet['primaryTitle']).value_counts()
    labels = ["Même titre", "Titres différents"]

    fig, ax = plt.subplots(figsize=(10,3))
    ax.pie(orginal_egal_primary, labels=labels, explode=[0.05, 0.05], autopct='%1.1f%%', shadow=True)
    ax.set_title('Comparaison des titres primaires et originals')
    st.pyplot(fig) 