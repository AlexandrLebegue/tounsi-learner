import streamlit_antd_components as sac
import streamlit as st
from streamlit_javascript import st_javascript
from streamlit_navigation_bar import st_navbar

def show_nav_bar():
    pages = ["🏚️ Accueil", "👩‍🏫 Leçons", "📖 Dictionnaire", "📝 Quizz", "🏅Classement"]
    styles = {
        
        #"nav": {
        #    "background-color": "rgb(200, 16, 46)",
        #    },
        #
        "div": {
            "max-width": "25rem",
            "box-shadow": "0px 10px 0px rgb(255, 75, 75)"
        },
        "nav": {
            "box-shadow": "10px 0px 0px rgb(255, 75, 75)"
        },
        "img": {
            "padding-right": "14px",


        },
        "span": {
            "color": "rgb(255, 255, 255)",  # Blanc
            "border-radius": "0.5rem",
            "font-weight": "normal",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
            "font-family": "'Roboto Thin', sans-serif",
            "transition": "0.3s",
            "font-weight": "lighter",
            "font-size": "90%",
            "justify-content": "left",
            
        },
        #    "margin": "0 0.125rem",
        #    "padding": "0.4375rem 0.625rem",
              # Ajout de la police
        #},
        "active": {
            "color": "rgb(255, 75, 75)",
            "background-color": "rgba(255, 75, 75, 0.25)"

        },

        "hover": {
            "transition": "0.3s",
            "font-size": "120%",
            "background-color": "rgba(255, 75, 75, 0.25)"
        },
       
    }

    options = {
    "fix_shadow": True,
    "show_menu": False,
    }
    
    selected = st_navbar(pages, styles=styles, options = options, selected = None, )
    if selected == "🏚️ Accueil" and "Accueil" != st.session_state["current_page"]:
        st.switch_page("streamlit_app.py")
    elif selected == "👩‍🏫 Leçons" and "Leçons" != st.session_state["current_page"]:
        st.switch_page("pages/page_lecons.py")
    elif selected == "📖 Dictionnaire" and "Dictionnaire" != st.session_state["current_page"]:
        st.switch_page("pages/page_dico.py")
    elif selected == "📝 Quizz" and "Quizz" != st.session_state["current_page"]:
        st.switch_page("pages/page_quizz.py")
    elif selected == "🏅Classement" and "Classement" != st.session_state["current_page"]:
        st.switch_page("pages/page_classement.py")

def show_menu():
    #show_nav_bar()
    with st.sidebar:
        with open( ".streamlit/style.css" ) as css:
            st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

        st.markdown("""<style>
  div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
      height: 10rem;
      width: auto;
  }
  
  div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
  div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
      display: flex;
      align-items: center;
  }
</style>""", unsafe_allow_html= True)
        st.logo("output-onlinepngtools.png", size = 'large')
        st.divider()
        selected = sac.menu([
            sac.MenuItem('Navigation', children = [
                sac.MenuItem('Accueil', icon='house-fill'),
                sac.MenuItem('Leçons', icon='clipboard-fill'),
                sac.MenuItem('Dictionnaire', icon='book-fill'),
                sac.MenuItem('Quizz', icon='joystick'),
                sac.MenuItem('Classement', icon='award-fill'),

            ])
        ], open_all=True)
        

        if selected == "Accueil" and selected != st.session_state["current_page"]:
            st.switch_page("streamlit_app.py")
        elif selected == "Leçons" and selected != st.session_state["current_page"]:
            st.switch_page("pages/page_lecons.py")
        elif selected == "Dictionnaire" and selected != st.session_state["current_page"]:
            st.switch_page("pages/page_dico.py")
        elif selected == "Quizz" and selected != st.session_state["current_page"]:
            st.switch_page("pages/page_quizz.py")
        elif selected == "Classement" and selected != st.session_state["current_page"]:
            st.switch_page("pages/page_classement.py")
