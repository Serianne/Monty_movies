import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def duree_barplot(df_complet):
    df_complet["runtimeMinutes_categorie"] = pd.cut(df_complet["runtimeMinutes"], [60, 80, 100, 150, 300], labels=["60-80", "80-100", "100-150", "150-300"])
    #duree_graph = df_complet.groupby(by = "runtimeMinutes_categorie")["numVotes"].mean().round(2)
    fig, ax = plt.subplots()
    ax = sns.countplot(data=df_complet, x="runtimeMinutes_categorie", color="royalblue") # countplot
    plt.title("nb de film par durée")
    plt.ylabel("nb film")
    plt.xlabel("durée")
    st.pyplot(fig)

def duree_lolipop(df_complet):
    larry_serie = df_complet.groupby(by = "runtimeMinutes_categorie")["numVotes"].mean().round(2)
    larry_serie.sort_values(ascending=False)
    my_range=range(len(larry_serie.index))

    fig, ax = plt.subplots(figsize=(12,5))
    (markers, stemlines, baseline) = plt.stem(larry_serie)
    plt.xticks(my_range, larry_serie.index, )
    plt.setp(markers, marker='*', markersize=10, markeredgecolor="royalblue", markeredgewidth=2)
    #plt.title("Moyenne des votes par durée de film")
    plt.ylabel("Votes")
    plt.xlabel("Durée des films")
    st.pyplot(fig)

def duree_histplot(df_complet):
    fig, ax = plt.subplots()
    ax = sns.histplot(data=df_complet, x="averageRating", bins=5) 
    #plt.title("nb de film par note")
    plt.ylabel("Nombre de films")
    plt.xlabel("Notes")
    st.pyplot(fig)

def histoplot_film_decade(df_complet):
    fig, ax = plt.subplots() 
    ax =sns.histplot(data=df_complet, x="decade") 
    #plt.title("nb de film par décennie")
    plt.ylabel("Nombre de films")
    plt.xlabel("Décennies")
    st.pyplot(fig)

def barplot_stack_categorie_duree(df_complet):
    df_decade_runtime = df_complet.groupby(by = ["decade", "runtimeMinutes_categorie"])["title"].count().reset_index()
    df_decade_runtime = df_decade_runtime.rename(columns={"title":"count"})
    df_decade_runtime.groupby(['decade','runtimeMinutes_categorie']).sum().unstack().plot(kind='bar', stacked=True)
    plt.xlabel("décennie")
    plt.ylabel("Nombre de films")
    #plt.title("Nombre de films par catégorie de durée de film pour chaque décennie")
    st.pyplot(df_decade_runtime.groupby(['decade','runtimeMinutes_categorie']).sum().unstack().plot(kind='bar', stacked=True).figure)    