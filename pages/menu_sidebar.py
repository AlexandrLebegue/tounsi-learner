import streamlit_antd_components as sac
import streamlit as st
def show_menu():
    with st.sidebar:
        selected = sac.menu([
            sac.MenuItem('Navigation', children = [
                sac.MenuItem('Accueil', icon='house-fill'),
                sac.MenuItem('Leçons', icon='clipboard-fill'),
                sac.MenuItem('Dictionnaire', icon='book-fill'),
            ])
        ], open_all=True)

        if selected == "Accueil":
            st.switch_page("streamlit_app.py")
        elif selected == "Leçons":
            st.switch_page("pages/page_lecons.py")
        elif selected == "Dictionnaire":
            st.switch_page("pages/page_dico.py")

