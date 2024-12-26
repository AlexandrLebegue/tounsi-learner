import streamlit_antd_components as sac
import streamlit as st
from streamlit_javascript import st_javascript
def show_menu():
    with st.sidebar:
        selected = sac.menu([
            sac.MenuItem('Navigation', children = [
                sac.MenuItem('Accueil', icon='house-fill'),
                sac.MenuItem('Leçons', icon='clipboard-fill'),
                sac.MenuItem('Dictionnaire', icon='book-fill'),
            ])
        ], open_all=True)
        

        if selected == "Accueil" and selected != st.session_state["current_page"]:
            st.switch_page("streamlit_app.py")
        elif selected == "Leçons" and selected != st.session_state["current_page"]:
            st.switch_page("pages/page_lecons.py")
        elif selected == "Dictionnaire" and selected != st.session_state["current_page"]:
            st.switch_page("pages/page_dico.py")

