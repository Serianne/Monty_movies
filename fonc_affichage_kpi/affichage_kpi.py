import streamlit as st

import fonc_kpi.intervenants as interv
import fonc_kpi.decennie as decen
import fonc_kpi.duree as duree
import fonc_kpi.genres as genres
import fonc_kpi.titres as titres

# Partie KPI

def kpi_sidebar(df_complet, df_title, df_genres_exp, group_by_genre):
    st.write("KPI réalisés :")

    with st.expander("Intervenants", expanded=True):
        df_intervenant = interv.df_intervenants(df_complet)

        espace_1, topacteur, espace_2, topactrice, espace_3, pyramide, espace_4= st.columns([0.3, 2.5, 0.1, 2.5, 0.1, 3, 0.3])
        with topacteur :
            st.subheader("Top 10 des acteurs")
            interv.top_10_acteurs(df_intervenant)
        with topactrice :
            st.subheader("Top 10 des actrices")
            interv.top_10_actrices(df_intervenant)
        with pyramide:
            st.subheader("Répartition acteurs/actrices")
            interv.acteur_actrice_pyramide()

    with st.expander("Décennies", expanded=True):
        espace_1, decenies_pop, espace_2, pyramide_decenies, espace_3 = st.columns([0.1, 3, 0.1, 3, 0.1])

        with decenies_pop:
            st.subheader("Variation par décénnies du nombre de films et de votes")
            decen.decenies_populaires(df_complet)
            
        with pyramide_decenies:
            st.subheader("Analyse de la parité")
            decen.pyramide_h_f_decenie()

    with st.expander("Durée", expanded=True):


        espace_1, lolipop, espace_1_2, histo_film_decade, espace_1_3, duree_histo, espace_1_4 = st.columns([0.1, 3, 0.1, 3, 0.1, 3, 0.5])

        with lolipop :
            
            st.subheader("Moyenne votes/durée de films")
            st.subheader(" ")
            st.subheader(" ")
            duree.duree_lolipop(df_complet)

        with histo_film_decade :
            st.subheader("Nombre de films par décénies")
            duree.histoplot_film_decade(df_complet)

        with duree_histo:
            st.subheader("Nombre de films par notes")
            duree.duree_histplot(df_complet)

    with st.expander("Genres", expanded=True):
        #df_genres_exp, group_by_genre  = genres.genre_explode_df(df_complet)

        espace_1_1, top_10_genre, espace_1_2, barplot_plotly, espace_1_3, = st.columns([0.3, 3, 0.3, 5, 0.3, ])

        with top_10_genre : 
            st.subheader("Les 10 genres les plus présents")
            genres.top_10_genres(df_genres_exp)

        #with scatter_fleche :
            #st.subheader("")
            #genres.scatterplot_fleche(group_by_genre)

        with barplot_plotly:
            st.subheader("Genres les plus notés")
            genres.barplot_genre_plus_votes(df_genres_exp)
        
        #espace_2_1, barplot_1, espace_2_2,  = st.columns([0.5, 3, 0.5])

        espace_1_1, barplot_1, espace_1_2, vide_large, espace_1_3, = st.columns([0.3, 3, 0.3, 5, 0.3, ])

        with barplot_1 :
            st.subheader("Genres les plus présent dans les films")
            genres.barplot_genre_plus_present(df_genres_exp)



    #with st.expander("Titres", expanded=True):
        ##df_title = titres.df_titres(df_complet)
        
        #espace_2_1, barplot_titres, espace_2_2, titres_reviennent, espace_2_3, pie_chart_titres, espace_2_4 = st.columns([0.1, 3, 0.1, 3, 0.1, 3, 0.1])

        #with barplot_titres :
                #titres.barplot_titre(df_title)
        #with titres_reviennent :
                #titres.titres_reviennent_plus(df_title)
        #with pie_chart_titres :
                #titres.pie_chart_titre(df_complet)