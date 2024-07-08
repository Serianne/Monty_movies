import streamlit as st

def kpi_image():
    # Passage a des screens car l'affichage est trop lourd pour la version basique de Streamlit.
    st.image("kpi_intervenants.jpg", use_column_width="auto", )

    st.image("kpi_genres.jpg", use_column_width="auto", )

    st.image("kpi_duree.jpg", use_column_width="auto", )

    st.image("kpi_decennies.jpg", use_column_width="auto", )